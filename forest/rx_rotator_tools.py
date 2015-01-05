

softlimit_plus = 80.0
softlimit_minus = -90.1

# 

import time
import socket
import threading
import pyinterface

class rx_rotator(object):
    deg2count = 15000.
    
    move_speed = 20000
    move_low_speed = 200
    move_acc = 1000
    move_dec = 1000
    
    softlimit = False
    
    tracking_running = False
    tracking_stop = False
    tracking_stopped = False
    tracking_low_speed = 10
    tracking_acc = 50
    tracking_dec = 50
    tracking_proc_freq = 0.5 # sec
    tracking_P = 1
    tracking_moving = False
    target_position_count = 0
    traget_position_deg = 0
    
    server_host = ''
    cosmos_port = 4010
    cosmos_running = False
    cosmos_stop = False
    cosmos_stopped = False
    err_thresh = 0.3
    
    def __init__(self):
        self.mtr = pyinterface.create_gpg7204(2)
        pass
        
    def move_org(self):
        now = self.mtr.get_position()
        move = -now
        self.mtr.move_with_lock(self.move_speed, move, self.move_low_speed, 
                                self.move_acc, self.move_dec, sspeed=0)
        return
    
    def set_org(self):
        pass
        
    def move(self, degree, lock=True):
        count = self.deg_to_count(degree)
        goto = self.get_position() + degree
        if self.check_softlimit(goto):
            print('softlimit')
            return
            
        try:
            if lock:
                self.mtr.move_with_lock(self.move_speed, count,
                                        self.move_low_speed, self.move_acc,
                                        self.move_dec, sspeed=0)
            else:
                self.mtr.move(self.move_speed, count, self.move_low_speed,
                              self.move_acc, self.move_dec, sspeed=0)
                pass
        except:
            self.stop()
            pass
        return
    
    def goto(self, goto, lock=True):
        move = goto - self.deg_position()
        self.move(move, lock)
        return
        
    def stop(self):
        self.mtr.stop()
        return
        
    def get_position(self):
        cnt = self.mtr.get_position()
        deg = self.count_to_deg(cnt)
        return deg
        
    def check_softlimit(self, goto=None):
        if goto is None: goto = self.get_position()
        if softlimit_minus < goto < softlimit_plus:
            self.softlimit = False
            return False
        self.softlimit = True
        return True
    
    def start_tracking(self):
        th = threading.Thread(target=self._tracking_proc)
        th.start()
        return
    
    def stop_tracking(self):
        if not self.tracking_running: return
        self.tracking_stop = True
        while True:
            if self.tracking_stopped: break
            time.sleep(0.1)
            continue
        self.tracking_stop = False
        self.tracking_stopped = False
        self.tracking_running = False
        return
    
    def _tracking_proc(self):
        self.tracking_running = True
        self.tracking_moving = False
        self.mtr.ctrl.print_log = False
        
        self.current_vel = 0
        self.current_vel_deg = self.count_to_deg(0)
        
        direc0 = +1
        while True:
            if self.tracking_stop: break
            if self.check_softlimit():
                self.stop()
                self.tracking_moving = False
                time.sleep(self.tracking_proc_freq)
                continue
            p0 = self.mtr.get_position()
            p1 = self.target_position_count
            dp = p1 - p0
            self.current_position = p0
            self.current_position_deg = self.count_to_deg(p0)
            self.current_diff = dp
            self.current_diff_deg = self.count_to_deg(dp)
            self.current_timestamp = time.strftime('%y%m%d%H%M%S') + '.%03d'%(int((time.time() - int(time.time()))*1000))
            count = int(dp * self.tracking_P)
            if count < 0: direc = -1
            else: direc = +1
            if abs(count) < self.tracking_low_speed * 3:
                self.stop()
                self.tracking_moving = False
            elif direc != direc0:
                self.stop()
                self.tracking_moving = False
            else:
                if abs(count) > self.move_speed: count = self.move_speed * direc
                self.current_vel = count
                self.current_vel_deg = self.count_to_deg(count)
                #print(p0, p1, count)
                if self.tracking_moving == False:
                    self.mtr.start(count, self.tracking_low_speed,
                                   self.tracking_acc, self.tracking_dec)
                    self.tracking_moving = True
                    time.sleep(0.5)
                else:
                    self.mtr.change_speed(count)
                    pass
                pass
            direc0 = direc
            time.sleep(self.tracking_proc_freq)
            continue
        
        self.stop()
        self.tracking_stopped = True
        self.mtr.ctrl.print_log = True
        return
    
    def set_target_position(self, target):
        self.target_position_deg = target
        self.target_position_count = self.deg_to_count(target)
        return
    
    def deg_to_count(self, deg):
        return deg * self.deg2count
    
    def count_to_deg(self, count):
        return count / self.deg2count
        
    def start_cosmos_client(self):
        th = threading.Thread(target=self._cosmos_client)
        th.start()
        return
    
    def stop_cosmos(self):
        if not self.cosmos_running: return
        self.cosmos_stop = True
        while True:
            if self.cosmos_stopped: break
            time.sleep(0.1)
            continue
        self.cosmos_stop = False
        self.cosmos_stopped = False
        self.cosmos_running = False
        return
    
    def _cosmos_client(self):
        self.cosmos_running = True
        
        server = socket.socket()
        server.settimeout(1)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('(bind) %s:%s'%(self.server_host, self.cosmos_port))
        server.bind((self.server_host, self.cosmos_port))
        server.listen(1)
        
        while True:
            try:
                client, client_address = server.accept()
                print('Accept')
                print(client, client_address)
                client.settimeout(1)
            except socket.timeout:
                if self.cosmos_stop: break
                continue
            
            track_duration = 0
            while True:
                if self.cosmos_stop: break                
                
                try:
                    ret = client.recv(24)
                except socket.timeout:
                    continue
                except socket.error, e:
                    print(e.errno, e.message, e.strerror)
                    print('BREAK')
                    break
                
                print('RECV: %s'%(repr(ret)))
                if ret == '': break
                
                
                ret = ret.strip('\0').split('\t')
                operate = int(ret[0])
                return_flag = int(ret[1])
                timestamp = ret[2]
                target = float(ret[3])
                self.cosmos_latest_recv = [operate, return_flag, timestamp, target]
                
                if abs(self.current_diff_deg) < self.err_thresh:
                    if track_duration > 3: is_tracking = 1
                    else: is_tracking = 0
                    track_duration += 1
                else: 
                    is_tracking = 0
                    track_duration = 0
                    pass
                
                print('[%s] op=%s ret=%s t=%s prog=%s real=%+06.1f diff=%.1f vel=%+06.1f track=%d'% \
                      (time.strftime('%Y/%m/%d %H:%M:%S'), ret[0], ret[1], ret[2], ret[3],
                       self.current_position_deg, self.current_diff_deg, self.current_vel_deg, track_duration))
                
                if operate == 1: 
                    self.set_target_position(target)
                    pass
                    
                if return_flag == 1:
                    err_no = 0
                    err_msg = ''
                    msg = '%d\t%s\t%+06.1f\t%02d\t%50s\0'%(is_tracking, self.current_timestamp,
                                                           self.current_position_deg, err_no, err_msg)
                    print('SEND: %s'%(repr(msg)))
                    client.send(msg)
                    pass
                    
                continue
            continue
        
        self.cosmos_stopped = True
        return

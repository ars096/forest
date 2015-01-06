

# configures
# ==========

# software limit
# --------------
softlimit0_plus = 80.1
softlimit0_minus = -90.1

softlimit1_plus = 80.5
softlimit1_minus = -90.5

softlimit2_plus = 83.0
softlimit2_minus = -93.0

# speed
# -----
max_speed = 1.4   # deg sec-1
min_speed = 0.05   # deg sec-1

#
# --
cosmos_server_port = 4010

#
# ========= 
#
 

import time
import socket
import threading
import pyinterface

class rx_rotator_controller(object):
    deg2count = 15000.
    
    real_angle = 0.
    real_vel = 0.
    prog_angle = 0.
    cosmos_angle = 0.
    residual = 0.
    
    error = []
    
    shutdown_flag = False
    
    softlimit0_flag = False
    softlimit1_flag = False
    softlimit1_interval = 0.2
    softlimit2_flag = False
    softlimit2_interval = 0.1
    
    position_interval = 0.1
    
    tracking_count = 0
    tracking_interval = 0.5
    
    move_low_speed = 10
    move_acc = 50
    move_dec = 50
    
    cosmos_flag = False
    cosmos_recv = ''
    cosmos_send = ''
        
    def __init__(self):
        self.mtr = pyinterface.create_gpg7204(2)
        self.motion = motion_controller()
        self.start_logger()
        self.start_limit_handler()
        self.start_position_reader()
        self.start_tracking_proc()
        self.start_cosmos_server()
        pass
    
    def print(self, msg):
        print(msg)
        return
        
    def print_error(self, msg):
        self.error.append(msg)
        self.print('!!!! ERROR !!!! ' + msg)
        return
    
    def start_logger(self):
        return
        
    def start_limit_handler(self):
        sl2 = threading.Thread(target=self._start_softlimit_proc2)
        sl2.start()
        sl1 = threading.Thread(target=self._start_softlimit_proc1)
        sl1.start()
        return
        
    def _start_softlimit_proc2(self):
        self.print('INFO: start software limit 2')
        self.print('INFO: softlimit2 = %.2f, %.2f'%(softlimit2_minus,
                                                    softlimit2_plus))
        while True:
            try:
                self._softlimit_proc2()
            except Exception as e:
                self.print('**********************************************')
                self.print_error('software limit 2 except error: %s'%(e.msg))
                self.print('**********************************************')
                self.print('INFO: restart softlimit_proc2')
                continue
            break
        self.print('INFO: stop software limit 2')
        return
        
    def _softlimit_proc2(self):
        self.softlimit2_flag = False
        while True:
            if self.shutdown_flag:
                self.print('INFO: softlimit2: detect shutdown signal')
                self.print('INFO: softlimit2: break')
                break
            
            if softlimit2_minus < self.real_angle < softlimit2_plus:
                time.sleep(self.softlimit2_interval)
                continue
            
            self.print('**********************************************')
            self.print('**********************************************')
            self.print_error('SOFTLIMIT2 TRIGGERED : SYSTEM HALT')
            self.print('**********************************************')
            self.print('**********************************************')
            
            self.mtr.stop()
            self.mtr.ctrl.close()
            del(self.mtr.ctrl)
            del(self.mtr)
            self.softlimit2_flag = True
            self.shutdown_flag = True
            break
        return
        
    def _start_softlimit_proc1(self):
        self.print('INFO: start software limit 1')
        self.print('INFO: softlimit1 = %.2f, %.2f'%(softlimit1_minus,
                                                    softlimit1_plus))
        while True:
            try:
                self._softlimit_proc1()
            except Exception as e:
                self.print('**********************************************')
                self.print_error('software limit 1 except error: %s'%(e.msg))
                self.print('**********************************************')
                self.print('INFO: restart softlimit_proc1')
                continue
            break
        self.print('INFO: stop software limit 1')
        return
        
    def _softlimit_proc1(self):
        self.softlimit1_flag = False
        while True:
            if self.shutdown_flag: 
                self.print('INFO: softlimit1: detect shutdown signal')
                self.print('INFO: softlimit1: break')
                break
            
            if softlimit1_minus < self.real_angle < softlimit1_plus:
                self.softlimit1_flag = False
                time.sleep(self.softlimit1_interval)
                continue
            
            if self.softlimit1_flag == False:
                self.print('**********************************************')
                self.print('**********************************************')
                self.print_error('SOFTLIMIT1 TRIGGERED : SYSTEM LOCK')
                self.print('**********************************************')
                self.print('**********************************************')
                self.softlimit1_flag = True
                pass
                
            time.sleep(self.softlimit1_interval)
            break
        return
    
    def start_position_reader(self):
        self.print('INFO: start position reader')
        
        while True:
            try:
                self._position_proc()
            except Exception as e:
                self.print('**********************************************')
                self.print_error('position reader except error: %s'%(e.msg))
                self.print('**********************************************')
                self.print('INFO: restart position_reader')
                continue
            break
        self.print('INFO: stop position reader')
        return
    
    def _position_proc(self):
        while True:
            if self.shutdown_flag: 
                self.print('INFO: position: detect shutdown signal')
                self.print('INFO: position: break')
                break
            
            p0 = self.real_angle
            p1 = self.get_position()
            self.real_angle = p1
            self.real_vel = p1 - p0
            self.residual = self.prog_angle - p1
            self.real_timestamp = time.strftime('%y%m%d%H%M%S') + \
                                  '.%03d'%(int((time.time() - int(time.time()))*1000))
            time.sleep(self.position_interval)
            continue
        return
    
    def start_tracking_proc(self):
        self.print('INFO: start tracking proc')
        
        while True:
            try:
                self._position_proc()
            except Exception as e:
                self.print('**********************************************')
                self.print_error('tracking proc except error: %s'%(e.msg))
                self.print('**********************************************')
                self.print('INFO: restart tracking_proc')
                continue
            break
        self.print('INFO: stop tracking proc')
        return
        
    def _tracking_proc(self):
        while True:
            if self.shutdown_flag: 
                self.print('INFO: tracking: detect shutdown signal')
                self.print('INFO: tracking: break')
                break
            
            if self.softlimit1_flag:
                self.stop()
                msg = 'ERROR: REAL ANGLE IS OVER SOFT-LIMIT (%.1f)'%(self.real_angle)
                self.print(msg)
            
            elif not(softlimit0_minus < self.prog_angle < softlimit0_plus):
                msg = 'PROG ANGLE IS OVER RANGE (%.1f)'%(self.prog_angle)
                if self.softlimit0_flag == False:
                    self.print_error(msg)
                else:
                    self.print('ERROR: '+msg)
                    pass
                self.softlimit0_flag = True
                pass
            
            else:
                self.softlimit0_flag = False
                
                if self.real_vel < min_speed:
                    self.tracking_count += 1
                    try:
                        self._move_angle(self.prog_angle)
                    except Exception as e:
                        self.print_error('%s (p0=%.1f, v0=%.1f, p1=%.1f)'%
                                         (e.msg, self.real_angle,
                                          self.real_vel, self.prog_angle))
                        pass
                else:
                    self.tracking_count = 0
                    pass
                pass
                
            
            time.sleep(self.tracking_interval)
            continue
        return
    
    def start_cosmos_server(self):
        self.print('INFO: start cosmos server')
        
        while True:
            try:
                self._cosmos_server()
            except Exception as e:
                self.print('**********************************************')
                self.print_error('cosmos server except error: %s'%(e.msg))
                self.print('**********************************************')
                self.print('INFO: restart cosmos_server')
                continue
            break
        self.print('INFO: stop cosmos server')
        return
        
    def _cosmos_server(self):
        server = socket.socket()
        server.settimeout(1)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.print('INFO: cosmos: (bind) %s:%s'%('', cosmos_server_port))
        server.bind(('', cosmos_server_port))
        server.listen(1)
        
        while True:
            self.cosmos_flag = False
            
            try:
                client, client_address = server.accept()
                self.print('INFO: cosmos: Accept from %s:%d'%(client, client_address))
                client.settimeout(1)
            
            except socket.timeout:
                if self.shutdown_flag:
                    self.print('INFO: cosmos: detect shutdown signal')
                    self.print('INFO: cosmos: break')
                    break
                continue
            
            self.cosmos_flag = True

            while True:
                if self.shutdown_flag: 
                    self.print('INFO: cosmos: detect shutdown signal')
                    self.print('INFO: cosmos: break')
                    break
                
                try:
                    ret = client.recv(24)
                except socket.timeout:
                    continue
                except socket.error, e:
                    self.print_error('cosmos: %s'str((e.errno, e.message, e.strerror)))
                    self.print('INFO: cosmos: connection break')
                    break
                
                #print('RECV: %s'%(repr(ret)))
                self.cosmos_recv = ret
                if ret == '': 
                    self.print('INFO: cosmos: connection break')
                    break
                
                ret = ret.strip('\0').split('\t')
                operate = int(ret[0])
                return_flag = int(ret[1])
                timestamp = ret[2]
                target = float(ret[3])
                self.cosmos_angle = target
                
                if self.tracking_count > 4: is_tracking = 1
                else: is_tracking = 0
                
                msg = '[%s] op=%s ret=%s t=%s prog=%s '%(time.strftime('%Y/%m/%d %H:%M:%S'),
                                                         ret[0], ret[1], ret[2], ret[3])
                msg += 'real=%+06.1f diff=%.1f vel=%+06.1f track=%d'%(self.real_angle,
                                                                      self.residual,
                                                                      self.real_vel,
                                                                      self.tracking_count))
                self.print(msg)
                
                if operate == 1: 
                    self.move(target)
                    pass
                
                if return_flag == 1:
                    err_no = 0
                    err_msg = ''
                    msg = '%d\t%s\t%+06.1f\t%02d\t%50s\0'%(is_tracking, self.real_timestamp,
                                                           self.real_angle, err_no, err_msg)
                    #print('SEND: %s'%(repr(msg)))
                    self.cosmos_send = msg
                    client.send(msg)
                    pass
                continue
            continue
        return
    
    def deg_to_count(self, deg):
        return deg * self.deg2count
    
    def count_to_deg(self, count):
        return count / self.deg2count
        
    def get_position(self):
        cnt = self.mtr.get_position()
        deg = self.count_to_deg(cnt)
        return deg
        
    def move_org(self):
        now = self.mtr.get_position()
        move = -now
        self.mtr.move_with_lock(max_speed, move, self.move_low_speed, 
                                self.move_acc, self.move_dec)
        return
    
    def _move_angle(self, deg):
        p0 = self.real_angle
        p1 = deg
        vel = self.motion.calc_speed(p0, p1)
        count = self.deg_to_count(deg)
        v_count = self.deg_to_count(vel)
        self._move_count(count, v_count)
        return
    
    def _move_count(self, count, speed=max_speed):
        now = self.mtr.get_position()
        move = count - now
        
        if move == 0: return
        
        self.mtr.move(speed, move, self.move_low_speed, self.move_acc, self.move_dec)
        return

    def move(self, degree):
        self.prog_angle = degree
        return

    def stop(self):
        self.mtr.stop()
        return
        
    def shutdown_start(self):
        self.shutdown_flag = True
        return
    
    def read_status(self):
        ret = {'real_angle': self.real_angle,
               'real_vel': self.real_vel,
               'prog_angle': self.prog_angle,
               'cosmos_angle': self.cosmos_angle,
               'residual': self.residual,
               'shutdown_flag': self.shutdown_flag,
               'softlimit0_flag': self.softlimit0_flag,
               'softlimit1_flag': self.softlimit1_flag,
               'softlimit2_flag': self.softlimit2_flag,
               'cosmos_flag': self.cosmos_flag,
               'tracking_count': self.tracking_count}
        return ret
        
    def read_error(self):
        ret = self.error
        self.error = []
        return ret
        
    def read_cosmos_log(self):
        recv = self.cosmos_recv
        send = self.cosmos_send
        self.cosmos_recv = ''
        self.cosmos_send = ''
        return (recv, send)

def rx_rotator():
    client = pyinterface.server_client_wrapper.control_client_wrapper(
        rx_rotator_controller, '192.168.40.13', 4003)
    return client

def rx_rotator_monitor():
    client = pyinterface.server_client_wrapper.monitor_client_wrapper(
        rx_rotator_controller, '192.168.40.13', 4103)
    return client

def start_rx_rotator_server():
    rxrot = rx_rotator_controller()
    server = pyinterface.server_client_wrapper.server_wrapper(rxrot,
                                                              '', 4003, 4103)
    server.start()
    return server



class motion_controller(object):
    
    def calc_speed(self, p0, p1):
        delt = p1 - p0
        v = delt
        
        if v < 0: direc = -1
        else: direc = 1
        
        if abs(v) > max_speed: v = max_speed * direc
        if abs(v) < min_speed: v = min_speed * direc
        
        return v
        


import sys
import time
import forest

class forest_script_base(object):
    method = ''
    ver = ''
    
    def __init__(self):
        self.log = forest.db_writer('operation_log')
        self.stdout = stdout()
        self.stderr = stderr()
        pass
    
    def check_other_operation(self):
        latest = self.log.get_latest_item()
        flag = latest[2]
        
        if flag != 'Done.':
            other = latest[3]
            other_ts = latest[2].strftime('%Y/%m/%d %H:%M:%S')
            msg = 'Other process is now running. '
            msg += '(%s; from %s)'%(other, other_ts)
            self.stderr.p(msg + '[%s]'%(self.method))
            raise Exception(msg)
        
        return

    def operation_start(self, args='', logfile=''):
        self.log.insert(keydict={'flag': 'START',
                                 'method': self.method,
                                 'args': args})
        
        if logfile != '':
            self.stdout.set_output_file(logfile)
            self.stderr.set_output_file(logfile)
        else:
            self.stdout.reset()
            self.stderr.reset()
            pass
        
        return
        
    def operation_done(self):
        self.log.insert(keydict={'flag': 'Done.',
                                 'method': self.method})
        return
        
    def open_sis_biasbox(self):
        self.stdout.write('Opening SIS bias box ... ')
        sis = forest.biasbox()
        self.stdout.write('ok')
        self.stdout.nextline()
        return sis

    def open_lo_sg(self):
        self.stdout.write('Opening 1st LO SG ... ')
        lo_sg = None
        self.stdout.write('NG')
        self.stdout.nextline()
        return lo_sg
    
    def open_lo_att(self):
        self.stdout.write('Opening 1st LO Attenuator ... ')
        lo_att = forest.loatt()
        self.stdout.write('ok')
        self.stdout.nextline()
        return lo_att
    
    def open_irr_sg(self):
        self.stdout.write('Opening IRR Signal SG ... ')
        irr_sg = None
        self.stdout.write('NG')
        self.stdout.nextline()
        return irr_sg
    
    def open_rxrot(self):
        self.stdout.write('Opening Rx Rotator ... ')
        rxrot = forest.rx_rotator()
        self.stdout.write('ok')
        self.stdout.nextline()
        return rxrot
    
    def open_slider(self):
        self.stdout.write('Opening Sliding Chopper ... ')
        slider = forest.slider()
        self.stdout.write('ok')
        self.stdout.nextline()
        return slider
    
        
        
    def run(self, *args, **kwargs):
        pass
        


class logger(object):
    table = ''
    colname = ''
    output_file = ''
    history = []
    tmp = ''
    
    def __init__(self):
        self.db = forest.db_writer(self.table)
        pass
    
    def reset(self):
        self.history = []
        self.tmp = ''
        return
        
    def set_output_file(self, filepath):
        self.output_file = filepath
        open(filepath, 'w').write('')
        self.reset()
        return
    
    def p(self, msg):
        self.write(msg)
        self.nextline()
        return
        
    def write(self, msg):
        self.tmp += msg
        sys.stdout.write(msg)
        self.flush()
        return
        
    def nextline(self):
        msg = self.tmp
        msg2 = time.strftime('[%Y/%m/%d.%H:%M:%S] ') + msg
        
        self.db.insert(keydict={self.colname: msg})
        
        if self.output_file != '':
            open(self.output_file, 'a').write(msg2+'\n')
            pass
        
        self.history.append(msg2)
        
        sys.stdout.write('\r%s\n'%(msg2))
        self.flush()
        
        self.tmp = ''
        return
        
    def flush(self):
        sys.stdout.flush()
        return


class stdout(logger):
    table = 'operation_console_log'
    colname = 'msg'

class stderr(logger):
    table = 'operation_error_log'
    colname = 'error'

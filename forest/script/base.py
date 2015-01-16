
import sys
import forest

class forest_script_base(object):
    method = ''
    
    def __init__(self):
        self.log = forest.db_writer('operation_log')
        self.stdout = stdout()
        self.stderr = stderr()
        pass
    
    def check_other_operation(self):
        latest = self.log.get_latest_item(2)
        flag = latest[0][2]
        
        if flag != 'Done.':
            other = latest[1][3]
            other_ts = latest[1][2].strftime('%Y/%m/%d %H:%M:%S')
            msg = 'Other process is now running. '
            msg += '(%s; from %s)'%(other, other_ts)
            self.stderr.p(msg + '[%s]'%(self.method))
            raise Exception(msg)
        
        return

    def operation_start(self, args=''):
        self.log.insert(keydict={'flag': 'START',
                                 'method': self.method,
                                 'args': args})
        return
        
    def operation_done(self):
        self.log.insert(keydict={'flag': 'Done.',
                                 'method': self.method})
        return
        

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
        self.history = ''
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
        return
        
    def nextline(self):
        self.db.insert(keydict={self.colname: self.tmp})
        if self.output_file != '':
            open(self.output_file, 'a').write(self.tmp+'\n')
            pass
        self.history.append(self.tmp)
        self.tmp = ''
        sys.stdout.write('\n')
        self.flush()
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

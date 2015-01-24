#! /usr/bin/env python


interval = 10.0


# ----

import time
import forest

sql_status = forest.db_writer('IF_switch')

# --

def printlog(status):
    forest.print_switch(status)
    return

# --

try:
    while True:
        forest.print_timestamp()
        t0 = time.time()
        
        if forest.is_operating():
            print('operation is running ...')
            
        else:
            switch = forest.switch()
            
            ch = switch.ch_check()
            
            del(switch)
            
            keydict = {}
            keydict['CH1'] = ch[0]
            keydict['CH2'] = ch[1]
            keydict['CH3'] = ch[2]
            keydict['CH4'] = ch[3]
            
            sql_status.insert(keydict=keydict)        
            printlog(ch)
            pass
            
        t1 = time.time()
        dt = t1 - t0
        if dt < interval: time.sleep(interval - dt)
        continue

except KeyboardInterrupt:
    print('break')
    pass


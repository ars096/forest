#! /usr/bin/env python


interval = 10.0


# ----

import time
import forest

rxrot_monitor = forest.rx_rotator_monitor()
sql_status = forest.db_writer('rxrot_status')
sql_error = forest.db_writer('rxrot_errors')
sql_cosmos = forest.db_writer('rxrot_cosmos_log')

# --

def printlog(status):
    forest.print_rxrot(status)
    return

# --

try:
    while True:
        forest.print_timestamp()
        
        t0 = time.time()
        
        status = rxrot_monitor.read_status()
        
        keydict = {}
        keydict['REAL_ANGLE'] = status['real_angle']
        keydict['REAL_VEL'] = status['real_vel']
        keydict['PROG_ANGLE'] = status['prog_angle']
        keydict['COSMOS_ANGLE'] = status['cosmos_angle']
        keydict['RESIDUAL'] = status['residual']
        keydict['TRACKING'] = status['tracking_count']
        keydict['SHUTDOWN_FLAG'] = status['shutdown_flag']
        keydict['SOFTLIMIT0_FLAG'] = status['softlimit0_flag']
        keydict['SOFTLIMIT1_FLAG'] = status['softlimit1_flag']
        keydict['SOFTLIMIT2_FLAG'] = status['softlimit2_flag']
        keydict['COSMOS_FLAG'] = status['cosmos_flag']
        sql_status.insert(keydict=keydict)        
        printlog(status)
        
        errors = rxrot_monitor.read_error()
        if errors != []:
            for e in errors:
                keydict = {}
                keydict['ERROR'] = e
                sql_error.insert(keydict=keydict)
                print('ERROR: %s'%(e))
                continue
            pass
        
        cosmos = rxrot_monitor.read_cosmos_log()
        if cosmos != ('', ''):
            keydict = {}
            keydict['RECV_MSG'] = cosmos[0]
            keydict['SEND_MSG'] = cosmos[1]
            print('COSMOS:RECV: %s'%(repr(cosmos[0])))
            print('COSMOS:SEND: %s'%(repr(cosmos[1])))
            pass
        
        t1 = time.time()
        dt = t1 - t0
        if dt < interval: time.sleep(interval - dt)
        continue

except KeyboardInterrupt:
    print('break')
    pass


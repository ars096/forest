#! /usr/bin/env python


interval = 10.0


# ----

import time
import forest

rxrot_monitor = forest.rx_rot_monitor()
sql_status = forest.db_writer('rxrot_status')
sql_error = forest.db_writer('rxrot_errors')
sql_cosmos = forest.db_writer('rxrot_cosmos')

# --

def printlog(bias):
    #forest.print_loatt(bias)
    return

# --

try:
    while True:
        t0 = time.time()
        
        status = rxrot_monitor.read_status()
        
        """
        keydict = {}
        for _ch, _b in zip(ch, bias):
            keydict['BIAS_V%02d'%_ch] = _b
            continue
        
        sql.insert(keydict=keydict)
        printlog(bias)
        """
        
        errors = rxrot_monitor.read_error()
        
        #
        #
        #
        
        cosmos = rxrot_monitor.read_cosmos_log()
        
        #
        #
        #
        
        t1 = time.time()
        dt = t1 - t0
        if dt < interval: time.sleep(interval - dt)
        continue

except KeyboardInterrupt:
    print('break')
    pass


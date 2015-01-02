#! /usr/bin/env python


interval = 60.0


# ----

import time
import forest

biasbox_monitor = forest.biasbox_monitor()
sql = forest.db_writer('sis_bias')

# --

def printlog(bias):
    forest.print_timestamp()
    forest.print_bias(bias)
    return

# --

ch = range(1, 17)

try:
    while True:
        t0 = time.time()
        
        v, i = biasbox_monitor.read_bias()
        
        keydict = {}
        for _ch, _v, _i in zip(ch, v, i):
            keydict['BIAS_V%02d'%_ch] = _v
            keydict['BIAS_I%02d'%_ch] = _i
            continue
        
        sql.insert(keydict=keydict)
        printlog((v, i))
        
        t1 = time.time()
        dt = t1 - t0
        if dt < interval: time.sleep(interval - dt)
        continue

except KeyboardInterrupt:
    print('break')
    pass


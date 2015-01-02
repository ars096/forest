#! /usr/bin/env python


interval = 60.0


# ----

import time
import forest

loatt_monitor = forest.loatt_monitor()
sql = forest.db_writer('lo_att')

# --

def printlog(bias):
    forest.print_timestamp()
    forest.print_loatt(bias)
    return

# --

ch = range(1, 9)

try:
    while True:
        t0 = time.time()
        
        bias = loatt_monitor.read_bias()
        
        keydict = {}
        for _ch, _b in zip(ch, bias):
            keydict['BIAS_V%02d'%_ch] = _b
            continue
        
        sql.insert(keydict=keydict)
        printlog(bias)
        
        t1 = time.time()
        dt = t1 - t0
        if dt < interval: time.sleep(interval - dt)
        continue

except KeyboardInterrupt:
    print('break')
    pass


#! /usr/bin/env python


check_interval = 1.0
update_interval = 600.0

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
        
        sql.update(keydict, update_interval)
        printlog(bias)
        
        t1 = time.time()
        dt = t1 - t0
        if dt < check_interval: time.sleep(check_interval - dt)
        continue

except KeyboardInterrupt:
    print('break')
    pass


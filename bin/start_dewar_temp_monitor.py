#! /usr/bin/env python


check_interval = 1.0
update_interval = 600.0


# ----

import time
import forest

tm = forest.dewar_temp()
sql = forest.db_writer('dewar_temp')

# --

def printlog(k):
    ts = time.strftime('%Y/%m/%d.%H:%M:%S')
    temp = ', '.join(['%.2f K'%(_k) for _k in k])
    print('[%s] %s'%(ts, temp))
    return

# --

ch = tm.ch
name = ['%s, %s'%(_n, _sn) for _n, _sn in zip(tm.curve_name, tm.curve_sn)]


try:
    while True:
        t0 = time.time()
        
        k, su = tm.temperature_query()
        
        keydict = {}
        for _c, _n, _k, _s in zip(ch, name, k, su):
            keydict['SENSOR%d'%_c] = _n
            keydict['K%d'%_c] = _k
            keydict['SU%d'%_c] = _s
            continue
        
        sql.update(keydict, update_interval)
        printlog(k)
        
        t1 = time.time()
        dt = t1 - t0
        if dt < check_interval: time.sleep(check_interval - dt)
        continue

except KeyboardInterrupt:
    print('break')
    pass


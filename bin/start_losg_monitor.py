#! /usr/bin/env python


interval = 10.0


# ----

import time
import forest

sql_status = forest.db_writer('lo_sg')

# --

def printlog(status):
    forest.print_losg(status)
    return

# --

try:
    while True:
        forest.print_timestamp()
        t0 = time.time()
        
        if forest.is_observing():
            print('observation is running ...')
            
        else:
            losg = forest.losg()
            
            freq = losg.freq_query()
            power = losg.power_query()
            output = losg.output_query()
            
            del(losg)
            
            keydict = {}
            keydict['FREQ1'] = freq[0]
            keydict['POWER1'] = power[0]
            keydict['OUTPUT1'] = output[0]
            keydict['FREQ2'] = freq[1]
            keydict['POWER2'] = power[1]
            keydict['OUTPUT2'] = output[1]

            
            sql_status.insert(keydict=keydict)
            printlog([freq, power, output])
            pass
            
        t1 = time.time()
        dt = t1 - t0
        if dt < interval: time.sleep(interval - dt)
        continue

except KeyboardInterrupt:
    print('break')
    pass


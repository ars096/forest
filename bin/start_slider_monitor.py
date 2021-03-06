#! /usr/bin/env python



check_interval = 1.0
update_interval = 600.0


# ----

import time
import forest

slider_monitor = forest.slider_monitor()
sql_status = forest.db_writer('slider_status')

# --

def printlog(status):
    forest.print_slider(status)
    return

# --

try:
    while True:
        forest.print_timestamp()
        
        t0 = time.time()
        
        position = slider_monitor.read_position()
        count = slider_monitor.read_count()
        
        keydict = {}
        keydict['POSITION'] = position
        keydict['COUNT'] = count

        sql_status.update(keydict, update_interval)        
        printlog([position, count])
    
        t1 = time.time()
        dt = t1 - t0
        if dt < check_interval: time.sleep(check_interval - dt)
        continue

except KeyboardInterrupt:
    print('break')
    pass


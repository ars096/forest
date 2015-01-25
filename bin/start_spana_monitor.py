#! /usr/bin/env python


interval = 60.0


# ----

import pickle
import zlib
import time
import forest

sql_status = forest.db_writer('spana')

# --

def printlog(status):
    forest.print_spana(status)
    return

# --

try:
    while True:
        forest.print_timestamp()
        t0 = time.time()
        
        if forest.is_operating():
            print('operation is running ...')
            
        else:
            spana = forest.speana()
            
            ch = spana.trace_data_query()
            
            del(spana)
            
            keydict = {}
            keydict['SPANA1'] = pickle.dumps(ch[0])
            keydict['SPANA2'] = pickle.dumps(ch[1])
            keydict['SPANA3'] = pickle.dumps(ch[2])
            keydict['SPANA4'] = pickle.dumps(ch[3])
            
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


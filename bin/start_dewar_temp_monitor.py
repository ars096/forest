#! /usr/bin/env python

import datetime
import forest

tm = forest.dewar_temp()

ch = tm.ch
name = ['%s, %s'%(_n, _sn) for _n, _sn in zip(tm.curve_name, tm.curve_sn)]

try:
    while True:
        k, su = tm.temperature_query()
        
        for 
        
        continue
except KeyboardInterrupt:
    print('break')
    pass


#! /usr/bin/env python

import time
import forest

print('~~~~~~~~~~~~~~~')
print('IRR Att. SERVER')
print('~~~~~~~~~~~~~~~')
print('')

irratt = forest.start_irratt_server()

try:
    while True:
        time.sleep(1)
        continue
except KeyboardInterrupt:
    irratt.shutdown()
    c = forest.irratt()
    c.server_stop()
    time.sleep(2)
    pass

print('')
print('done.')

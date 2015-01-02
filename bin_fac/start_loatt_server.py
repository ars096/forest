#! /usr/bin/env python

import time
import forest

print('~~~~~~~~~~~~~~')
print('LO Att. SERVER')
print('~~~~~~~~~~~~~~')
print('')

loatt = forest.start_loatt_server()

try:
    while True:
        time.sleep(1)
        continue
except KeyboardInterrupt:
    loatt.shutdown()
    c = forest.loatt()
    c.server_stop()
    time.sleep(2)
    pass

print('')
print('done.')

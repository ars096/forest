#! /usr/bin/env python

import time
import forest

print('~~~~~~~~~~~~~~~~~')
print('Rx Rotator SERVER')
print('~~~~~~~~~~~~~~~~~')
print('')

rot = forest.start_rx_rotator_server()

try:
    while True:
        time.sleep(1)
        continue
except KeyboardInterrupt:
    rot.shutdown_start()
    rot.shutdown()
    c = forest.rx_rotator()
    c.server_stop()
    time.sleep(2)
    pass

print('')
print('done.')

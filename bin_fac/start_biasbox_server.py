#! /usr/bin/env python

import time
import forest

print('===================')
print('SIS BIAS-BOX SERVER')
print('===================')
print('')

biasbox = forest.start_biasbox_server()

try:
    while True:
        time.sleep(1)
        continue
except KeyboardInterrupt:
    biasbox.shutdown()
    c = forest.biasbox()
    c.server_stop()
    time.sleep(2)
    pass

print('')
print('done.')

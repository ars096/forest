#! /usr/bin/env python

import time
import forest

print('~~~~~~~~~~~~~~~~~')
print('Slider SERVER')
print('~~~~~~~~~~~~~~~~~')
print('')

slider = forest.start_slider_server()

try:
    while True:
        time.sleep(1)
        continue
except KeyboardInterrupt:
    slider.instance.shutdown()
    slider.shutdown()
    c = forest.slider()
    c.server_stop()
    time.sleep(2)
    pass

print('')
print('done.')

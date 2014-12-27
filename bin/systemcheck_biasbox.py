#! /usr/bin/env python


name = 'systemcheck_biasbox'


# -----

import time
import numpy
import pylab
import forest

fp = forest.filepath_generator(name)

biasbox = instruments.biasbox()

data = numpy.linspace(0, 1, 101)
v, i = biasbox.bias_sweep(data)
biasbox.bias_set(0)

# --

ch = instruments.biasbox_tools.biasbox_ch_mapper()

pylab.rcParams['font.size'] = 8

fig = pylab.figure(figsize=(16,12))
ax = [fig.add_subplot(4, 4, j) for j in range(1, 17)]
for _ax, _n, _box, _ch, _beam, _pol, _unit \
    in zip(ax, ch.sis, ch.box, ch.ch, ch.beam, ch.pol, ch.dsbunit):
    _ax.plot(v[:,_n-1], i[:,_n-1], '+')
    _ax.text(0.1, 0.8, 'Box: %d, CH: %d'%(_box, _ch), transform=_ax.transAxes)
    _ax.text(0.1, 0.7, 'Beam: %d, Pol: %s, Unit: %d'%(_beam, _pol, _unit),
             transform=_ax.transAxes)
    _ax.grid(True)
    _ax.set_xlabel('Bias Voltage (mV)')
    _ax.set_ylabel('Bias Current (mA)')
    continue

fig.suptitle('systemcheck_biasbox :: %s'%(time.strftime('%Y/%m/%d %H:%M:%S')))
fig.savefig(fp('fig.bias.%s.png')


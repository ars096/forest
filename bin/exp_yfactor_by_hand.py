#! /usr/bin/env python

# configures
# ==========

# default values
# --------------
f_start = 0  # GHz
f_stop = 12  # GHz
resbw = 3    # MHz  (10Hz - 3MHz)
average = 5 

eval_ch = [1, 2, 3, 4]

thot = 300.0 # K

# --

name = 'exp_yfactor_by_hand'


# import
# ======

import sys
import time
import argparse
import numpy
import pylab
import forest


# argparse configure
# ==================

desc = 'Y-factor by hand.'

p = argparse.ArgumentParser(description=desc)
p.add_argument('--start', type=float,
               help='Start freq. in GHz. default is %.2f GHz'%(f_start))
p.add_argument('--stop', type=float,
               help='Stop freq. in GHz. default is %.2f GHz'%(f_stop))
p.add_argument('--resbw', type=float,
               help='Resolution BW in MHz. default is %.2f MHz'%(resbw))
p.add_argument('--average', type=int,
               help='Average num to acqumerate. default is %d.'%(average))
p.add_argument('--ch',  type=str,
               help='Ch numbers to be evalulated. default is %s.'%(eval_ch))
p.add_argument('--thot', type=float,
               help='Hot temperature in K. default is %.1f'%(thot))

args = p.parse_args()


# main
# ====

print('~~~~~~~~~~~~~~~~~~~~~~~~~')
print('FOREST : Y-factor by hand')
print('~~~~~~~~~~~~~~~~~~~~~~~~~')
forest.print_timestamp()
print('')


# create save directory
# ---------------------
fp = forest.filepath_generator(name)


# handling args
# -------------
if args.start is not None: f_start = args.start
if args.stop is not None: f_stop = args.stop
if args.resbw is not None: resbw = args.resbw
if args.average is not None: average = args.average
if args.ch is not None:
    if args.ch.find('[') != -1: eval_ch = eval(args.ch)
    else: eval_ch = int(args.ch)
    pass
if args.thot is not None: thot = args.thot

params = 'f_start = %f\n'%(f_start)
params += 'f_stop = %f\n'%(f_stop)
params += 'resbw = %f\n'%(resbw)
params += 'average = %d\n'%(average)
params += 'ch = %s\n'%(str(eval_ch))
params += 'thot = %f\n'%(thot)
open(fp('log.params.%s.txt'), 'w').writelines(params)

print('')

# open devices
# ------------
print('open devices')
print('============')

print('spectrum analyzers...'),
sys.stdout.flush()
sp = forest.speana()
time.sleep(1)
print('')

print('IF switches...'),
sys.stdout.flush()
sw = forest.switch()
print('')

print('')


# init devices
# ------------
print('init devices')
print('============')

print('INFO: f_start = %f GHz'%(f_start))
sp.frequency_start_set(f_start, 'GHz')

print('INFO: f_stop = %f GHz'%(f_stop))
sp.frequency_stop_set(f_stop, 'GHz')

print('INFO: resbw = %f MHz'%(resbw))
sp.resolution_bw_set(resbw, 'MHz')

print('INFO: average = %d'%(average))
sp.average_set(average)
sp.average_onoff_set('ON')
sweeptime = sp.sweep_time_query()[0]
acquiretime = sweeptime * average
print('INFO: acquiretime = %f sec.'%(acquiretime))

print('INFO: switch set ch 1')
sw.ch_set_all(1)

print('')


# init data set
# -------------
dcold = []
dhot = []

freq = sp.sp[0].gen_xaxis()
numpy.save(fp('freq.%s.npy'), freq)


# get cold
# --------
raw_input("Set COLD mode, then 'Enter' to start...")
print('')

for i in eval_ch:
    print('acquire ch%d, waittime=%.1f'%(i, acquiretime))
    sw.ch_set_all(i)
    time.sleep(0.2)
    sp.average_restart()
    time.sleep(acquiretime)
    _d = sp.trace_data_query()
    dcold.append(_d)
    continue

print('save: %s'%fp('data.cold.%s.npy'))
dcold = numpy.array(dcold)
numpy.save(fp('data.cold.%s.npy'), dcold)

print('')

# get hot
# -------
raw_input("Set HOT mode, then 'Enter' to start...")
print('')

for i in eval_ch:
    print('acquire ch%d, waittime=%.1f'%(i, acquiretime))
    sw.ch_set_all(i)
    time.sleep(0.2)
    sp.average_restart()
    time.sleep(acquiretime)
    _d = sp.trace_data_query()
    dhot.append(_d)
    continue
    
print('save: %s'%fp('data.hot.%s.npy'))
dhot = numpy.array(dhot)
numpy.save(fp('data.hot.%s.npy'), dhot)

print('')

print('INFO: switch set ch 1')
sw.ch_set_all(1)

print('')

# calc y-factor
# -------------
print('calc Tsys*...')
tsys = forest.rsky_dB(dhot, dcold, thot)
numpy.save(fp('data.tsys.%s.npy'), tsys)


# plot part
# ---------

ax_x = 4
ax_y = len(eval_ch)
ax_num = ax_x * ax_y

dhot = dhot.reshape([ax_num, -1])
dcold = dcold.reshape([ax_num, -1])
tsys = tsys.reshape([ax_num, -1])

g_freq = freq * 1e-9

speana = ['SP:1', 'SP:2', 'SP:3', 'SP:4'] * ax_y 
switch = ['SW:%d'%_ch for i in range(ax_x) for _ch in eval_ch]
label = ['%s, %s'%(_sw, _sp) for _sw, _sp in zip(switch, speana)]

if numpy.nanmax(tsys) < 300: tsys_max = 300
elif numpy.nanmax(tsys) < 500: tsys_max = 500
else: tsys_max = 1000

pylab.rcParams['font.size'] = 7

fig = pylab.figure()
fig.suptitle('y-factor : %s'%(time.strftime('%Y/%m/%d %H:%M:%S')), fontsize=12)
ax = [fig.add_subplot(ax_y, ax_x, i+1) for i in range(ax_num)]
ax2 = [_a.twinx() for _a in ax]
[_a.plot(g_freq, _hot, 'r-') for _a, _hot in zip(ax, dhot)]
[_a.plot(g_freq, _cold, 'b-') for _a, _cold in zip(ax, dcold)]
[_a.plot(g_freq, _tsys, 'k-') for _a, _tsys in zip(ax2, tsys)]
[_a.text(0.1, 0.8, _l, transform=_a.transAxes, fontsize=12)
 for _a, _l in zip(ax, label)]
[_a.set_xlim(g_freq.min(), g_freq.max()) for _a in ax]
[_a.set_xlim(g_freq.min(), g_freq.max()) for _a in ax2]
[_a.set_ylim(0, tsys_max) for _a in ax2]
[_a.set_xlabel('Frequency (GHz)') for i, _a in enumerate(ax) if i/4>=(ax_y-1)]
[_a.set_ylabel('Power (dBm)') for i, _a in enumerate(ax) if i%4==0]
[_a.set_yticklabels('') for i, _a in enumerate(ax) if i%4!=0]
[_a.set_ylabel('Tsys (K)') for i, _a in enumerate(ax2) if i%4==3]
[_a.set_yticklabels('') for i, _a in enumerate(ax2) if i%4!=3]
[_a.grid(True) for _a in ax]
fig.savefig(fp('yfactor.results.%s.png'))

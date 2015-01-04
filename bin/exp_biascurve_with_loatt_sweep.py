#! /usr/bin/env python

# configures
# ==========

# default values
# --------------
v_start = 0  # mV
v_stop = 15  # mV
v_step = 0.3 # mV

att_start = 0
att_stop = 4000
att_step = 50

# --

name = 'exp_biasscurve_with_loatt_sweep'


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

desc = 'Sweep SIS bias voltage.'

p = argparse.ArgumentParser(description=desc)
p.add_argument('--att_start', type=int,
               help='Start att. current. default is %d'%(att_start))
p.add_argument('--att_stop', type=float,
               help='Stop att. voltage. default is %d'%(att_stop))
p.add_argument('--att_step', type=float,
               help='Step to sweep att. bias. default is %d'%(att_step))
p.add_argument('--v_start', type=float,
               help='Start SIS voltage in mV. default is %.2f mV'%(v_start))
p.add_argument('--v_stop', type=float,
               help='Stop SIS voltage in mV. default is %.2f mV'%(v_stop))
p.add_argument('--v_step', type=float,
               help='Step to sweep SIS bias in mV. default is %.2f mV'%(v_step))

args = p.parse_args()


# main
# ====

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('FOREST : Bias Sweep with LO Att. sweep')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
forest.print_timestamp()


# create save directory
# ---------------------
fp = forest.filepath_generator(name)
print('INFO: saveto %s'%(fp(' ')))
print('')


# handling args
# -------------
if args.v_start is not None: v_start = args.v_start
if args.v_stop is not None: v_stop = args.v_stop
if args.v_step is not None: v_step = args.v_step
if args.att_start is not None: att_start = args.att_start
if args.att_stop is not None: att_stop = args.att_stop
if args.att_step is not None: att_step = args.att_step

params = 'v_start = %f\n'%(v_start)
params += 'v_stop = %f\n'%(v_stop)
params += 'v_step = %f\n'%(v_step)
params += 'att_start = %f\n'%(att_start)
params += 'att_stop = %f\n'%(att_stop)
params += 'att_step = %f\n'%(att_step)
open(fp('log.params.%s.txt'), 'w').writelines(params)


# open devices
# ------------
print('open devices')
print('============')

print('Bias Box...'),
sys.stdout.flush()
bb = forest.biasbox()
print('')

print('LO Att...'),
sys.stdout.flush()
la = forest.loatt()
print('')

print('')


# init devices
# ------------
print('init devices')
print('============')

print('INFO: SIS bias set to 0 mV.')
bb.bias_set(0)

print('INFO: LO Att. set to 0.')
la.bias_set(0)

print('')


# init data set
# -------------
sweep_data = map(float, numpy.arange(v_start, v_stop+v_step, v_step))
loatt_sweep = numpy.arange(att_start, att_stop+att_step, att_step)

# start experiment
# ----------------
print('start experiment')
print('================')

for att in loatt_sweep:
    print('LO Att. = %d'%(att))
    la.bias_set(att)
    
    # sweep bias
    # - - - - - -
    print('sweep start...')
    v, i = bb.bias_sweep(sweep_data)
    print('done.')
    v = numpy.array(v)
    i = numpy.array(i)
    
    # save data
    # - - - - - 
    print('save data...')
    numpy.save(fp('biassweep.data.%04d'%(att)+'.%s.npy'), (v, i))
    
    # plot data
    # - - - - -
    print('save figure...')
    vv = v.T
    ii = i.T
    
    ch = forest.biasbox_tools.biasbox_ch_mapper()
    
    l_box = ['BOX:%d'%(_i) for _i in ch.box]
    l_ch = ['CH:%d'%(_i) for _i in ch.ch]
    l_beam = ['BEAM:%d'%(_i) for _i in ch.beam]
    l_pol = ['(%s)'%(_i) for _i in ch.pol]
    l_unit = ['UNIT:%d'%(_i) for _i in ch.dsbunit]
    label = ['%s, %s\n%s %s, %s'%(_x, _c, _b, _p, _u) for _x, _c, _b, _p, _u \
             in zip(l_box, l_ch, l_beam, l_pol, l_unit)]
    
    pylab.rcParams['font.size'] = 7
    
    fig = pylab.figure()
    fig.suptitle('Bias Sweep (%s)'%(time.strftime('%Y/%m/%d %H:%M:%S')), fontsize=11)
    ax = [fig.add_subplot(4, 4, j+1) for j in range(16)]
    [_a.plot(_v, _i, '+') for _a, _v, _i in zip(ax, vv, ii)]
    [_a.text(0.08, 0.72, _l, transform=_a.transAxes) for _a, _l in zip(ax, label)]
    [_a.grid(True) for _a in ax]
    [_a.set_xlabel('Bias Voltage (mV)') for _i, _a in enumerate(ax) if _i/4.>=3]
    [_a.set_ylabel('Bias Current (uA)') for _i, _a in enumerate(ax) if _i%4==0]
    fig.savefig(fp('biassweep.fig.%04d'%(att)+'.%s.png'))
    pylab.close(fig)
    print('')
    continue

# finalize devices
# ----------------
print('finalize')
print('========')

print('INFO: SIS bias set to 0 mV.')
bb.bias_set(0)

print('INFO: LO Att. set to 4000.')
la.bias_set(4000)

print('')

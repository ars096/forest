#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'get_SIS_bias_curve_with_LO_att_level_sweep'

description = 'Get SIS bias curve with LO Att level sweep.'


# Default parameters
# ------------------

start = 0  # mA
stop = 20  # mA
step = 0.25 # mA

sis_start = 0  # mV
sis_stop = 15  # mV
sis_step = 0.5 # mV


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--start', type=float,
               help='LO att sweep start current in mA. default is %.2f mA.'%(start))
p.add_argument('--stop', type=float,
               help='LO att sweep stop current in mA. default is %.2f mA.'%(stop))
p.add_argument('--step', type=float,
               help='LO att sweep step current in mA. default is %.2f mA.'%(step))
p.add_argument('--sis_start', type=float,
               help='SIS sweep start voltage in mV. default is %.2f mV.'%(sis_start))
p.add_argument('--sis_stop', type=float,
               help='SIS sweep stop voltage in mV. default is %.2f mV.'%(sis_stop))
p.add_argument('--sis_step', type=float,
               help='SIS sweep step voltage in mV. default is %.2f mV.'%(sis_step))

args = p.parse_args()

if args.start is not None: start = args.start
if args.stop is not None: stop = args.stop
if args.step is not None: step = args.step
if args.sis_start is not None: start = args.sis_start
if args.sis_stop is not None: stop = args.sis_stop
if args.sis_step is not None: step = args.sis_step


# Run Script
# ==========

import forest.script

script = forest.script.get_sis_bias_curve_with_LO_att_level_sweep()
script.run(start, stop, step, sis_start, sis_stop, sis_step)



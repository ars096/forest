#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'rsky_with_lo_att_sweep'

description = 'R-SKY with LO Att Sweep.'


# Default parameters
# ------------------

start = 5
stop = 25
step = 0.2
Thot = 293.0 # K
if_freq = 8

# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--start', type=float,
               help='Sweep start Att level in mA. default is %.2f mA.'%(start))
p.add_argument('--stop', type=float,
               help='Sweep stop Att level in mA. default is %.2f mA.'%(stop))
p.add_argument('--step', type=float,
               help='Step of sweep Att level in mA. default is %.2f mA.'%(step))
p.add_argument('--Thot', type=float,
               help='Hot temperature in K. default is %.2f K.'%(Thot))
p.add_argument('--if_freq', type=float,
               help='IF freq. to be evaruated. default is %.2f GHz.'%(if_freq))

args = p.parse_args()

if args.start is not None: start = args.start
if args.stop is not None: stop = args.stop
if args.step is not None: step = args.step
if args.Thot is not None: Thot = args.Thot
if args.if_freq is not None: if_freq = args.if_freq


# Run Script
# ==========

import forest.script

script = forest.script.rsky_with_lo_att_sweep()
script.run(start, stop, step, Thot, if_freq)



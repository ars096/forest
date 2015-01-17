#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'rsky_with_sis_bias_sweep'

description = 'R-SKY with SIS Bias Sweep.'


# Default parameters
# ------------------

start = 7.0  # mV
stop = 11.0  # mV
step = 0.2  # mV

Thot = 293.0 # K


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--start', type=float,
               help='Start voltage in mV. default is %.2f mV.'%(start))
p.add_argument('--stop', type=float,
               help='Stop voltage in mV. default is %.2f mV.'%(stop))
p.add_argument('--step', type=float,
               help='Step of each bias voltage in mV. default is %.2f mV.'%(step))
p.add_argument('--Thot', type=float,
               help='Hot temperature in K. default is %.2f K.'%(Thot))

args = p.parse_args()

if args.start is not None: start = args.start
if args.stop is not None: stop = args.stop
if args.step is not None: step = args.step
if args.Thot is not None: Thot = args.Thot


# Run Script
# ==========

import forest.script

script = forest.script.rsky_with_sis_bias_sweep()
script.run(start, stop, step, Thot)



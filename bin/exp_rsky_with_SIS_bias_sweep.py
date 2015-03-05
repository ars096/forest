#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'rsky_with_sis_bias_sweep'

description = 'R-SKY with SIS Bias Sweep.'


# Default parameters
# ------------------

step = 0.05 # mV
Thot = 293.0 # K

tsys_min = 100  # K
tsys_max = 500  # K

if_freq = 8


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--step', type=float,
               help='Step of sweep interval in mV. default is %.2f mV.'%(step))
p.add_argument('--Thot', type=float,
               help='Hot temperature in K. default is %.2f K.'%(Thot))
p.add_argument('--Tsys_min', type=float,
               help='Minimum Tsys value in color map. default is %.2f K.'%(tsys_min))
p.add_argument('--Tsys_max', type=float,
               help='Maximum Tsys value in color map. default is %.2f K.'%(tsys_max))
p.add_argument('--if_freq', type=float,
               help='IF freq. to be evaruated. default is %.2f GHz.'%(if_freq))

args = p.parse_args()
if args.step is not None: step = args.step
if args.Thot is not None: Thot = args.Thot
if args.Tsys_min is not None: tsys_min = args.Tsys_min
if args.Tsys_max is not None: tsys_max = args.Tsys_max
if args.if_freq is not None: if_freq = args.if_freq


# Run Script
# ==========

import forest.script

script = forest.script.rsky_with_sis_bias_sweep()
script.run(step, Thot, tsys_min, tsys_max, if_freq)



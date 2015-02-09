#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'irr_with_if_freq_sweep'

description = 'IRR with IF Freq Sweep.'


# Default parameters
# ------------------

lo_freq = 105
start = 5
stop = 10
step = 1
Thot = 293.0 # K


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--lo_freq', type=str,
               help='LO freq in GHz. default is %.1f GHz.'%(lo_freq))
p.add_argument('--start', type=float,
               help='Start IF freq in GHz. default is %.2f GHz.'%(start))
p.add_argument('--stop', type=float,
               help='Stop IF freq in GHz. default is %.2f GHz.'%(stop))
p.add_argument('--step', type=float,
               help='Step of IF freq in GHz. default is %.2f GHz.'%(step))
p.add_argument('--Thot', type=float,
               help='Hot temperature in K. default is %.2f K.'%(Thot))

args = p.parse_args()

if args.lo_freq is not None: lo_freq = args.lo_freq
if args.start is not None: start = args.start
if args.stop is not None: stop = args.stop
if args.step is not None: step = args.step
if args.Thot is not None: Thot = args.Thot


# Run Script
# ==========

import forest.script

script = forest.script.irr_with_if_freq_sweep()
script.run(lo_freq, start, stop, step, Thot)



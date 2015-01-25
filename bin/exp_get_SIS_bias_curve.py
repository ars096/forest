#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'get_SIS_bias_curve'

description = 'Get SIS bias curve.'


# Default parameters
# ------------------

start = 0  # mV
stop = 15  # mV
step = 0.1 # mV


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

args = p.parse_args()

if args.start is not None: start = args.start
if args.stop is not None: stop = args.stop
if args.step is not None: step = args.step


# Run Script
# ==========

import forest.script

script = forest.script.get_sis_bias_curve()
script.run(start, stop, step)



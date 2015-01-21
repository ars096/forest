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


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--step', type=float,
               help='Step of sweep interval in mV. default is %.2f mV.'%(step))
p.add_argument('--Thot', type=float,
               help='Hot temperature in K. default is %.2f K.'%(Thot))

args = p.parse_args()
if args.step is not None: step = args.step
if args.Thot is not None: Thot = args.Thot


# Run Script
# ==========

import forest.script

script = forest.script.rsky_with_sis_bias_sweep()
script.run(step, Thot)



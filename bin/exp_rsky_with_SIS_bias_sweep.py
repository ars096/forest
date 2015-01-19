#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'rsky_with_sis_bias_sweep'

description = 'R-SKY with SIS Bias Sweep.'


# Default parameters
# ------------------

Thot = 293.0 # K


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--Thot', type=float,
               help='Hot temperature in K. default is %.2f K.'%(Thot))

args = p.parse_args()

if args.Thot is not None: Thot = args.Thot


# Run Script
# ==========

import forest.script

script = forest.script.rsky_with_sis_bias_sweep()
script.run(Thot)



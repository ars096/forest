#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'LO_power_set'

description = 'Set 1st LO SGs output powers.'


# Default parameters
# ------------------

power = -130.0


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--power', type=float,
               help='Output power to be set. default is %f.'%(power))

args = p.parse_args()

if args.power is not None: power = args.power


# Run Script
# ==========

import forest.script

script = forest.script.lo_power_set()
script.run(power)




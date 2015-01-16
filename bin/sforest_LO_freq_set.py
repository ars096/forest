#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'LO_freq_set'

description = 'Set 1st LO SGs frequencies.'


# Default parameters
# ------------------

freq = 10.0
unit = 'GHz'

unit_list = ['GHz', 'MHz', 'kHz', 'Hz']


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--freq', type=float,
               help='Frequency to be set. default is %f.'%(freq))
p.add_argument('--unit', type=str,
               help='Unit of the freq. Select from %s. default is %s.'%(
                   str(unit_list), unit))

args = p.parse_args()

if args.freq is not None: freq = args.freq
if args.unit is not None: unit = args.unit


# Run Script
# ==========

import forest.script

script = forest.script.lo_freq_set()
script.run(freq, unit)




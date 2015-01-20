#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'sis_tune'

description = 'Tuning SIS receivers.'


# Default parameters
# ------------------

LO_freq = 105 # GHz


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--LO_freq', type=float,
               help='LO frequency to tune in GHz. default is %.2f GHz.'%(LO_freq))

args = p.parse_args()

if args.LO_freq is not None: LO_freq = args.LO_freq


# Run Script
# ==========

import forest.script

script = forest.script.sis_tune()
script.run(LO_freq)



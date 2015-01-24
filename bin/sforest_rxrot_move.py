#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'rxrot_move'

description = 'Move Rx rotator to target position.'


# Default parameters
# ------------------

target = 0.0 # deg


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--target', type=float,
               help='Target to be moved. default is %.2f deg.'%(target))

args = p.parse_args()

if args.target is not None: target = args.target


# Run Script
# ==========

import forest.script

script = forest.script.rxrot_move()
script.run(target)




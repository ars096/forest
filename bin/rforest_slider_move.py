#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'slider_move'

description = 'Move slider to the target point.'


# Default parameters
# ------------------

target = 0


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--target', type=float,
               help='Target to be moved. default is %d.'%(target))

args = p.parse_args()

if args.target is not None: target = args.target


# Run Script
# ==========

import forest.script

script = forest.script.slider_move()
script.run(target)




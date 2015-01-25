#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'sis_tune_show_params'

description = 'Show SIS tuning parameters.'


# Default parameters
# ------------------

name = '105'


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--name', type=str,
               help='Name of tuning parameter set. default is %s.'%(name))

args = p.parse_args()

if args.bane is not None: name = args.name


# Run Script
# ==========

import forest.script

script = forest.script.sis_tune_show_params()
script.run(name)



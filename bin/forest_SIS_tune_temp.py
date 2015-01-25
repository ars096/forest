#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'sis_tune_temp'

description = 'Tuning SIS receivers.'


# Default parameters
# ------------------

path = ''


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('path', type=str,
               help='Filepath to the .cnf file.')

args = p.parse_args()

if args.path is not None: path = args.path


# Run Script
# ==========

import forest.script

script = forest.script.sis_tune_temp()
script.run(path)



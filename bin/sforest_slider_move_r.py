#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'slider_move_R'

description = 'Move slider to R position.'


# Default parameters
# ------------------

#
# No parameters are available in forest_initialize.
#


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)

args = p.parse_args()


# Run Script
# ==========

import forest.script

script = forest.script.slider_move_r()
script.run()




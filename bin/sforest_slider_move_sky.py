#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'slider_move_SKY'

description = 'Move slider to SKY position.'


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

script = forest.script.slider_move_sky()
script.run()




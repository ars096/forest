#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'sis_tune_show_availables'

description = 'Show SIS tuning available configurations.'


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

script = forest.script.sis_tune_show_availables()
script.run()



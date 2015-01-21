#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'check_LO_SG'

description = 'Check 1st LO SGs status.'


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

script = forest.script.lo_sg_check()
script.run()




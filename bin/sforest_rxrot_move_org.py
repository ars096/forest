#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'rxrot_move_org'

description = 'Move Rx rotator to ORG position.'


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

script = forest.script.rxrot_move_org()
script.run()




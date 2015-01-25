#! /usr/bin/env python


# Configurations
# ==============

# Script information
# ------------------

name = 'initialize'

description = 'Initialize FOREST receiver system.'


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

script = forest.script.initialize()
script.run()

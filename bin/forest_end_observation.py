#! /usr/bin/env python


# Configurations
# ==============

# Script information
# ------------------

name = 'end_observation'

description = 'End COSMOS observation mode.'


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

script = forest.script.end_observation()
script.run()

#! /usr/bin/env python


# Configurations
# ==============

# Script information
# ------------------

name = 'start_observation'

description = 'Start COSMOS observation mode.'


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

script = forest.script.start_observation()
script.run()

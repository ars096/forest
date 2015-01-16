#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'slider_move_ORG'

description = 'Move slider to ORG position.' +\
              'If the alarm is raised, clear it before moving.'


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

script = forest.script.slidet_move_org()
script.run()




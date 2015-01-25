#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'SIS_bias_set'

description = 'Set SIS bias.'


# Default parameters
# ------------------

bias = 0.0
beam = 'ALL'
pol = 'ALL'
unit = 'ALL'

beam_list = ['ALL', 1, 2, 3, 4]
pol_list = ['ALL', 'H', 'V']
unit_list = ['ALL', 1, 2]


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--bias', type=float,
               help='Bias voltage to be set. default is %f mV.'%(bias))
p.add_argument('--beam',
               help='Beam number. Select from %s. default is %s.'%(
                   str(beam_list), beam))
p.add_argument('--pol', type=str,
               help='Polarization. Select from %s. default is %s.'%(
                   str(pol_list), pol))
p.add_argument('--unit', type=str,
               help='Unit number. Select from %s. default is %s.'%(
                   str(unit_list), unit))

args = p.parse_args()

if args.bias is not None: bias = args.bias
if args.beam is not None: beam = args.beam
if args.pol is not None: pol = args.pol
if args.unit is not None: unit = args.unit


if beam == 'ALL': beam = None
else: beam = int(beam)

if pol == 'ALL': pol = None

if unit == 'ALL': unit =None
else: unit = int(unit)


# Run Script
# ==========

import forest.script

script = forest.script.sis_bias_set()
script.run(bias, beam, pol, unit)




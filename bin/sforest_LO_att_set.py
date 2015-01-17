#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'LO_att_set'

description = 'Set 1st LO attenuator levels.'


# Default parameters
# ------------------

bias = 200.0
beam = 'ALL'
pol = 'ALL'

beam_list = ['ALL', 1, 2, 3, 4]
pol_list = ['ALL', 'H', 'V']


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--bias', type=float,
               help='Bias current to be set. default is %f mA.'%(bias))
p.add_argument('--beam',
               help='Beam number. Select from %s. default is %s.'%(
                   str(beam_list), beam))
p.add_argument('--pol', type=str,
               help='Polarization. Select from %s. default is %s.'%(
                   str(pol_list), pol))

args = p.parse_args()

if args.bias is not None: bias = args.bias
if args.beam is not None: beam = args.beam
if args.pol is not None: pol = args.pol


if beam == 'ALL': beam = None
else: beam = int(beam)

if pol == 'ALL': pol = None


# Run Script
# ==========

import forest.script

script = forest.script.lo_att_set()
script.run(bias, beam, pol)




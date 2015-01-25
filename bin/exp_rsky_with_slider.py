#! /usr/bin/env python

# Configurations
# ==============

# Script information
# ------------------

name = 'rsky_with_slider'

description = 'R-SKY with slider.'


# Default parameters
# ------------------

start = 4.0  # GHz
stop = 12.0  # GHz
resbw = 3.0  # MHz
average = 5
Thot = 293.0 # K


# Argument Parser
# ===============

import argparse

p = argparse.ArgumentParser(description=description)
p.add_argument('--start', type=float,
               help='Start frequency in GHz. default is %.2f GHz.'%(start))
p.add_argument('--stop', type=float,
               help='Stop frequency in GHz. default is %.2f GHz.'%(stop))
p.add_argument('--resbw', type=float,
               help='Res. BW in MHz. default is %.2f MHz.'%(resbw))
p.add_argument('--average', type=float,
               help='Average num. default is %d.'%(average))
p.add_argument('--Thot', type=float,
               help='Hot temperature in K. default is %.2f K.'%(Thot))

args = p.parse_args()

if args.start is not None: start = args.start
if args.stop is not None: stop = args.stop
if args.resbw is not None: resbw = args.resbw
if args.average is not None: average = args.average
if args.Thot is not None: Thot = args.Thot


# Run Script
# ==========

import forest.script

script = forest.script.rsky_with_slider()
script.run(start, stop, resbw, average, Thot)



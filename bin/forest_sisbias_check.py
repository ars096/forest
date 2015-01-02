#! /usr/bin/env python

# configures
# ==========



# import
# ======

import sys
import argparse
import forest


# argparse configure
# ==================

desc = 'Check SIS biases.'

p = argparse.ArgumentParser(description=desc)

args = p.parse_args()


# main
# ====

print('~~~~~~~~~~~~~~~~~~~~~~~')
print('FOREST : SIS Bias Check')
print('~~~~~~~~~~~~~~~~~~~~~~~')
forest.print_timestamp()
print('')

print('opening ...'),
sys.stdout.flush()
biasbox = forest.biasbox()
print('OK')

print('checking biases ...'),
sys.stdout.flush()
sisbias = biasbox.bias_get()
print('OK')

print('')

print('*** Results ***')
forest.print_bias(sisbias) 


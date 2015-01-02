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

desc = 'Shutdown FOREST receiver.'

p = argparse.ArgumentParser(description=desc)

args = p.parse_args()


# main
# ====

print('~~~~~~~~~~~~~~~~~')
print('FOREST : Finalize')
print('~~~~~~~~~~~~~~~~~')
forest.print_timestamp()
print('')

# biasbox
# -------
print('SIS Bias Box')
print('============')
print('opening ...'),
sys.stdout.flush()
biasbox = forest.biasbox()
print('OK')
print('set 0 mV ...'),
sys.stdout.flush()
biasbox.bias_set(0)
print('OK')

print('*** Results ***')
sisbias = biasbox.bias_get()
forest.print_bias(sisbias) 

# 
# 

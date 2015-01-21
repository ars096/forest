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

desc = 'Check LO Att. biases.'

p = argparse.ArgumentParser(description=desc)

args = p.parse_args()


# main
# ====

print('~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('FOREST : LO Att Bias Check')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~')
forest.print_timestamp()
print('')

print('opening ...'),
sys.stdout.flush()
loatt = forest.loatt()
print('OK')

print('checking biases ...'),
sys.stdout.flush()
loattbias = loatt.bias_get()
print('OK')

print('')

print('*** Results ***')
forest.print_loatt(loattbias) 


#! /usr/bin/env python

import forest

print('=================')
print('FOREST : Finalize')
print('=================')
forest.print_timestamp()
print('')

# biasbox
# -------
print('SIS Bias Box ...'),
biasbox = forest.biasbox()
biasbox.bias_set(0)
print(' OFF')
sisbias = biasbox.bias_get()
forest.print_bias(sisbias) 

# 
# 

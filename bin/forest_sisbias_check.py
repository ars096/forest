#! /usr/bin/env python

import forest

print('=======================')
print('FOREST : SIS Bias Check')
print('=======================')
forest.print_timestamp()
print('')

biasbox = forest.biasbox()
sisbias = biasbox.bias_get()
forest.print_bias(sisbias) 


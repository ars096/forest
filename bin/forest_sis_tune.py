#! /usr/bin/env python

# configures
# ==========

config_file_name = 'FOREST2014.cnf'

# --

config_file_dir = '/home/forest/tuning_parameters'
mixer_data_dir = 'mixer_unit_data'


# import
# ======

import os
import sys
import argparse
import ConfigParser
import forest


# argparse configure
# ==================

desc = 'Set SIS bias and LO Att. to tune the mixers.'

p = argparse.ArgumentParser(description=desc)
p.add_argument('lo_freq', type=int, help='LO frequency to tune.')

args = p.parse_args()


# main
# ====

print('~~~~~~~~~~~~~~~~~~~~~~~~')
print('FOREST : Tune SIS mixers')
print('~~~~~~~~~~~~~~~~~~~~~~~~')
forest.print_timestamp()
print('')

print('INFO: Tune to LO_Freq. = %d GHz.'%(args.lo_freq))
print('')


# read config files
# -----------------
confpath = os.path.join(config_file_dir, config_file_name)

conf = ConfigParser.SafeConfigParser()
conf.read(confpath)

params = {}

print('Parameters')
print('==========')

for unit in conf.options('combination'):
    unitname = conf.get('combination', unit)
    unitconfpath = os.path.join(config_file_dir, mixer_data_dir, 
                                unitname+'.cnf')
    unitconf = ConfigParser.SafeConfigParser()
    unitconf.read(unitconfpath)
    
    section = '%d GHz'%(args.lo_freq)
    if not unitconf.has_section(section):
        print('WARN: %s has no parameters for %d GHz.'%(unitname, args.lo_freq))
        print('WARN: Use default parameters.')
        lo_freq_str = unitconf.get('info', 'default')
        try:
            lo_freq = int(lo_freq_str.strip(' GHZghz_-'))
        except ValueError, e:
            raise('ERROR: %s.info.default is wrong. (%s)'%(unitname, 
                                                           lo_freq_str))
        print('WARN: Default is LO_Freq. = %d GHz.'%(lo_freq))
        section = '%d GHz'%(lo_freq)
        if not unitconf.has_section(section):
            raise('ERROR: %s has no parameters for %d GHz.'%(unitname, lo_freq))
        pass
    
    bias1 = float(unitconf.get(section, 'bias1'))
    bias2 = float(unitconf.get(section, 'bias2'))
    lo_att = float(unitconf.get(section, 'lo_att'))
    
    print('%s: bias1 = %f,  bias2 = %f,  lo_att = %f'%(unit, bias1, bias2,
                                                       lo_att))
    params[unit] = {'bias1': bias1, 'bias2': bias2, 'lo_att': lo_att}
    continue

print('')


# set tuning parameters
# ---------------------

print('open devices')
print('============')

print('biasbox...'),
sys.stdout.flush()
biasbox = forest.biasbox()
print('')

print('lo_att...'),
sys.stdout.flush()
loatt = forest.lo_att()
print('')

print('')

unitlist = ['beam1_hpol', 'beam1_vpol', 'beam2_hpol', 'beam2_vpol', 
            'beam3_hpol', 'beam3_vpol', 'beam4_hpol', 'beam4_vpol']

print('set parameters')
print('==============')

for unit in unitlist:
    print(unit+','), 
    sys.stdout.flush()
    p = params[unit]
    beam = int(unit.strip('beam_hvpol'))
    pol = unit.strip('beam1234_pol').upper()
    
    biasbox.bias_set(p['bias1'], beam=beam, pol=pol, dsbunit=1)
    biasbox.bias_set(p['bias2'], beam=beam, pol=pol, dsbunit=2)
    loatt.bias_set(p['lo_att'], beam=beam, pol=pol)
    continue

print('done.')
print('')


# Show results
# ------------

print('Results')
print('=======')

bias_results = biasbox.bias_get()
print('Bias Box')
print('--------')
forest.print_bias(bias_results) 

print('LO Att.')
print('-------')
print('(soon...)')
print('\n\n')
# loatt_results = loatt.bias_get()
# forest.print_loatt(loatt_results)

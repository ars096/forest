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

print('========================')
print('FOREST : Tune SIS mixers')
print('========================')
forest.print_timestamp()
print('')

print('INFO: Tune to LO_Freq. = %d GHz.')
print('')


# read config files
# -----------------
confpath = os.path.join(config_file_dir, config_file_name)

conf = ConfigParser.SafeConfigParser()
conf.read(confpath)

params = {}

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
    
    bias1 = unitconf.get(section, 'bias1')
    bias2 = unitconf.get(section, 'bias2')
    lo_att = unitconf.get(section, 'lo_att')
    
    params[unit] = {'bias1': bias1, 'bias2': bias2, 'lo_att': lo_att}
    continue
        

# set tuning parameters
# ---------------------
biasbox = forest.biasbox()
loatt = forest.lo_att()

unitlist = ['beam1_hpol', 'beam1_vpol', 'beam2_hpol', 'beam2_vpol', 
            'beam3_hpol', 'beam3_vpol', 'beam4_hpol', 'beam4_vpol']

for unit in unitlist:
    p = params[unit]
    beam = int(unit.strip('beam_hvpol'))
    pol = unit.strip('beam1234_pol').upper()
    
    biasbox.bias_set(p['bias1'], beam=beam, pol=pol, dsbunit=1)
    biasbox.bias_set(p['bias2'], beam=beam, pol=pol, dsbunit=2)
    loatt.bias_set(p['lo_att'], beam=beam, pol=pol)
    continue


bias_results = biasbox.bias_get()
forest.print_bias(bias_results) 

# loatt_results = loatt.bias_get()
# forest.print_loatt(loatt_results)

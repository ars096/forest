
import os
import time
import numpy
import ConfigParser
import forest

def mkdirs(path):
    if os.path.exists(path): return False
    print('mkdir %s'%(path))
    os.makedirs(path)
    return path


def filepath_generator(name):
    fdir = '/home/forest/data'
    ts = time.strftime('%Y%m%d_%H%M%S')
    savedir = os.path.join(fdir, name, ts)
    mkdirs(savedir)
    def filepath(fname):
        if fname.find('%s')!=-1: fname = fname%(ts)
        return os.path.join(savedir, fname)
    return filepath


def load_sis_config(name, config_file_name='FOREST2014.cnf'):
    config_file_dir = '/home/forest/tuning_parameters'
    mixer_data_dir = 'mixer_unit_data'
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
        
        section = name
        if not unitconf.has_section(section):
            print('WARN: %s has no parameters named %s.'%(unitname, name))
            name = unitconf.get('info', 'default')
            print('WARN: Use default parameters %s.'%(name))
            section = name
            if not unitconf.has_section(section):
                raise('ERROR: %s has no parameters named %s.'%(unitname, section))
            pass
        
        if not unitconf.has_option(section, 'use'):
            section = unitconf.get(section, 'use')
            pass
        
        bias1 = float(unitconf.get(section, 'bias1'))
        bias2 = float(unitconf.get(section, 'bias2'))
        lo_att = float(unitconf.get(section, 'lo_att'))
        j_type = unitconf.get('info', 'L_sis_id').split('-')[2]
        beam = int(unit.strip('Bbeam_HVhvpol'))
        pol = unit.strip('Bbeam1234_pol')
                
        #print('%s: bias1 = %f,  bias2 = %f,  lo_att = %f'%(unit, bias1, bias2,
        #                                                   lo_att))
        params[unit] = {'bias1': bias1, 'bias2': bias2, 'lo_att': lo_att,
                        'J-type': j_type, 'beam': beam, 'pol': pol.upper()}
        continue
        
    return params

def load_tuning_available(config_file_name='FOREST2014.cnf'):
    config_file_dir = '/home/forest/tuning_parameters'
    mixer_data_dir = 'mixer_unit_data'
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
        
        sections = unitconf.sections()
        availables = [_sec for _sec in sections if _sec!='info']
        
        params[unit] = sorted(availables)
        continue
        
    return params



def is_operating():
    db = forest.db_writer('operation_log')
    ret = db.get_latest_item()
    status = ret[2]
    if is_observing(): return True
    if status == 'START': return True
    return False

def is_observing():
    db = forest.db_writer('operation_log')
    ret = db.get_latest_item()
    status = ret[3]
    if status == 'observation_mode': return True
    return False


# print methods
# -------------
def print_timestamp():
    msg = time.strftime('%Y/%m/%d %H:%M:%S')
    print('Timestamp: %s'%(msg))
    return
    
def print_bias(bias):
    v = bias[0]
    i = bias[1]
     
    v1 = 'V(mV): ' + ', '.join(['%5.2f'%_v for _v in v[:8]]) + '\n'
    v2 = 'V(mV): ' + ', '.join(['%5.2f'%_v for _v in v[8:]]) + '\n'
    i1 = 'I(uA): ' + ', '.join(['%5.1f'%_i for _i in i[:8]]) + '\n'
    i2 = 'I(uA): ' + ', '.join(['%5.1f'%_i for _i in i[8:]]) + '\n'
    sep = '-' * (len(v1)) + '\n'
    
    beam1 = '%5s | %8s %s %8s | %8s %s %8s  |\n'%('', '', 'Beam 1', '', 
                                                  '', 'Beam 2', '')
    beam2 = '%5s | %8s %s %8s | %8s %s %8s  |\n'%('', '', 'Beam 3', '',
                                                  '', 'Beam 4', '')
    
    pol = '%5s |  H-1   H-2    V-1   V-2  |   H-1   H-2    V-1   V-2  |\n'%('')
    
    msg = ''
    msg += sep
    msg += beam1
    msg += pol
    msg += sep
    msg += v1
    msg += i1
    msg += sep
    #msg += '\n'
    msg += sep
    msg += beam2
    msg += pol
    msg += sep
    msg += v2
    msg += i2
    msg += sep
    
    print(msg)
    return

def print_loatt(bias):
    v = ' ' + ', '.join(['%4d'%_v for _v in bias]) + '\n'
    sep = '-' * (len(v)) + '\n'
    beam = '|         H Pol.        |         V Pol.        |\n'
    pol =  '|   B1   B2   B3   B4   |   B1   B2   B3   B4   |\n'

    msg = ''
    msg += sep
    msg += beam
    msg += pol
    msg += sep
    msg += v
    msg += sep
    
    print(msg)
    return

def print_rxrot(status):
    print(status)
    return

def print_slider(status):
    position, count = status
    print('%s (%d)'%(position, count))
    return

def print_switch(status):
    ch1, ch2, ch3, ch4 = status
    print('ch1: %d, ch2: %d, ch3: %d, ch4: %d'%(ch1, ch2, ch3, ch4))
    return

def print_losg(status):
    freq, power, output = status
    print('SG1: %f GHz, %.1f dBm, ON/OFF=%d'%(freq[0]/1e9, power[0], output[0]))
    print('SG2: %f GHz, %.1f dBm, ON/OFF=%d'%(freq[1]/1e9, power[1], output[1]))
    return

def print_spana(status):
    av = numpy.average(status, axis=1)
    print('Sp1: %.1f dBm,  Sp2: %.1f dBm'%(av[0], av[1]))
    print('Sp3: %.1f dBm,  Sp4: %.1f dBm'%(av[2], av[3]))
    return

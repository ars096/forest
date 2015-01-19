
import os
import time
import ConfigParser

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


def load_sis_config(lo_freq, config_file_name='FOREST2014.cnf'):
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
        
        section = '%d GHz'%(lo_freq)
        if not unitconf.has_section(section):
            print('WARN: %s has no parameters for %d GHz.'%(unitname, lo_freq))
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
        j_type = unitconf.get('info', 'L_sis_id').split('-')[2]
        
        print('%s: bias1 = %f,  bias2 = %f,  lo_att = %f'%(unit, bias1, bias2,
                                                           lo_att))
        params[unit] = {'bias1': bias1, 'bias2': bias2, 'lo_att': lo_att, 'J-type': j_type}
        continue
        
    return params




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

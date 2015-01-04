
import os
import time

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
    beam = '|   Beam 1  |   Beam 2  |   Beam 3  |   Beam 4  |\n'
    pol =  '|   H   V   |   H   V   |   H   V   |   H   V   |\n'

    msg = ''
    msg += sep
    msg += beam
    msg += pol
    msg += sep
    msg += v
    msg += sep
    
    print(msg)
    return



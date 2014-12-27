
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
        if fname.find('%s'): fname = fname%(ts)
        return os.path.join(savedir, fname)
    return filepath



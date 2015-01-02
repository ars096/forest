#! /usr/bin/env python

import os
import sys
import urllib2

print('==============')
print('update_scripts')
print('==============')
print('')

# Initialize
# ==========
print('directories check')
print('=================')

# Create directories
# ------------------
def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print('mkdir %s'%(path))
        pass
    return

mkdir('/home/forest/git')
mkdir('/home/forest/python')
mkdir('/home/forest/bin')
mkdir('/home/forest/database')
mkdir('/home/forest/database/scripts')
mkdir('/home/forest/data')
mkdir('/home/forest/tuning_parameters')
mkdir('/home/forest/tuning_parameters/mixer_unit_data')

print('>>> OK')
print('')


# Download Latest Python Modules
# ===============================
print('download latest files')
print('=====================')

print('checking the Internet connection...'),

if sys.argv[-1]!='-skip':    
    try:
        urllib2.urlopen('http://www.google.com/', timeout=2)
        
        print(' OK')
        print('')
        
        # forest
        # ------
        print('checking forest tools...')
        print('------------------------')
        if not os.path.exists('/home/forest/git/forest'):
            os.system('git clone https://github.com/ars096/forest.git /home/forest/git/forest/')
        else:
            os.chdir('/home/forest/git/forest')
            os.system('git pull')
            pass
        print('')
        
        # pymeasure2
        # ----------
        print('checking pymeasure2 module...')
        print('-----------------------------')
        if not os.path.exists('/home/forest/git/pymeasure2'):
            os.system('git clone https://github.com/ars096/pymeasure2.git /home/forest/git/pymeasure2/')
        else:
            os.chdir('/home/forest/git/pymeasure2')
            os.system('git pull')
            pass
        print('')
        
        # pyinterface
        # -----------
        print('checking pyinterface module...')
        print('------------------------------')
        if not os.path.exists('/home/forest/git/pyinterface'):
            os.system('git clone https://github.com/ars096/pyinterface.git /home/forest/git/pyinterface/')
        else:
            os.chdir('/home/forest/git/pyinterface')
            os.system('git pull')
            pass
        print('')
        
    except:
        print(' NG')
        print('>> MODE: off-line')
        print('')
        pass
else:
    print('passed')
    print('')
    pass
    

# Update Modules and Scripts
# ==========================
print('overwrite files')
print('===============')

# forest
# ------
print('forest...')
os.system('cp -r /home/forest/git/forest/forest /home/forest/python/')
os.system('cp /home/forest/git/forest/bin/* /home/forest/bin/')
os.system('cp /home/forest/git/forest/database_scripts/* /home/forest/database/scripts/')
os.system('chmod 755 /home/forest/bin/*')
os.system('chmod 755 /home/forest/database/scripts/*')

# pymeasure2
# ----------
print('pymeasure2...')
os.system('cp -r /home/forest/git/pymeasure2/pymeasure /home/forest/python/')

# pyinterface
# -----------
print('pyinterface...')
os.system('cp -r /home/forest/git/pyinterface/pyinterface /home/forest/python/')

# tuning parameters
# -----------------
print('tuning_parameters...')
os.system('cp -r /home/forest/git/forest/tuning_parameters /home/forest/tuning_parameters/')


print('')
print('done.')

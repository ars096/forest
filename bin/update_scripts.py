#! /usr/bin/env python

import os
import urllib2

print('==============')
print('update_scripts')
print('==============')


# Initialize
# ==========
print('directories check')
print('=================')

# Create directories
# ------------------
if not os.path.exists('/home/forest/git'): os.mkdir('/home/forest/git')
if not os.path.exists('/home/forest/python'): os.mkdir('/home/forest/python')
if not os.path.exists('/home/forest/bin'): os.mkdir('/home/forest/bin')
if not os.path.exists('/home/forest/database'): os.mkdir('/home/forest/database')
if not os.path.exists('/home/forest/database/scripts'): os.mkdir('/home/forest/database/scripts')
if not os.path.exists('/home/forest/data'): os.mkdir('/home/forest/data')

print('>>> OK')
print('')


# Download Latest Python Modules
# ===============================
print('download latest files')
print('=====================')

print('checking the Internet connection...'),
try:
    urllib2.urlopen('http://www.google.com/', timeout=3)
    
    print(' OK')
    
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


print('')
print('done.')

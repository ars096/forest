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
if not os.path.exists('/home/forestroot/git'): os.mkdir('/home/forestroot/git')
if not os.path.exists('/home/forestroot/python'): os.mkdir('/home/forestroot/python')
if not os.path.exists('/home/forestroot/bin'): os.mkdir('/home/forestroot/bin')

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
        if not os.path.exists('/home/forestroot/git/forest'):
            os.system('git clone https://github.com/ars096/forest.git /home/forestroot/git/forest/')
        else:
            os.chdir('/home/forestroot/git/forest')
            os.system('git pull')
            pass
        print('')
            
        # pymeasure2
        # ----------
        print('checking pymeasure2 module...')
        print('-----------------------------')
        if not os.path.exists('/home/forestroot/git/pymeasure2'):
            os.system('git clone https://github.com/ars096/pymeasure2.git /home/forestroot/git/pymeasure2/')
        else:
            os.chdir('/home/forestroot/git/pymeasure2')
            os.system('git pull')
            pass
        print('')
        
        # pyinterface
        # -----------
        print('checking pyinterface module...')
        print('------------------------------')
        if not os.path.exists('/home/forestroot/git/pyinterface'):
            os.system('git clone https://github.com/ars096/pyinterface.git /home/forestroot/git/pyinterface/')
        else:
            os.chdir('/home/forestroot/git/pyinterface')
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
os.system('cp -r /home/forestroot/git/forest/forest /home/forestroot/python/')
os.system('cp /home/forestroot/git/forest/bin_fac/* /home/forestroot/bin/')
os.system('chmod 755 /home/forestroot/bin/*')

# pymeasure2
# ----------
print('pymeasure2...')
os.system('cp -r /home/forestroot/git/pymeasure2/pymeasure /home/forestroot/python/')

# pyinterface
# -----------
print('pyinterface...')
os.system('cp -r /home/forestroot/git/pyinterface/pyinterface /home/forestroot/python/')


print('')
print('done.')

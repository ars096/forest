#! /usr/bin/env python

import os
import shutil

# Initialize
# ==========

# Create directories
# ------------------
if not os.path.exists('~/git'): os.mkdir('~/git')
if not os.path.exists('~/python'): os.mkdir('~/python')
if not os.path.exists('~/bin'): os.mkdir('~/bin')
if not os.path.exists('~/database'): os.mkdir('~/database')
if not os.path.exists('~/database/scripts'): os.mkdir('~/database/scripts')
if not os.path.exists('~/data'): os.mkdir('~/data')


# Download Latest Python Modules
# ===============================

# forest
# ------
if not os.path.exists('~/git/forest'):
    os.system('git clone https://github.com/ars096/forest.git ~/git/forest/')
else:
    os.chdir('~/git/forest')
    os.system('git pull')
    pass

# pymeasure2
# ----------
if not os.path.exists('~/git/pymeasure2'):
    os.system('git clone https://github.com/ars096/pymeasure2.git ~/git/pymeasure2/')
else:
    os.chdir('~/git/pymeasure2')
    os.system('git pull')
    pass

# pyinterface
# -----------
if not os.path.exists('~/git/pyinterface'):
    os.system('git clone https://github.com/ars096/pyinterface.git ~/git/pyinterface/')
else:
    os.chdir('~/git/pyinterface')
    os.system('git pull')
    pass


# Update Modules and Scripts
# ==========================

# forest
# ------
os.system('cp -r ~/git/forest/forest ~/python/')
os.system('cp ~/git/forest/bin/* ~/bin/')
os.system('cp ~/git/forest/database_scripts/* ~/database/scripts/')
os.system('chmod 755 ~/bin/*')

# pymeasure2
# ----------
os.system('cp -r ~/git/pymeasure2/pymeasure ~/python/')

# pyinterface
# -----------
os.system('cp -r ~/git/pyinterface/pyinterface ~/python/')






#!/usr/bin/env python

import os
import shutil
import glob
import re

#dir = './'
dir = './temp/'

###

os.chdir(dir)
files = glob.glob('*processed.root')

for f in files:
    print f

    splitted_filename = f.split('_')
    m = re.findall(r'\d+' ,splitted_filename[0][1:])
    m = m[0]

    # - Format might behave in an unexpected way in python 2.*
    out_file_name = "{0}.root".format( m )
    print(out_file_name)
    shutil.move(f , out_file_name)

#for f in glob.glob('*Hhhbbtautau*'):
#
#    mH = re.findall(r'\d+' , f)
#
#    out_file_name = 'Hhhbbtautau{}.root'.format(mH[0])
#    shutil.move(f , out_file_name)

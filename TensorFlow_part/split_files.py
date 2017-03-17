# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 19:35:27 2017
@author: thomas

Transform big files in smaller ones.
"""
from __future__ import print_function
import os


start_directory = "/home/thomas/Documents/PAr/zzModel1/data"
filename = "005.txt"

end_directory = "/home/thomas/Documents/PAr/zzModel1/data_new"

pas = 5
nb_files = len(f)/pas

def filename(i):
    return "005%06d.txt" % (i,)

# Read filename.
with open(os.path.join(start_directory, filename), 'r') as f:
    f = f.read()    
f = f.split('\n+++$+++\n')

# Write nb_files.
for i in range(nb_files):
    with open(os.path.join(end_directory, filename(i)), 'w') as new_f:
        text = "\n+++$+++\n".join(f[i:i+pas])
        new_f.write(text)

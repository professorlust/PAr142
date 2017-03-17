# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 16:53:32 2017

@author: thomas
"""
from __future__ import print_function


import pickle as pk


with open("postag_dict_clean", 'rb') as f:
    postag_dict_clean = pk.load(f)
    print("'postag_dict_clean' loaded.")
    
    
def printt(dictionnary):
    for key, value in dictionnary.iteritems():
        print('{key}, size: {size}, {values}'.format(key=key, 
              size=len(value), values=value[0:4]))

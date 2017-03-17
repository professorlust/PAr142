# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 16:18:47 2017

@author: thomas.

Add the word of the file FILE in a dictionnary. FILE is the output of
the Syntaxnet system (a parsed text file).
"""
from __future__ import print_function
import pickle as pk

FILE = "005.txt"

def printt(dictionnary):
    """Display in a nice manner a dictionnary.
    """
    for key, value in dictionnary.iteritems():
        print('{key}, size: {size}, {values}'.format(key=key, 
              size=len(value), values=value[0:4]))

def main(fil):
    # Load or create a new dictionnary.
    if input('Load old dictionnary ? (1|0)') ==1:
        with open("dic_postag", 'rb') as f:
            dic_postag = pk.load(f)
        print("Loaded.")
    else:
        dic_postag = {}
        print("New dictionnary.")
    
    
    # Add the words in the dictionnary if they are not already here.
    with open(fil, "r") as f:
        data = f.read().split('\n')[0:-1]
        length = len(data)
    
    for count, line in enumerate(data):
        line = line.split(' ')
        for token in line:
            word, postag = token.split('_')[0:2]
    
            if postag not in dic_postag:
                dic_postag[postag] = [word]
            else:
                if word not in dic_postag[postag]:
                    dic_postag[postag].append(word)
        if count%1000 == 0:
            print('{0}/{1}'.format(count, length))
    print("{0}/{0} sentences split.".format(length))
    
    
    # Save or not the dictionnary.
    if input('Save the current dictionnary ? (1|0)') ==1:
        pk.dump(dic_postag, open("dic_postag", "wb"))
        print("Saved.")
    else:
        print("Not saved")
    
    return dic_postag
    

if __name__ == '__main__':
    dic_postag = main(FILE)
    printt(dic_postag)
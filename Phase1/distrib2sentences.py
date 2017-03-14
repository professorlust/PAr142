# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 14:30:11 2017

@author: thomas
"""

from __future__ import print_function
import re
import operator
import pickle as pk
import numpy as np

def initialize():
    """ Return the list of words, whose indexes are their ID.
    """
    # Read and find couples (word ID, word).
    with open('correspondance.tsv', 'r') as f:
        f = f.read() #f = "Word ID\tWord\n1\tfawn\n2\tlocalizes\n3\tanogeissus"
    matches = re.findall('\n(\d+)\t([\'\w]+)', f)
    
    # Cast ID from string to int.
    for i, couple in enumerate(matches):
        matches[i] = (int(couple[0])-1, couple[1])

    # Sort and return list of words.    
    matches.sort(key=operator.itemgetter(0))
    _, list_words = zip(*matches)
    return list_words

def printt(resultat):
    for word, distance in resultat:
        print('Distance {:.6}: {}'.format(distance, word))

def get_distrib_from_file(filename):
    
    with open('scores', 'rb') as f:
        scores = np.abs(pk.load(f))
        scores = scores[0]
        scores = scores.tolist()[0]
        
    list_words_sorted = initialize()
    resultat = zip(list_words_sorted, scores)
    resultat.sort(key=operator.itemgetter(1), reverse=True)
    
    return resultat



with open('word_dict_v2', 'rb') as f:
    word_dict = pk.load(f)

distrib = get_distrib_from_file('scores')

dic_words = {}
count_not_found= 0
for word, proba in distrib:
    if word in word_dict:
        categorie = word_dict[word][0] #Even if several categories are there, I take the first one, arbitrarily.
        if categorie not in dic_words:
            dic_words[categorie] = [(word, proba)]
        else:
            dic_words[categorie].append((word, proba))
    else:
        count_not_found += 1
        print("key {} not found in dictionnary.".format(word))
        
print('not found: {}'.format(count_not_found))
#print(dic_words)

      
for key, value in dic_words.iteritems():    
    value.sort(key = lambda x:x[1]) 
    print(key, value[0:2])
    
dic_desired = {}

s = ['PRP', 'VBD', 'VBG', 'IN', 'DT', 'NN']
for postag in s:
    if postag in dic_desired:
        dic_desired[postag] += 1
    else:
        dic_desired[postag] = 1
        


for categorie, nb_elements in dic_desired.iteritems():
    dic_desired[categorie] = dic_words[categorie][-1-nb_elements:-1]
    

new_s = []
for postag in s:
    word = dic_desired[postag].pop(-1)[0]
    new_s.append(word)

new_s = " ".join(new_s)
print(new_s)




















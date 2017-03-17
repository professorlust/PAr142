# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 16:51:12 2017

@author: thomas
"""

from __future__ import print_function
import re
import operator
import pickle
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


def token_to_ID(list_ID, list_words_sorted):
    """ Convert a list of ID to a list of words.
    """
    list_words = []
    for word in liste:
        list_words.append(list_words_sorted.index(word))

    return list_words


if __name__ == '__main__':
    liste = ['house', 'work', 'state', 'animal']
    print(token_to_ID(liste, list_words_sorted))




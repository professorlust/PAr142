# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 14:35:14 2016

@author: thomas
"""
import pickle as pk


# Load or create a new dictionnary.
if input('Load old dictionnary ? (1|0)') ==1:
    with open("word_dict_v2", 'rb') as f:
        dic_words = pk.load(f)
    print("Loaded.")
else:
    dic_words = {}
    print("New dictionnary.")
    

with open("005.txt", "r") as f:
    data = f.read().split('\n')[0:-1]
    lenght = len(data)
    count = 1 
    for line in data:
        
        list_entities = line.split(' ')
        for entity in list_entities:
            word, postag = entity.split('_')[0:2]
            
            if word not in dic_words:
                dic_words[word] = [postag]
            elif postag not in dic_words[word]:
                dic_words[word].append(postag)
        count +=1
        if count%1000 == 0:
            print("Split {0}/{1} sentences.".format(count, lenght))
            
print("Split {0}/{0} sentences.".format(lenght))

if input('Save the current dictionnary ? (1|0)') ==1:
    pk.dump(dic_words, open("word_dict_v2", "ab"))
    print("Saved.")
else:
    print("Not saved")
    
    
    

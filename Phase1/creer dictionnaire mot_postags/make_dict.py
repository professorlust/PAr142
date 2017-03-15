# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 14:35:14 2016

@author: thomas
"""
import pickle as pk


def add_words_to_dictionnary(path_to_text, dictionnary):
    with open(dictionnary, "r") as f:
        data = f.read().split('\n')[0:-1]
        lenght = len(data)
        count = 1 
        for line in data:
            
            list_entities = line.split(' ')
            for entity in list_entities:
                word, postag = entity.split('_')[0:2]
                
                if word not in dictionnary:
                    dictionnary[word] = [postag]
                elif postag not in dictionnary[word]:
                    dictionnary[word].append(postag)
            count += 1
            
            if count%1000 == 0:
                print("Split {0}/{1} sentences.".format(count, lenght))
                
    print("Split {0}/{0} sentences.".format(lenght))
    print("{} words in the dictionnary 'dic_words'".format(len(dic_words)))
    
    return dictionnary


if __name__ == '__name__':
    
    # Load or create a new dictionnary.
    if input('Load old dictionnary ? (1|0)') ==1:
        with open("word_dict_v2", 'rb') as f:
            dic_words = pk.load(f)
        print("Loaded.")
    else:
        dic_words = {}
        print("New dictionnary.")
    
    # Actual computation.
    new_dic_words = add_words_to_dictionnary('001.txt', dic_words)
    
    # Save or not the new dictionnary.
    if input('Save the current dictionnary ? (1|0)') ==1:
        pk.dump(new_dic_words, open("word_dict_v2", "wb"))
        print("Saved.")
    else:
        print("Not saved")
        
    
    

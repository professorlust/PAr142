"""
Description
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import re
import os

from random import choice, shuffle
import nltk

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from 
      https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py.
    
    Argument:
        string: one string to be cleaned.
        
    Return:
        The same string, cleaned.
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def datafile_to_array(filename):
    """
    Argument: 
        filemame, string of the location of the dataset.
        
    Returns:
        raw_data: a 2D-list of the paragraphs and their sentences.
    """
    
    def create_adjacent_sentences(sentences):
        """
        Create data from one paragraph.    
        
        Argument:
            sentences: a list of sentences from one paragraph.
            
        Returns:
            adjacent_sentences lists the lists of three adjacent sentences.
        """
        adjacent_sentences = []
        for i in range(len(sentences)-2):
            adjacent_sentences.append([sentences[i+j] for j in range(3)])
        return adjacent_sentences
    
    # Open the file    
    with open(filename, "r") as f:
        data_string = f.read()
    # Split the paragraph
    data_1D_list = data_string.split('\n+++$+++\n')
    # Split and clean the sentences
    data_2D_list = []
    for i in range(len(data_1D_list)):
        data_2D_list.append(data_1D_list[i].split('\n'))
        data_2D_list[-1] = [clean_str(sent) for sent in data_2D_list[-1]]
    # Create raw data
    raw_data = []
    for paragraph in data_2D_list:
        raw_data += create_adjacent_sentences(paragraph)
    return raw_data


def load_labels_data(data_directory):
    """
    Return all data and FALSE labels (too long to compute).
    
    Argument:
        data_directory: location of the data.
        
    Returns:
        list of all lines of data.
    """    
    # Get the list of the locations of every file in data_directory
    locations = []
    for (dirpath, dirnames, filenames) in os.walk(data_directory):
        locations.extend(filenames)
        break
    for i in range(len(locations)):
        locations[i] = os.path.join(data_directory, locations[i])       
    
    raw_data = []
    for location in locations:
        raw_data += datafile_to_array(location)

    labels_data = []
    for i in raw_data:
        data_line = " <<EOS>> ".join(i)
        label = ['i', 'i', 'i', 'i']      
        labels_data.append([label, data_line])
    return labels_data
    
    
def labelize_data(data):
    """
    Argument:
        data: list of three sentences (these are stored in another list).
        
    Returns:
        data_labels: bigger list of pairs (label, sentences (in one string)).
    """
    
    def labelize(sentences):
        """
        Create labels from sentences.
        
        2 nouns and 1 verb is taken from the first sentence.
        1 noun is taken from the third and last sentence.
            
        Argument:
            sentences: list of 3 sentences e.g. ['i am', 'no', 'you are'].
        
        Returns:
            labels: list of quadruplets of words corresponding to every label
            that can be created from the three sentences provided.
        """
        noun1 = []
        verb1 = []
        noun3 = []
        for word, pos in nltk.pos_tag(nltk.word_tokenize(sentences[0])):
            if pos.startswith('NN'):
                noun1.append(word)
            elif pos.startswith('V'):
                verb1.append(word)
        for word, pos in nltk.pos_tag(nltk.word_tokenize(sentences[2])):
            if pos.startswith('NN'):
                noun3.append(word)
        if len(noun1)<2 or verb1 == [] or noun3 == []:
            return False
        else:
            labels = []
            for word in noun1:
                for word2 in noun1:
                    if word2 != word:
                        for word3 in verb1:
                            for word4 in noun3:
                                labels.append((word, word2, word3, word4))
        return labels
    
    labels_data = []
    for i in data:
        data_line = " <<EOS>> ".join(i)
        labels = labelize(i)        
        if labels:
            for label in labels:
                labels_data.append([label, data_line])
                
    shuffle(labels_data)
    return labels_data
    

def batch_iter(data_directory, batch_size, num_epochs):
    """
    Creates a batch iterator for a dataset.
    
    Arguments:
        data_directory: location of the data.
        batch_size: number of lines in one batch.
        num_epochs: number of training epochs.

    Returns:
        list of batch_size lines of data.
    """
    
    # Get the list of the locations of every file in data_directory
    locations = []
    for (dirpath, dirnames, filenames) in os.walk(data_directory):
        locations.extend(filenames)
        break
    for i in range(len(locations)):
        locations[i] = os.path.join(data_directory, locations[i])    
    
    
    for epoch in range(num_epochs):
        # A file is chosen each epoch        
        file_chosen = choice(locations)
        raw_data = datafile_to_array(file_chosen)
        print("Epoch {}. Batch coming from {}.".format(epoch+1, file_chosen.split('/')[-1]))

        # Shuffle the data at each epoch
        shuffle_indices = np.random.permutation(np.arange(len(raw_data)))
        shuffled_raw_data = np.array(raw_data)[shuffle_indices]
        # Add labels
        shuffled_data = labelize_data(shuffled_raw_data)
        
        #num_batches_per_epoch = int((len(shuffled_data)-1)/batch_size) + 1
        num_batches_per_epoch = 20
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, len(shuffled_data))
            #print('Batch {0}/{1}'.format(batch_num+1, num_batches_per_epoch))
            yield shuffled_data[start_index:end_index]
    

if __name__ == '__main__':
    d = batch_iter('/data_new_small_small', 4000, 200000)
    a = load_labels_data('data_new_small_small')


    """
    d.next() = [[('noun1', 'noun2', 'verb1', 'noun3'), 'dfkud <<EOS>> dfkv <<EOS>> dfh']
                [('noun1', 'noun2', 'verb1', 'noun3'), 'dfkud <<EOS>> dfkv <<EOS>> dfh']
                [('noun1', 'noun2', 'verb1', 'noun3'), 'dfkud <<EOS>> dfkv <<EOS>> dfh']
                [('noun1', 'noun2', 'verb1', 'noun3'), 'dfkud <<EOS>> dfkv <<EOS>> dfh']]
    """

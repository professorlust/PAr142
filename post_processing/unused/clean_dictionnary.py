# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 19:49:24 2017

@author: thomas



Delete some useless keys in the postag_dict dictionnary
(postag_dict_2 is a copy of postag_dict).

Eventually, the final dictionnary is 45-key long.

"""
from __future__ import print_function
import pickle as pk

def printt(dictionnary):
    """Display in a nice manner a dictionnary.
    """
    for key, value in dictionnary.iteritems():
        print('{key}, size: {size}, {values}'.format(key=key, 
              size=len(value), values=value[0:4]))


# Load dictionnary
with open('postag_dict_2', 'rb') as f:
    postag_dict = pk.load(f)

# Delete some keys
keys_to_delete = ['disease', 'm', 'Saladin', 'VERB', 'length=', 'philosophy', 'animal',
         'DYN', 'cambridge.pdf', 'in', '', '12-15.pdf', 'info', 'date=|manufacturer=|unit',
         '``', 'ADV', 'urban', 'LBourke.pdf', ':', 'code', 'PAX', 
         'functions.svg|300px|right|thumb|Trigonometric', "''", "ft", 'AG', 
         'illness', 'blank1', 'AutoPlaceBars', 'WRITE', 'line=yes', 
         'Australia', 'NOUN', 'union', '.', 'MxdvMw', 'footnotes', 'history/tutor/eurvoya/columbus.htmlhttp',
         'density', 'News', "EXEC", 'Precip', 'by=Germany', 'X', 'name', 
         'activists', 'Neopaganism', 'vmuseum〈=en', '-RRB-', 'expression', 
         'offset', '1.shtmlAnd', '-LRB-', 'DET', 'AE', 'Parlement.jpg|thumb|right|Le', 'DST']

for key in keys_to_delete:
    del postag_dict[key]

# Display the result.
printt(postag_dict)

# Save the dictionnary.
with open('postag_dict_clean', 'wb') as f:
    pk.dump(postag_dict, f)
    
    



    
"""
The final dictionary:


PRP$ - size: 71    ['her', 'its', 'my', 'your']
WDT - size: 31    ['which', 'that', 'What', 'what']
JJ - size: 32598    ['olden', 'beautiful', 'much', 'great']
WP - size: 45    ['What', 'what', 'Whatever', 'who']
RP - size: 77    ['down', 'up', 'off', 'away']
$ - size: 137    ['you.', '$', 'ther', 'uhu']
VBD - size: 4483    ['helped', 'lived', 'were', 'was']
, - size: 974    [',', "'I", 'either.', "'if"]
PRP - size: 474    ['itself', 'it', 'she', 'her']
RB - size: 4577    ['still', 'all', 'so', 'Close']
NNS - size: 25888    ['times', 'daughters', 'eyes', 'clothes']
NNP - size: 108950    ['king', 'Princess', 'Henry', "'who"]
GW - size: 125    ["'follow", "'if", 'T\xc3\xb3rshavn', '//www.']
WRB - size: 53    ['when', 'whenever', 'How', 'how']
SYM - size: 736    ["'the", '\t', 'ninetieth', '+']
REC - size: 14    ['|Jan', '|Feb', '|Mar', '|Apr']
Hi - size: 49    ['|Jan', '|Feb', '|Mar', '|Apr']
EX - size: 68    ['there', 'There', "'what", "'why"]
MD - size: 45    ['could', 'would', 'can', 'will']
UH - size: 1684    ['Ah', 'Oh', 'yes', 'no']
VBG - size: 6805    ['wishing', 'holding', 'stretching', 'weeping']
FW - size: 1891    ["'is", "'no", 'forth.', "'You"]
NFP - size: 946    ["'I", "'Why", "'If", "'Of"]
VBN - size: 9664    ['seen', 'astonished', 'bored', 'cried']
VBP - size: 2459    ['weep', 'am', 'bring', 'do']
VBZ - size: 3239    ['has', 'ails', 'is', 'does']
NN - size: 52595    ['king', 'sun', 'face', 'castle']
HYPH - size: 657    ['-', 'saved-up', 'shrivelled-up', 'EC-130E']
CC - size: 73    ['but', 'and', 'And', 'nor']
PDT - size: 76    ['all', 'half', "'hold", 'such']
CD - size: 15615    ['one', 'two', 'eight', 'three']
ADD - size: 172    ['/ref', 'www.whaletrust.com', '.com', 'www.example.com']
WP$ - size: 3    ['whose', 'whoso', 'Whose']
JJS - size: 488    ['youngest', 'eldest', 'greatest', 'dearest']
JJR - size: 501    ['louder', 'more', 'younger', 'elder']
Lo - size: 59    ['|Jan', '|Feb', '|Mar', '|Apr']
DT - size: 366    ['a', 'the', 'an', 'this']
POS - size: 26    ["'s", "'", 's', 'los']
TO - size: 29    ['to', 'rapunzel', 'To', 'na']
LS - size: 758    ["'but", "'if", '\tA', 'O']
VB - size: 6954    ['fall', 'be', 'cry', 'show']
RBS - size: 105    ['most', 'Sleepest', 'wakest', 'best']
RBR - size: 68    ['nearer', 'longer', 'more', 'farther']
IN - size: 460    ['In', 'that', 'in', 'by']
NNPS - size: 7756    ['Jews', 'Gods', 'Hansels', 'Hans']
"""
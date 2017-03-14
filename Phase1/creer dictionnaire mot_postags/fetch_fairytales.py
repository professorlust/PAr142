# -*- coding: utf-8 -*-
"""
Éditeur de Spyder
Thomas Blondelle

Fetch the fairytales of grimm from www.cs.smu.edu.
Put it in the text files : "texts.txt" and "texts2.txt"
"""

import urllib2


with open("/home/thomas/Documents/Phase1/texts.txt", 'a') as f:
    for i in range (1,210):
        print(i)
        number = "%03d" % (i,)        
        url = 'http://www.cs.cmu.edu/~spok/grimmtmp/' + number + '.txt'
        response = urllib2.urlopen(url)
        html = response.read()
        f.write(html + "\n")

        print(html[0:90])




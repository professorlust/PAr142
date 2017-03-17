# PAr142
Code for my PAr 142 (Centrale Lyon)

## Requirements
* Python 2.7
* Tensorflow 1.0

## Project
Building a system that generate three contiguous sentences from four words.

More precisely, three of these four words are nouns. The last one is a verb. The first sentence must use the verb and at least two of the three words. The last sentence must use the last word.

### Data used
I used fairy tales as my training data. You can find it [here](https://github.com/bscofield/fairy-tale-remix/blob/master/data/fairy-tales.json)
All this data need to be cleaned (ie delete every character that does not provide any additionnal information like \n, '"', "'", etc.).
I put one sentence per line. This can be found on Phase1/syntaxnet/001.txt.

### Creating actual training data
I need now to take three contiguous sentences from 001.txt and extract from them three words and a verb.

### Creating the TensorFlow graph


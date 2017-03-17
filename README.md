# Generating sentences using syntactic structures
Research Project PAr142 - Ecole Centrale Lyon, 2017.

## Requirements
* Python 2.7
* Tensorflow 1.0

## Project
Building a system that generate three contiguous sentences from four words.

More precisely, three of these four words are nouns. The last one is a verb. The first sentence must use the verb and at least two of the three words. The last sentence must use the last word.

### Data used
I used fairy tales as my training data. You can find it [here](https://github.com/bscofield/fairy-tale-remix/blob/master/data/fairy-tales.json).
All this data need to be cleaned (ie delete every character that does not provide any additionnal information like \n, ", ', etc.).
I put one sentence per line. This can be found on Phase1/syntaxnet/001.txt.

### Creating actual training data
I need now to take three contiguous sentences from 001.txt and extract from them three words and a verb.

### Creating the TensorFlow graph
The file that must be launched is `train.py`. This will create the graph defined in `model.py`. This model is a very simple feed-forward regression model with 1 embedding layer and 3 hidden l ayers.

Modify directly the file `train.py` at the bottom to train it or to use it. To test it, you need to replace the tuple inside by your own, using the following order `(noun1, noun2, verb, noun3)`.


 


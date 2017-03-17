# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 11:28:37 2017

@author: thomas
"""
from __future__ import print_function

import numpy as np
import os
import pickle
import datetime

import tensorflow as tf
from tensorflow.contrib import learn
from tensorflow.python.platform import gfile
#from tensorflow.python import debug as tf_debug


import data_util as du
from model import Regression

# Like FLAGS.
LENGTH_MAX = 350 # Greater than the maximum number of tokens among all paragraphs.
DATA_DIRECTORY = "./data_new_small"
BATCH_SIZE = 5
NUM_EPOCH = 200000
EMBEDDING_SIZE = 10000
LEARNING_RATE = 0.0005
MODEL_DIR = 'model_saidi'
SAVE_EVERY = 75


def training():

    # Load data.
    print('Loading data...')
    try:
        with gfile.Open(MODEL_DIR + '/data', 'rb') as f:
            x_data, y_data = pickle.loads(f.read())
        print('  Old data found in {}.'.format(MODEL_DIR +'/data'))
    except:
        print('  Creation of a new set of data.')
        x_data, y_data = zip(*du.load_labels_data(DATA_DIRECTORY))
        with gfile.Open(MODEL_DIR + '/data', 'wb') as f:
            f.write(pickle.dumps((x_data, y_data)))

    # Load and save vocabulary.
    print('Loading vocabulary...')
    try:
        vocab_processor = learn.preprocessing.VocabularyProcessor.restore(MODEL_DIR +'/vocab')
        print("  Old vocabulary found in {}.".format(MODEL_DIR + '/vocab'))
    except:
        print("  Creation of a new vocabulary.")
        max_document_length = max([len(x.split(" ")) for x in y_data])
        vocab_processor = learn.preprocessing.VocabularyProcessor(max_document_length)
        vocab_processor.fit(y_data)
    vocab_processor_x = learn.preprocessing.VocabularyProcessor(4, vocabulary=vocab_processor.vocabulary_)
    vocab_processor.save(MODEL_DIR+ '/vocab')
    print("  Vocabulary Size: {:d}".format(len(vocab_processor.vocabulary_)))

    # Write correspondance 'word ID' to 'word'.
    with open(MODEL_DIR + '/correspondance.tsv', 'w') as f:
        f.write('Word ID\tWord\n')
        for word, word_id in vocab_processor.vocabulary_._mapping.iteritems():
            f.write('{}\t{}\n'.format(str(word_id), word))

    with tf.Graph().as_default() as graph:
        #sess = tf_debug.LocalCLIDebugWrapperSession(sess)

        # Create model.
        print('Creating model...')
        model = Regression(
                    number_of_words = len(x_data[0]),
                    sequence_length = LENGTH_MAX,
                    vocab_size = len(vocab_processor.vocabulary_),
                    embedding_size = EMBEDDING_SIZE)

        # Define Training procedure.
        global_step = tf.Variable(0, name="global_step", trainable=False)
        optimizer = tf.train.AdamOptimizer(LEARNING_RATE)
        grads_and_vars = optimizer.compute_gradients(model.loss)
        train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)

        # Checkpoint directory.
        checkpoint_path = MODEL_DIR + "/checkpoint.ckpt"
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=3)

    with tf.Session(graph=graph) as sess:

        # Initialize.
        print('Initializing...')
        sess.run(tf.global_variables_initializer())

        # Maybe restore model parameters.
        ckpt = tf.train.get_checkpoint_state(MODEL_DIR)
        if ckpt and tf.gfile.Exists(ckpt.model_checkpoint_path + '.index'):
            print("Restoring model parameters from %s." % ckpt.model_checkpoint_path)
            saver.restore(sess, ckpt.model_checkpoint_path)
        else:
            print("Fresh parameters for this model.")

        # Tensorboard.
        dir_summary = MODEL_DIR +'/summary/' + datetime.datetime.now().isoformat()
        train_writer = tf.summary.FileWriter(dir_summary, sess.graph)
        merged_summary = tf.summary.merge_all()

        def train_step(x_batch, y_batch):
            """
            A single training step.
            """
            feed_dict = {
              model.input_x: x_batch,
              model.input_y: y_batch}

            summary, _, step, loss = sess.run(
                [merged_summary, train_op, global_step, model.loss],
                feed_dict)

            train_writer.add_summary(summary, step)
            time_str = datetime.datetime.now().isoformat()
            print("{}: step {}, loss {}".format(time_str, step, loss))

        # Generate batches.
        batch_generator = du.batch_iter(DATA_DIRECTORY, BATCH_SIZE, 200000)

        # Training loops.
        while True:
            x_text, y_text = zip(*batch_generator.next())

            x_batch = [" ".join(four_words) for four_words in x_text]
            x_batch = vocab_processor_x.transform(x_batch) # list of token sequence = [[1,2,3,4], [5,6,7,8], [7,8,9,10]]
            y_batch = vocab_processor.transform(y_text) # list of tokens sequences = [[1,3 2 5 6], [7,8,9,10,12,15,16]]

            x_batch = np.array([x for x in x_batch])
            y_batch = np.array([y for y in y_batch])

            # Pad sentences of variable lengths.
            y_batch = np.concatenate((y_batch, np.zeros((len(y_batch), LENGTH_MAX - len(y_batch[1])))), 1)

            train_step(x_batch, y_batch)
            current_step = tf.train.global_step(sess, global_step)
            if current_step % SAVE_EVERY == 0:
                path = saver.save(sess, checkpoint_path, global_step=current_step)
                print("Saved model checkpoint to {}\n".format(path))


# Unfinished test function. Use with precaution.
def testing():
    tf.reset_default_graph()
    with tf.Session() as sess:
        #sess = tf_debug.LocalCLIDebugWrapperSession(sess)
    
        # Definition of x_data, y_data for the definition of the model.
        x_data = [['i']*4]*4
        y_data = ['man eat dog <<EOS>> help <<EOS>> pie',
                  'man eat dog <<EOS>> fit <<EOS>> pile',
                  'man eat dog <<EOS>> form <<EOS>> lip',
                  'man eat dog god <<EOS>> bye <<EOS>> plot']

        # Creation of the vocabulary
        max_document_length = max([len(x.split(" ")) for x in y_data])
        vocab_processor = learn.preprocessing.VocabularyProcessor(max_document_length)
        vocab_processor.fit(y_data)
        vocab_processor_x = learn.preprocessing.VocabularyProcessor(4, vocabulary=vocab_processor.vocabulary_)
        print("Vocabulary Size: {:d}".format(len(vocab_processor.vocabulary_)))
        #print(vocab_processor.vocabulary_._mapping) # print all vocabulary

        # Definition model
        # Create model.
        print('Creating model...')
        model = Regression(
                number_of_words = len(x_data[0]),
                sequence_length = LENGTH_MAX,
                vocab_size = len(vocab_processor.vocabulary_),
                embedding_size = 3)

        # Define Training procedure.
        print('training procedure')
        global_step = tf.Variable(0, name="global_step", trainable=False)
        optimizer = tf.train.AdamOptimizer(0.001)
        grads_and_vars = optimizer.compute_gradients(model.loss)
        train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)

        # Initialize.
        print('Initialize...')
        sess.run(tf.global_variables_initializer())
        print('End of initialization.')


        def train_step(x_batch, y_batch):
            """
            A single training step.
            """
            feed_dict = {
              model.input_x: x_batch,
              model.input_y: y_batch,
            }
            _, step, loss = sess.run(
                [train_op, global_step, model.loss],
                feed_dict)
            time_str = datetime.datetime.now().isoformat()
            print("{}: step {}, loss {}".format(time_str, step, loss))



        # Training loops
        while True:
            x_text = (('man', 'dog', 'eat', 'pie'),
                      ('man', 'dog', 'eat', 'pile'),
                      ('man', 'dog', 'eat', 'lip'),
                      ('man', 'dog', 'eat', 'plot'))

            y_text = ('man eat dog <<EOS>> help <<EOS>> pie',
                  'man eat dog <<EOS>> fit <<EOS>> pile',
                  'man eat dog <<EOS>> form <<EOS>> lip',
                  'man eat dog god <<EOS>> bye <<EOS>> plot')

            x_batch = [" ".join(four_words) for four_words in x_text]
            x_batch = vocab_processor_x.transform(x_batch) # list of token sequence = [[1,2,3,4], [5,6,7,8], [7,8,9,10]]
            y_batch = vocab_processor.transform(y_text) # list of tokens sequences = [[1,3 2 5 6], [7,8,9,10,12,15,16]]

            x_batch = np.array([x for x in x_batch])
            y_batch = np.array([y for y in y_batch])


            # Padding
            y_batch = np.concatenate((y_batch, np.zeros((len(y_batch), LENGTH_MAX - len(y_batch[1])))), 1)

            train_step(x_batch, y_batch)



def using(four_words_in_a_tuple):

    # Load data.
    print('Loading data...')
    try: ## TODO: change try-except with is_file..
        with gfile.Open(MODEL_DIR + '/data', 'rb') as f:
            x_data, y_data = pickle.loads(f.read())
        print('  Old data found in {}.'.format(MODEL_DIR+'/data'))
    except:
        print("I cannot continue: no data has been found in {}.".format(MODEL_DIR+'/data'))
        return

    # Load and save vocabulary.
    print('Loading vocabulary...')
    try:
        vocab_processor = learn.preprocessing.VocabularyProcessor.restore(MODEL_DIR+'/vocab')
        print("  Old vocabulary found in {}.".format(MODEL_DIR+'/vocab'))
    except:
        print("I cannot continue: no vocabulary has been found in {}.".format(MODEL_DIR+'/vocab'))
        return
    vocab_processor_x = learn.preprocessing.VocabularyProcessor(4, vocabulary=vocab_processor.vocabulary_)


    with tf.Graph().as_default() as graph:
        #sess = tf_debug.LocalCLIDebugWrapperSession(sess)

        # Create model.
        print('Creating model...')
        model = Regression(
                number_of_words = len(x_data[0]),
                sequence_length = LENGTH_MAX,
                vocab_size = len(vocab_processor.vocabulary_),
                embedding_size = EMBEDDING_SIZE)

        # Checkpoint directory.
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=1)

    with tf.Session(graph=graph) as sess:

        # Initialize.
        print('Initializing...')
        sess.run(tf.global_variables_initializer())

        # Maybe restore model parameters.
        ckpt = tf.train.get_checkpoint_state(MODEL_DIR)
        if ckpt and tf.gfile.Exists(ckpt.model_checkpoint_path + '.index'):
            print("Restoring model parameters from %s." % ckpt.model_checkpoint_path)
            saver.restore(sess, ckpt.model_checkpoint_path)
        else:
            print("I cannot continue: no checkpoint has been found in {}.".format(ckpt.model_checkpoint_path))
            return


        def test_step(x_batch, y_batch):
            """
            A single training step.
            """
            feed_dict = {
              model.input_x: x_batch,
              model.input_y: y_batch}

            scores = sess.run([model.scores],feed_dict)
            return scores


        x_text, y_text = zip(*[[four_words_in_a_tuple, 'help <<EOS>> help <<EOS>> help']])

        x_batch = [" ".join(four_words) for four_words in x_text]
        x_batch = vocab_processor_x.transform(x_batch) # list of token sequence = [[1,2,3,4], [5,6,7,8], [7,8,9,10]]
        y_batch = vocab_processor.transform(y_text) # list of tokens sequences = [[1,3 2 5 6], [7,8,9,10,12,15,16]]

        x_batch = np.array([x for x in x_batch])
        y_batch = np.array([y for y in y_batch])

        # Padding
        y_batch = np.concatenate((y_batch, np.zeros((len(y_batch), LENGTH_MAX - len(y_batch[0])))), 1)
        scores = test_step(x_batch, y_batch)

        return scores




if __name__ == '__main__':
    #test()
    training()
#
#    scores = using(('animal', 'time', 'feed', 'witch'))
#    print('scores: {}'.format(scores))
#
#    with open('scores', 'wb') as f:
#        pickle.dump(scores, f)




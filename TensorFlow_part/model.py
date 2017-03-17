# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 16:09:51 2017

@author: thomas
"""
import tensorflow as tf

class Regression(object):
    def __init__(self, number_of_words, sequence_length, vocab_size, embedding_size):
        
        # Keeping track of l2 regularization loss.
        l2_loss = tf.constant(0.0)

        # Placeholders for input, output and dropout
        self.input_x = tf.placeholder(tf.int32, [None, number_of_words], name="input_x")
        self.input_y = tf.placeholder(tf.int32, [None, sequence_length], name="input_y")
        
        # Embedding layer
        with tf.variable_scope("embedding_layer"):
            W = tf.Variable(tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0),
                            name="W")
            # embedding_lookup = select_rows ; Shape = [batch_size, number_of_words, embedding_size]
            self.input_x_embedded = tf.nn.embedding_lookup(W, self.input_x) 
            self.input_x_embedded = tf.reshape(self.input_x_embedded, [-1, number_of_words*embedding_size])
            tf.summary.histogram('weight_embedding', W)

        # Hidden layer 1
        with tf.variable_scope("wxb_layer_1"):
            W = tf.Variable(tf.truncated_normal([number_of_words*embedding_size, 500],
                                                stddev=0.1), name="W")
            b = tf.Variable(tf.constant(0.1, shape = [500]), name="b")

            self.y1 = tf.nn.xw_plus_b(self.input_x_embedded, W, b, name = 'y')
            # shape = [?, vocab_size]
            
            l2_loss += tf.nn.l2_loss(W)
            l2_loss += tf.nn.l2_loss(b)
            
            tf.summary.histogram('weight_1', W)
            tf.summary.histogram('biais_1', b)
            tf.summary.histogram('output_1', self.y1)
            
        # Hidden layer 2
        with tf.variable_scope("wxb_layer_2"):
            W = tf.Variable(tf.truncated_normal([500, vocab_size],
                                                stddev=0.1), name="W")
            b = tf.Variable(tf.constant(0.1, shape = [vocab_size]), name="b2")

            self.scores = tf.nn.l2_normalize(tf.nn.xw_plus_b(self.y1, W, b), 1, name='scores_normalized')
            # shape = [batch_size, vocab_size]
            
            l2_loss += tf.nn.l2_loss(W)
            l2_loss += tf.nn.l2_loss(b)
            
            tf.summary.histogram('weight_2', W)
            tf.summary.histogram('biais_2', b)
            tf.summary.histogram('output_2', self.scores)

        # Reference distribution
        with tf.variable_scope("reference_distribution"):
            y = tf.one_hot(self.input_y, vocab_size, name='one_hot_distrib')
            t = tf.reduce_sum(y, 1, name='reduced_sum_distrib')
            self.distrib = tf.nn.l2_normalize(t, 1, name='normalized_distrib')
        
        with tf.variable_scope("loss"):
            losses = tf.nn.softmax_cross_entropy_with_logits(logits=self.scores, labels=self.distrib)
            self.loss = tf.reduce_mean(losses, name='loss') + 4*l2_loss ## TODO: l2-reg coefficient
            tf.summary.scalar('loss', self.loss)
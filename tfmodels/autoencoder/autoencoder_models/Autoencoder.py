import tensorflow as tf
import numpy as np
from tfmodels.autoencoder.Utils import *


class Autoencoder(object):

    def __init__(self, params, weight_= None):
        # n_input, n_hidden, transfer_function = tf.nn.softplus, optimizer = tf.train.AdamOptimizer()
        self.params = params
        self.n_input = params['n_input']
        self.n_hidden = params['n_hidden']
        self.transfer = params['transfer_function']
        self.optimizer_ = params['optimizer']

        network_weights = self._initialize_weights(weight_)
        self.weights = network_weights

        # model
        self.x = tf.placeholder(tf.float32, [None, self.n_input])
        self.hidden = self.transfer(tf.add(tf.matmul(self.x, self.weights['w1']), self.weights['b1']))
        self.reconstruction = tf.add(tf.matmul(self.hidden, self.weights['w2']), self.weights['b2'])

        # cost
        self.cost = 0.5 * tf.reduce_sum(tf.pow(tf.sub(self.reconstruction, self.x), 2.0))
        self.optimizer = self.optimizer_.minimize(self.cost)

        init = tf.initialize_all_variables()
        self.sess = tf.Session()
        self.sess.run(init)

    def _initialize_weights(self, weight):
        all_weights = dict()
        if weight is not None:
            all_weights['w1'] = tf.Variable(weight.astype('float32'), dtype=tf.float32)
            all_weights['b1'] = tf.Variable(tf.zeros([self.n_hidden], dtype=tf.float32))
            all_weights['w2'] = tf.Variable(tf.transpose(weight.astype('float32')), dtype=tf.float32)
            all_weights['b2'] = tf.Variable(tf.zeros([self.n_input], dtype=tf.float32))
        else:
            all_weights['w1'] = tf.Variable(xavier_init(self.n_input, self.n_hidden))
            all_weights['b1'] = tf.Variable(tf.zeros([self.n_hidden], dtype=tf.float32))
            all_weights['w2'] = tf.Variable(tf.zeros([self.n_hidden, self.n_input], dtype=tf.float32))
            all_weights['b2'] = tf.Variable(tf.zeros([self.n_input], dtype=tf.float32))
        return all_weights

    def partial_fit(self, X):
        cost, opt = self.sess.run((self.cost, self.optimizer), feed_dict={self.x: X})
        return cost

    def inference(self, X):
        return self.sess.run(self.cost, feed_dict={self.x: X})

    def calc_total_cost(self, X):
        return self.sess.run(self.cost, feed_dict = {self.x: X})

    def transform(self, X):
        return self.sess.run(self.hidden, feed_dict={self.x: X})

    def generate(self, hidden = None):
        if hidden is None:
            hidden = np.random.normal(size=self.weights["b1"])
        return self.sess.run(self.reconstruction, feed_dict={self.hidden: hidden})

    def reconstruct(self, X):
        return self.sess.run(self.reconstruction, feed_dict={self.x: X})

    def get_hidden_activation(self, X):

        return [self.sess.run(self.hidden, feed_dict={self.x: X})]

    def getWeights(self):
        return self.sess.run(self.weights['w1'])

    def getReconstructionWeights(self):
        return self.sess.run(self.weights['w2'])

    def getBiases(self):
        return self.sess.run(self.weights['b1'])


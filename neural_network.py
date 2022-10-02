#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 20:34:10 2022

@author: sven
"""
import numpy as np


RANGE = 1.


class NeuralNetwork:
    def __init__(self, seed):
        np.random.seed(seed)
        self.weights = [
            # np.eye(5),
            self.random(20).reshape(5, 4),
            self.random(4).reshape(4, 1)
            ]
        self.biases = [
            # np.zeros(5).reshape(1, 5),
            (2 * np.random.random(4).reshape(1, 4) - 1) * RANGE,
            (2 * np.random.random(1).reshape(1, 1) - 1) * RANGE
            ]

    @staticmethod
    def random(size):
        data = (2. * np.random.random(size) - 1.) * RANGE
        return data

    @staticmethod
    def _sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def calculate(self, o):
        # import pdb;pdb.set_trace()
        for i in range(2):
            internals = np.dot(o, self.weights[i]) + self.biases[i]
            o = self._sigmoid(internals)
        return o

    # def get_internal(self):
    #     data = np.r_[np.dot(np.ones(5), self.weights[0]), self.weights[1].T.reshape(20),
    #                   self.weights[2].reshape(4), self.biases[0].reshape(5),
    #                   self.biases[1].reshape(4), self.biases[2].reshape(1)]
    #     return data

    def get_internal(self):
        data = np.r_[self.weights[0].T.reshape(20),
                      self.weights[1].reshape(4),
                      self.biases[0].reshape(4), self.biases[1].reshape(1)]
        return data

    def set_internal(self, data):
        self.weights = [
            np.eye(5) * data[:5],
            data[5:25].reshape(4, 5).T,
            data[25:29].reshape(4, 1)
            ]
        self.biases = [
            data[29:34].reshape(1, 5),
            data[34:38].reshape(1, 4),
            data[38].reshape(1, 1)
            ]


if __name__ == "__main__":
    nn = NeuralNetwork(1)

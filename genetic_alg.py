#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 20:37:16 2022

@author: sven
"""
import numpy as np


def get_random_int(min_int, max_int):
    dint = max_int - min_int
    res = dint + 1
    while res > dint:
        res = int(np.random.random() * (dint + 1))
    return res + min_int


def crossover(p1, p2):
    idx0 = get_random_int(0, len(p1)-1)
    idx1 = get_random_int(idx0+1, len(p1))
    return np.r_[p1[:idx0], p2[idx0:idx1], p1[idx1:]]


def select_process(p):
    cum_fitness = 0.
    for itm in p:
        cum_fitness += itm[0]
    pcum = []
    lastcum = 0.
    for itm in p:
        pcum.append((lastcum + itm[0] / cum_fitness, itm[1]))
        lastcum = pcum[-1][0]
    rand = np.random.random()
    for itm in pcum:
        if itm[0] >= rand:
            return itm[1]


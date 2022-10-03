#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 11:29:55 2022

@author: sven
"""
import os

import json
import tkinter as tk

import play
import neural_network
import genetic_alg


def play_game(gb, p, n):
    ctr = 0
    while not gb.check_collision(p.x, p.y) and p.nlaps < 2:
        output = n.calculate(play.get_player_distances(gb, p) / play.L)
        if output > 0.5:
            p.turn_right()
        else:
            p.turn_left()
        p.step()
        ctr += 1
    return ctr


def play_set(board, n_, training_loop=0):
    res = []
    for i, n in enumerate(n_):
        p = play.Player(50, len(board)*play.L/2-30, 0.05, 1, True)
        gb = play.Gameboard(board)
        ctr = play_game(gb, p, n)
        fname = "auto_play{:d}_day{:d}.csv".format(i, training_loop)
        play.save_player(p, fname)
        res.append((ctr, n))
    return res


def get_random_networks(n):
    return [neural_network.NeuralNetwork(i) for i in range(n)]


def get_replay_names(training_loop):
    suffix = "_day{:d}.csv".format(training_loop)
    return [itm for itm in os.listdir(".") if itm.endswith(suffix)]


def improve_networks(n_):
    res = []
    for i in range(46):
        p1 = genetic_alg.select_process(n_)
        p2 = genetic_alg.select_process(n_)
        internal_new = genetic_alg.crossover(p1.get_internal(), p2.get_internal())
        n_new = neural_network.NeuralNetwork()
        n_new.set_internal(internal_new)
        res.append(n_new)
    for i in range(4):
        res.append(neural_network.NeuralNetwork())
    return res


def train(board, ndays):
    n_ = get_random_networks(50)
    res = play_set(board, n_, 0)
    for day_ in range(1, ndays):
        print("day {:d}".format(day_))
        n_ = improve_networks(res)
        res = play_set(board, n_, day_)
    return n_


# if __name__ == "__main__":
#     with open("board.json", "r") as fid:
#         board = json.loads(fid.read())
#     fnames = []
#     for i in range(50):
#         n = neural_network.NeuralNetwork(i)
#         print(n.get_internal())
#         p = play.Player(50, len(board)*play.L/2-30, 0.05, 1, True)
#         gb = play.Gameboard(board)
#         play_game(gb, p, n)
#         fnames.append("auto_play{:d}.csv".format(i))
#         play.save_player(p, fnames[-1])

#     root = tk.Tk()
#     # rgb = play.ReprGameboard(root, board)
#     play.replay_multiple(root, fnames)
#     root.mainloop()


if __name__ == "__main__":
    with open("board.json", "r") as fid:
        board = json.loads(fid.read())

    n_ = train(board, 3)
    fnames = get_replay_names(2)
    root = tk.Tk()
    play.replay_multiple(root, fnames)
    root.mainloop()

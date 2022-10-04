#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 11:29:55 2022

@author: sven
"""
import multiprocessing as mp

import numpy as np
import json
import tkinter as tk

import play
import neural_network
import genetic_alg


def play_game(board, n, savename=None):
    p = play.Player(50, len(board)*play.L/2-30, 0.05, 1, True)
    gb = play.Gameboard(board)
    ctr = 0
    while not gb.check_collision(p.x, p.y) and p.nlaps < 2:
        output = n.calculate(play.get_player_distances(gb, p) / play.L)
        if output > 0.5:
            p.turn_right()
        else:
            p.turn_left()
        p.step()
        ctr += 1
    if savename is not None:
        play.save_player(p, savename)
    return ctr, n


def play_set(board, n_, training_loop=0):
    res = []
    pool = mp.Pool(mp.cpu_count())
    res = pool.starmap_async(play_game, [(board, n, "auto_play{:d}_day{:d}.csv".format(i, training_loop)) for i, n in enumerate(n_)])
    # for i, n in enumerate(n_):
    #     ctr = play_game(board, n, "auto_play{:d}_day{:d}.csv".format(i, training_loop))
    #     res.append(ctr)
    res = res.get()
    pool.close()
    return res


def get_random_networks(n):
    return [neural_network.NeuralNetwork(i) for i in range(n)]



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
#         fnames.append("auto_play{:d}.csv".format(i))
#         play_game(board, n, fnames[-1])

#     root = tk.Tk()
#     # rgb = play.ReprGameboard(root, board)
#     play.replay_multiple(root, fnames)
#     root.mainloop()


if __name__ == "__main__":
    with open("board.json", "r") as fid:
        board = json.loads(fid.read())

    n_ = train(board, 20)
    output = np.array([itm.get_internal() for itm in n_])
    np.savetxt("networs.csv", output)
    fnames = play.get_replay_names(19)
    root = tk.Tk()
    play.replay_multiple(root, fnames)
    root.mainloop()

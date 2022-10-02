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


def play_game(gb, p, n):
    ctr = 0
    while not gb.check_collision(p.x, p.y):
        output = n.calculate(play.get_player_distances(gb, p) / play.L)
        if output > 0.5:
            p.turn_right()
        else:
            p.turn_left()
        p.step()
        ctr += 1


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
    n_ = get_random_networks(50)
    play_set(board, n_)

    fnames = get_replay_names(0)
    root = tk.Tk()
    play.replay_multiple(root, fnames)
    root.mainloop()


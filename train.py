#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 11:29:55 2022

@author: sven
"""
import json
import tkinter as tk

import play
import neural_network


def play_game(gb, p, n):
    while not gb.check_collision(p.x, p.y):
        output = n.calculate(play.get_player_distances(gb, p))
        if output > 0.5:
            p.turn_right()
        else:
            p.turn_left()
        p.step()


if __name__ == "__main__":
    with open("board.json", "r") as fid:
        board = json.loads(fid.read())
    fnames = []
    for i in range(50):
        n = neural_network.NeuralNetwork(i)
        print(n.get_internal())
        p = play.Player(50, len(board)*play.L/2-30, 0.05, 1, True)
        gb = play.Gameboard(board)
        play_game(gb, p, n)
        fnames.append("auto_play{:d}.csv".format(i))
        play.save_player(p, fnames[-1])

    root = tk.Tk()
    # rgb = play.ReprGameboard(root, board)
    play.replay_multiple(root, fnames)
    root.mainloop()

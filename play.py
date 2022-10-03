#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 14:03:52 2022

@author: sven
"""
import json
import numpy as np

import tkinter as tk


L = 20
R = 5


class Player:
    def __init__(self, x, y, drot, velo=1, record=False):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 1
        self.nlaps = 0
        self.starty = y
        self.drot = drot
        self.velo = velo
        self.angle = np.pi/2
        self.recorded_data = []
        self.record = record
        if self.record:
            self.recorded_data.append((x, y))

    def step(self):
        yold = self.y
        self.y -= self.dy
        self.x += self.dx
        if yold > self.starty and self.y <= self.starty:
            self.nlaps += 1
        if self.record:
            self.recorded_data.append((self.x, self.y))

    def turn_right(self):
        self.angle -= self.drot
        self.dx, self.dy = self.velo * np.cos(self.angle), self.velo * np.sin(self.angle)

    def turn_left(self):
        self.angle += self.drot
        self.dx, self.dy = self.velo * np.cos(self.angle), self.velo * np.sin(self.angle)


class ReprGameboard:
    R = 5
    def __init__(self, root, board):
        self.board = board
        self.dir_key_l = False
        self.dir_key_r = False
        self.canvas = tk.Canvas(root, bg="white", height=len(self.board)*L, width=len(self.board[0])*L)
        self.canvas.pack()
        for i, row in enumerate(self.board):
            for j, itm in enumerate(row):
                if itm is False:
                    self.draw_square(j*L, i*L, L, "grey")
        root.bind("<KeyPress>", self.cb_keydown)
        root.bind("<KeyRelease>", self.cb_keyup)

    def draw_free_fields(self):
        for i, row in enumerate(self.board):
            for j, itm in enumerate(row):
                if itm is True:
                    self.draw_square(j*L, i*L, L, "white")

    def draw_square(self, x, y, l, color):
        self.canvas.create_rectangle(x, y, x+l, y+l, fill=color, outline="")

    def draw_circle(self, x, y, color):
        self.canvas.create_oval(x-R, y-R, x+self.R, y+self.R, fill=color,
                                outline="")

    def move_player(self, xold, yold, xnew, ynew):
        self.draw_circle(xold, yold, "white")
        self.draw_circle(xnew, ynew, "red")

    def cb_keydown(self, event):
        if event.keysym == "Right":
            self.dir_key_r = True
        elif event.keysym == "Left":
            self.dir_key_l = True

    def cb_keyup(self, event):
        if event.keysym == "Right":
            self.dir_key_r = False
        elif event.keysym == "Left":
            self.dir_key_l = False


class Gameboard:
    def __init__(self, board):
        self.board = board

    def check_collision(self, x, y):
        x0, x1 = x - R, x + R
        y0, y1 = y - R, y + R
        idx_x0 = int(x0 // L)
        idx_x1 = int(x1 // L)
        idx_y0 = int(y0 // L)
        idx_y1 = int(y1 // L)
        idx_xc = int(x // L)
        idx_yc = int(y // L)
        return not (self.board[idx_yc][idx_x0]
                    and self.board[idx_yc][idx_x1]
                    and self.board[idx_y0][idx_xc]
                    and self.board[idx_y1][idx_xc])

    def get_distance(self, x, y, phi):
        dx = np.cos(phi)
        dy = np.sin(phi)
        idx_x = int(x // L)
        idx_y = int(y // L)
        if self.board[idx_y][idx_x] is False:
            return 0.0
        if dx > 0.:
            xV = (idx_x + 1) * L
            next_tile_offsetx = 1e-10
        else:
            xV = idx_x * L
            next_tile_offsetx = -1e-10
        if dy > 0.:
            yH = idx_y * L
            next_tile_offsety = -1e-10
        else:
            yH = (idx_y + 1) * L
            next_tile_offsety = 1e-10
        if np.abs(dx) > 1e-10:
            m = dy / dx
        else:
            m = 1e50
        yV = y - m * (xV - x)
        if np.abs(m) > 1e-10:
            xH = x + (yH - y) / m
        else:
            xH = 1e10
        LsqV = (yV - y)**2. + (xV - x)**2.
        LsqH = (yH - y)**2. + (xH - x)**2.
        if LsqH < LsqV:
            xnew, ynew = xH, yH + next_tile_offsety
            L_ = LsqH
        else:
            xnew, ynew = xV + next_tile_offsetx, yV
            L_ = LsqV
        return np.sqrt(L_) + self.get_distance(xnew, ynew, phi)


def save_player(p, fname):
    with open(fname, "w") as fid:
        for ln in p.recorded_data:
            fid.write("{:d}, {:d}\n".format(int(ln[0]), int(ln[1])))


def replay(root, fname):
    with open("board.json", "r") as fid:
        board = json.loads(fid.read())
    data = read_save(fname)
    rgb = ReprGameboard(root, board)
    rgb.canvas.after(50, replay_step, rgb, data)


def replay_step(rgb, data):
    xold, yold = data.pop(0)
    if len(data):
        rgb.move_player(xold, yold, data[0][0], data[0][1])
        rgb.canvas.after(50, replay_step, rgb, data)


def game_loop(rgb, b, p):
    xold, yold = p.x, p.y
    if rgb.dir_key_r:
        p.turn_right()
    if rgb.dir_key_l:
        p.turn_left()
    p.step()
    rgb.move_player(xold, yold, p.x, p.y)
    if not b.check_collision(p.x, p.y):
        rgb.canvas.after(50, game_loop, rgb, b, p)
    else:
        print("Game over")


def read_save(fname):
    data = []
    with open(fname, "r") as fid:
        for ln in fid.read().split("\n"):
            chunks = ln.split(",")
            if len(chunks) == 2:
                data.append((int(chunks[0]), int(chunks[1])))
    return data


def read_and_pad_multiples(namelist):
    datalist = [read_save(fname) for fname in namelist]
    lens = [len(itm) for itm in datalist]
    max_len = max(lens)
    datalist = [itm + (max_len - len(itm)) * [itm[-1]]
                for itm in datalist]
    return datalist


def replay_multiple(root, namelist):
    with open("board.json", "r") as fid:
        board = json.loads(fid.read())
    data = [itm for itm in zip(*read_and_pad_multiples(namelist))]
    rgb = ReprGameboard(root, board)
    rgb.canvas.after(50, replay_multiple_step, rgb, data)


def replay_multiple_step(rgb, data):
    pos = data.pop(0)
    rgb.draw_free_fields()
    for p in pos:
        rgb.draw_circle(p[0], p[1], "red")
    if len(data):
        rgb.canvas.after(50, replay_multiple_step, rgb, data)


def get_player_distances(b, p):
    res = np.array([b.get_distance(p.x, p.y, p.angle + i * np.pi/4 - np.pi/2) for i in range(5)])
    return res


if __name__ == "__main__":
    with open("board.json", "r") as fid:
        board = json.loads(fid.read())
    root = tk.Tk()
    p = Player(50, len(board)*L/2, 0.05, 1, True)
    gb = Gameboard(board)
    rgb = ReprGameboard(root, board)
    root.after(50, game_loop, rgb, gb, p)
    root.mainloop()
    save_player(p, "test2.csv")

# if __name__ == "__main__":
#     root = tk.Tk()
#     replay(root, "auto_play.csv")
#     root.mainloop()

# if __name__ == "__main__":
#     root = tk.Tk()
#     replay_multiple(root, ("test.csv", "test1.csv", "test2.csv"))
#     root.mainloop()

# if __name__ == "__main__":
#     with open("board.json", "r") as fid:
#         board = json.loads(fid.read())
#     p = Player(50, len(board)*L/2, 0.05, 1, True)
#     # p.angle = np.pi*1/4.
#     gb = Gameboard(board)
#     print(get_distances(gb, p))
#     root = tk.Tk()
#     rgb = ReprGameboard(root, board)
#     rgb.draw_circle(p.x, p.y, "red")
#     root.mainloop()

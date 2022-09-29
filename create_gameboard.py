# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import tkinter
import numpy as np
import json

# init tk
root = tkinter.Tk()


L = 20
GBX = 30
GBY = 20

if True:
    with open("board.json", "r") as fid:
        board = json.loads(fid.read())
else:
    board = [[np.random.random() > 0.99999 for i in range(GBX)] for j in range(GBY)]

board[0] = GBX * [False]
board[-1] = GBX * [False]
for i in range(GBY):
    board[i][0] = False
    board[i][-1] = False

def draw_square(canvas, x, y, l, color):
    canvas.create_rectangle(x, y, x+l, y+l, fill=color, outline="")


BUTTON_DOWN1 = False
BUTTON_DOWN3 = False


def cb_motion(evt):
    global board, BUTTON_DOWN1, BUTTON_DOWN3
    if BUTTON_DOWN1 == BUTTON_DOWN3:
        return
    x_pos = evt.x // L
    y_pos = evt.y // L
    board[y_pos][x_pos] = True
    if BUTTON_DOWN1:
        board[y_pos][x_pos] = True
        draw_square(evt.widget, x_pos*L, y_pos*L, L, "white")
    if BUTTON_DOWN3:
        board[y_pos][x_pos] = False
        draw_square(evt.widget, x_pos*L, y_pos*L, L, "grey")



def cb_click1(evt):
    global board, BUTTON_DOWN1
    BUTTON_DOWN1 = True
    x_pos = evt.x // L
    y_pos = evt.y // L
    board[y_pos][x_pos] = True
    draw_square(evt.widget, x_pos*L, y_pos*L, L, "white")


def cb_click2(evt):
    global board, BUTTON_DOWN3
    BUTTON_DOWN3 = True
    x_pos = evt.x // L
    y_pos = evt.y // L
    board[y_pos][x_pos] = False
    draw_square(evt.widget, x_pos*L, y_pos*L, L, "grey")


def cb_up1(evt):
    global BUTTON_DOWN1
    BUTTON_DOWN1 = False


def cb_up2(evt):
    global BUTTON_DOWN3
    BUTTON_DOWN3 = False


def save(board, fname):
    with open(fname, "w") as fid:
        fid.write(json.dumps(board))


# create canvas
myCanvas = tkinter.Canvas(root, bg="white", height=GBY*L, width=GBX*L)
myCanvas.bind("<Button-1>", cb_click1)
myCanvas.bind("<ButtonRelease-1>", cb_up1)
myCanvas.bind("<ButtonRelease-3>", cb_up2)
myCanvas.bind("<Button-3>", cb_click2)
myCanvas.bind('<Motion>', cb_motion)

for i, row in enumerate(board):
    for j, itm in enumerate(row):
        if itm is False:
            draw_square(myCanvas, j*L, i*L, L, "grey")

# add to window and show
myCanvas.pack()
root.mainloop()
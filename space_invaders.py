#!/usr/bin/env python
from Tkinter import *
import random

def init():
    canvas.data.score = 0
    canvas.data.level = 0
    canvas.data.board = make_matrix(canvas.data.rows, canvas.data.cols)
    canvas.data.delay = 500
    canvas.data.isGameOver  = False

def run(rows, cols):
    global canvas
    root = Tk()

    # Size up the board's screen real estate
    cell_size = 15
    canvas_width = cols * cell_size
    canvas_height = rows * cell_size
    canvas = Canvas(root, width=canvas_width, height=canvas_height)

    # Initialize the data carrier
    class Struct:pass
    canvas.data =  Struct()
    canvas.data.empty_color = "blue"
    canvas.data.rows = rows
    canvas.data.cols = cols
    canvas.pack()

    # Go save the planet!
    init()
    root.mainloop()

def make_matrix(rows, cols):
    the_list = [cols * [columns] for columns in [canvas.data.empty_color] * rows]
    print the_list
    return the_list

run(30, 20)

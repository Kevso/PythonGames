#!/usr/bin/env python
from Tkinter import *
import random

# Initialize the game system
def init():
    canvas.data.score = 0
    canvas.data.level = 0
    canvas.data.board = make_matrix(canvas.data.rows, canvas.data.cols)
    canvas.data.delay = 500
    canvas.data.is_game_over  = False
    canvas.data.player_row = bottom_row()
    canvas.data.player_col = int(len(canvas.data.board[0]) / 2)

# Run the game system
def run(rows, cols):
    global canvas
    root = Tk()

    # Size up the board's screen real estate
    cell_size = 15
    canvas_margin = 20
    canvas_width = cols * cell_size + 2 * canvas_margin
    canvas_height = rows * cell_size + 2 * canvas_margin
    canvas = Canvas(root, width=canvas_width, height=canvas_height)

    # Initialize the data carrier
    class Struct:pass
    canvas.data =  Struct()
    canvas.data.empty_color = "white"
    canvas.data.bug_color = "black"
    canvas.data.player_color = "gray"
    canvas.data.rows = rows
    canvas.data.cols = cols
    canvas.data.width = canvas_width
    canvas.data.height = canvas_height
    canvas.data.cell_size = cell_size
    canvas.data.margin = canvas_margin
    canvas.pack()

    # Register event listeners
    root.bind("<Key>", key_pressed)

    # Go save the planet!
    init()
    fire_timer()
    root.mainloop()

# Create a rows x cols sized matrix
def make_matrix(rows, cols):
    the_list = [cols * [columns] for columns in [canvas.data.empty_color] * rows]
    return the_list

# Draws a single cell at the given (row, col) coordinate with the specified color
def draw_cell(row, col, color):
    margin = canvas.data.margin
    cell_size = canvas.data.cell_size
    left   = cell_size * col + margin
    right  = left + cell_size
    top    = cell_size * row + margin
    bottom = top + cell_size
    canvas.create_rectangle(left, top, right, bottom, fill=color)

def draw_board():
    board = canvas.data.board
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        for col in range(cols):
            draw_cell(row, col, board[row][col])

def draw_bug(row,col):
    draw_cell(row, col, canvas.data.bug_color)

def draw_player(row,col):
    draw_cell(row, col, canvas.data.player_color)

def move_player(row_delta, col_delta):
    row = canvas.data.player_row + row_delta
    col = canvas.data.player_col + col_delta
    if is_valid_move(row, col):

        # clear old player location
        draw_cell(canvas.data.player_row, canvas.data.player_col, canvas.data.empty_color)
        
        # set new player location
        canvas.data.player_row = row
        canvas.data.player_col = col
    print canvas.data.board[bottom_row()]
    redraw_all()

def is_valid_move(row, col):
    return 0 < row <= bottom_row() and 0 <= col < canvas.data.cols

def redraw_all():
    
    # Clear the board
    canvas.delete(ALL)
    
    # Setup text styling
    text_font = "Helvetica "
    text_normal_color = "black"
    text_alert_color = "red "
    text_normal_size = "13 "
    text_alert_size = "26 "

    # Render board
    draw_board()
    draw_player(canvas.data.player_row, canvas.data.player_col)
    if canvas.data.is_game_over:
        canvas.create_text(canvas.data.width / 2,
                           canvas.data.canvas_height * 2 / 5, text="Game Over Man!",
                           fill=text_alert_color, font=text_font + text_alert_size + " bold")
        canvas.create_text(canvas.data.width / 2,
                           canvas.data.height * 2 / 5, text="Play Again? (y)",
                           fill=text_alert_color, font=text_font + text_normal_size +" bold")
    else:
        canvas.create_text(canvas.data.width / 2,
                           canvas.data.margin / 2,
                           text="Score: " + str(canvas.data.score), 
                           fill=text_normal_color,
                           font=text_font + text_normal_size)

# Fires the game timer
def fire_timer():
    redraw_all()
    if not canvas.data.is_game_over:
        # move bugs
        pass
    canvas.after(canvas.data.delay, fire_timer)

def bottom_row():
    return len(canvas.data.board) - 1

def key_pressed(event):
    if 'y' == event.keysym:
        init()
    elif not canvas.data.is_game_over:
        if "Left" == event.keysym:
            move_player(0, -1)
        elif "Right" == event.keysym:
            move_player(0, +1)
    redraw_all()
        
# Run the game
run(30, 20)

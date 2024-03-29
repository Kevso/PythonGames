#!/usr/bin/env python
from Tkinter import *
import random

# Initialize the game system
def init():
    canvas.data.player_avatar = PhotoImage(file="images/player.gif")
    canvas.data.bug_avatar = PhotoImage(file="images/bug.gif")
    canvas.data.player_bullet_avatar = PhotoImage(file="images/player_bullet.gif")
    canvas.data.bug_bullet_avatar = PhotoImage(file="images/bug_bullet.gif")
    canvas.data.score = 0
    canvas.data.level = 0
    canvas.data.board = make_matrix(canvas.data.rows, canvas.data.cols)
    canvas.data.delay = 250
    canvas.data.bullet_delay = 100
    canvas.data.max_player_bullets = 5
    canvas.data.num_player_bullets = 0
    canvas.data.max_bug_bullets = 10
    canvas.data.num_bug_bullets = 0
    canvas.data.bug_fire_rate = 3 #% fire rate
    canvas.data.is_game_over  = False
    canvas.data.player_row = bottom_row()
    canvas.data.player_col = int(len(canvas.data.board[0]) / 2)
    canvas.data.bug_saturation = .666
    canvas.data.max_bug_rows = 10
    canvas.data.current_bug_rows = 0
    canvas.data.bug_marching_delta = 1 #bugs march to the right
    canvas.data.bugs_changed_direction = False
    make_bug_row() # Make the initial line of the swarm
    make_player(canvas.data.player_row, canvas.data.player_col)

# Run the game system
def run(rows, cols):
    global canvas
    root = Tk()

    # Size up the board's screen real estate
    cell_size = 21
    canvas_margin = 20
    canvas_width = cols * cell_size + 2 * canvas_margin
    canvas_height = rows * cell_size + 2 * canvas_margin
    canvas = Canvas(root, width=canvas_width, height=canvas_height)

    # Initialize the data carrier
    class Struct:pass
    canvas.data =  Struct()
    canvas.data.empty_color = "white"
    canvas.data.bug_color = "pink"
    canvas.data.player_color = "gray"
    canvas.data.player_bullet_color = "black"
    canvas.data.bug_bullet_color = "brown"
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
    canvas.data.is_game_over  = True # Start in a 'stopped' state.
    fire_timer()
    fire_projectile_timer()
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
    
    #update presentation model
    avatar = None
    if canvas.data.bug_color == color:
        avatar = canvas.data.bug_avatar
    elif canvas.data.player_bullet_color == color:
        avatar = canvas.data.player_bullet_avatar
    elif canvas.data.bug_bullet_color == color:
        avatar = canvas.data.bug_bullet_avatar
    elif canvas.data.player_color == color:
        avatar = canvas.data.player_avatar
    canvas.create_image(left, top, image=avatar, anchor=NW)

# Determines if the the swarm has been fully rendered
def should_make_bug_row():
    return canvas.data.current_bug_rows < canvas.data.max_bug_rows \
        and not contains_bugs(top_row())

# Determines if the input row contains bugs
def contains_bugs(row_num):
    for col in canvas.data.board[row_num]:
        if col == canvas.data.bug_color:
            return True
    return False

# Makes a new row with the appropriate number of bugs
def make_bug_row():
    # The marching direction determines if the new row should be placed
    # at the left or right side of the board
    num_bugs_to_draw = int(canvas.data.cols * canvas.data.bug_saturation)
    if bugs_are_moving_right():
        for col in range(num_bugs_to_draw):
            make_bug(row=0, col=col)
    else:
        for col in range(canvas.data.cols-1, canvas.data.cols-num_bugs_to_draw-1, -1):
            make_bug(row=0, col=col)
    canvas.data.current_bug_rows += 1

# Renders the entire game board and all of its pieces
def draw_board():
    board = canvas.data.board
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        for col in range(cols):
            draw_cell(row, col, board[row][col])

# Makes a cell on the board represent a bug
def make_bug(row,col):
    if is_player(row, col):
        canvas.data.is_game_over = True
    canvas.data.board[row][col] = canvas.data.bug_color

# Makes a cell on the board represent the player
def make_player(row,col):
    canvas.data.board[row][col] = canvas.data.player_color

# Makes a player bullet at the row and col
def make_player_bullet(row,col):
    if is_bug(row, col):
        make_empty(row, col)
        remove_player_bullet(row, col)
        score_player_hit(row)
    elif is_bug_bullet(row, col):
        remove_player_bullet(row, col)
        remove_bug_bullet(row, col)
    else:
        canvas.data.board[row][col] = canvas.data.player_bullet_color

def make_bug_bullet(row,col):
    if is_player(row,col):
        remove_bug_bullet(row, col)
        canvas.data.is_game_over = True
    elif is_player_bullet(row, col):
        remove_player_bullet(row, col)
        remove_bug_bullet(row, col)
    elif is_bug(row, col):
        canvas.data.num_bug_bullets -= 1
    else:
        if is_on_board(row, col):
            canvas.data.board[row][col] = canvas.data.bug_bullet_color
            canvas.data.num_bug_bullets += 1

# Makes a cell on the board represent an unoccupied area
def make_empty(row, col):
    canvas.data.board[row][col] = canvas.data.empty_color

# Moves the player's avatar on the board
def move_player(row_delta, col_delta):
    row = canvas.data.player_row + row_delta
    col = canvas.data.player_col + col_delta
    if is_valid_player_move(row, col):
        current_row = canvas.data.player_row
        current_col = canvas.data.player_col

        # clear old player location
        make_empty(current_row, current_col)
        
        # set new player location
        canvas.data.player_row = row
        canvas.data.player_col = col
        make_player(canvas.data.player_row, canvas.data.player_col)
    redraw_all()

# Moves the player bullets
def move_player_bullets():
    for row in range(len(canvas.data.board)):
        for col in range(len(canvas.data.board[0])):
            if is_player_bullet(row, col):
                move_player_bullet(row, col)

# Moves the bug bullets
def move_bug_bullets():
    for row in range(len(canvas.data.board)-1, -1, -1):
        for col in range(len(canvas.data.board[0])-1, -1, -1):
            if is_bug_bullet(row, col):
                move_bug_bullet(row, col)

# Moves all of the bugs on the board in their marching direction.
def move_bugs():
    # The order in which you shift the bugs depends on the direction
    # they're marching
    if bugs_are_moving_right():
        canvas.data.bugs_changed_direction = False
        for row in range(len(canvas.data.board)):
            for col in range(len(canvas.data.board[0])-1, -1, -1):
                if is_bug(row, col) and not canvas.data.bugs_changed_direction:
                    move_bug_horizontal(row, col)
    else:
        canvas.data.bugs_changed_direction = False
        for row in range(len(canvas.data.board)):
            for col in range(len(canvas.data.board[0])):
                if is_bug(row, col) and not canvas.data.bugs_changed_direction:
                    move_bug_horizontal(row, col)
    redraw_all()

# Moves a single bug on the board horizontally in the appropriate marching direction.
def move_bug_horizontal(row, col):
    new_col = col + canvas.data.bug_marching_delta
    if is_off_edge(new_col):
        change_bug_direction()
        move_all_bugs_down_one_row()
    else:
        if is_player_bullet(row, new_col):
            make_empty(row, col)
            remove_player_bullet(row, new_col)
            score_player_hit(row)
        elif is_bug_bullet(row, new_col):
            remove_bug_bullet(row, new_col)
            make_bug(row, new_col)
        else:
            make_empty(row, col)
            make_bug(row, new_col)

# Moves a bug to the next row on the board
def move_bug_vertical(row, col):
    new_row = row + 1
    make_empty(row, col)
    if not is_on_board(new_row,col) or new_row == bottom_row():
        canvas.data.is_game_over = True
    else:
        if is_player_bullet(new_row, col):
            make_empty(row, col)
            remove_player_bullet(new_row, col)
            score_player_hit(new_row)
        elif is_bug_bullet(new_row, col):
            remove_bug_bullet(new_row, col)
            move_bug(new_row, col)
        else:
            make_empty(row, col)
            make_bug(new_row, col)

# Changes the direction in which the bugs are marching
def change_bug_direction():
    canvas.data.bugs_changed_direction = True
    if bugs_are_moving_right():
        canvas.data.bug_marching_delta = -1
    else:
        canvas.data.bug_marching_delta = 1

# Determines the direction the bugs are marching
def bugs_are_moving_right():
    return canvas.data.bug_marching_delta == 1

# Moves all of the bugs on the board one row closer to the player
def move_all_bugs_down_one_row():
    for row in range(len(canvas.data.board)-1, -1, -1):
        for col in range(len(canvas.data.board[0])-1, -1, -1):
            if is_bug(row, col):
                move_bug_vertical(row, col)
    if should_make_bug_row():
            make_bug_row()

# Creates a player projectile
def player_shoot():
    if not is_player_out_of_ammo():
        row = canvas.data.player_row
        col = canvas.data.player_col
        make_player_bullet(row-1, col)
        canvas.data.num_player_bullets += 1

# Creates a swarm projectile
def bug_shoot(row, col):
    make_bug_bullet(row+1, col)                

# Moves a player's projectile occupying the row and col.
def move_player_bullet(row, col):
    new_row = row - 1
    if is_on_board(new_row, col):
        if is_bug(new_row, col):
            make_empty(new_row, col)
            remove_player_bullet(row, col)
            score_player_hit(new_row)
        elif is_bug_bullet(new_row, col):
            remove_player_bullet(new_row, col)
            remove_bug_bullet(row, col)
        else:
            make_empty(row, col)
            make_player_bullet(new_row, col)
    else:
        remove_player_bullet(row, col)

# Moves a bug projectile occupying the row and col.
def move_bug_bullet(row, col):
    new_row = row + 1
    if is_on_board(new_row, col):
        if is_player(new_row, col):
            make_empty(new_row, col)
            remove_bug_bullet(row, col)
            canvas.data.is_game_over = True
        elif is_player_bullet(new_row, col):
            remove_player_bullet(new_row, col)
            remove_bug_bullet(row, col)
        elif is_bug(new_row, col):
            remove_bug_bullet(row, col) # Bugs are immune to their own bullets
        else:
            make_empty(row, col)
            make_bug_bullet(new_row, col)
    else:
        remove_bug_bullet(row, col)

# Removes a player's bullet from the board.
def remove_player_bullet(row, col):
    make_empty(row, col)
    canvas.data.num_player_bullets -= 1

# Removes a bug bullet from the board.
def remove_bug_bullet(row, col):
    make_empty(row, col)
    canvas.data.num_bug_bullets -= 1

# Tallies the score of a player's bullet hit.
# The score for a particular hit is judged based
# on how far away from the player's row the hit
# occurred.
def score_player_hit(hit_row):
    canvas.data.score += canvas.data.rows - hit_row

# Determines if the player can move to a given location on the board.
def is_valid_player_move(row, col):
    return is_on_board(row, col) and row == bottom_row()

def is_valid_bug_move(row, col):
    return is_on_board(row, col)

# Determines if a given location is on the board
def is_on_board(row, col):
    return 0 < row < canvas.data.rows and 0 <= col < canvas.data.cols

# Determines if the player is out of ammunition
def is_player_out_of_ammo():
    return canvas.data.max_player_bullets == canvas.data.num_player_bullets

def is_swarm_out_of_ammo():
    return canvas.data.max_bug_bullets == canvas.data.num_bug_bullets

# Determines if a given cell on the board is a bug
def is_bug(row, col):
    return  canvas.data.board[row][col] == canvas.data.bug_color

# Determines if a given coordinate on the board is where the player avatar resides
def is_player(row, col):
    return is_on_board(row, col) and canvas.data.board[row][col] == canvas.data.player_color

def is_player_bullet(row, col):
    return  is_on_board(row, col) and canvas.data.board[row][col] == canvas.data.player_bullet_color

def is_bug_bullet(row, col):
    return canvas.data.board[row][col] == canvas.data.bug_bullet_color

def is_swarm_defeated():
    for row in range(len(canvas.data.board)):
        for col in range(len(canvas.data.board[0])):
            if is_bug(row, col):
                return False
    canvas.data.is_game_over = True
    return True

# Determines if the given column is within the horizontal bounds of the board
def is_off_edge(col):
    return col < 0 or canvas.data.cols <= col

# Re-renders the entire game window
def redraw_all():
    
    # Clear the board
    canvas.delete(ALL)
    
    # Setup text styling
    text_font = "Helvetica "
    text_normal_color = "black"
    text_alert_color = "red"
    text_normal_size = "13 "
    text_alert_size = "26 "

    # Render board
    draw_board()
    if canvas.data.is_game_over or is_swarm_defeated():
        game_over_y = canvas.data.height * 2 / 5
        canvas.create_text(canvas.data.width / 2,
                           game_over_y, text="Game Over Man!",
                           fill=text_alert_color, font=text_font + text_alert_size + " bold")
        canvas.create_text(canvas.data.width / 2,
                           game_over_y + int(text_alert_size) + 5, text="Play Again? (y)",
                           fill=text_alert_color, font=text_font + text_normal_size +" bold")
    canvas.create_text(canvas.data.width / 2,
                       canvas.data.margin / 2,
                       text="Score: " + str(canvas.data.score), 
                       fill=text_normal_color,
                       font=text_font + text_normal_size)

# Fires the game timer
def fire_timer():
    redraw_all()
    if not canvas.data.is_game_over:
        move_bugs()
        fire_bug_bullets()
    canvas.after(canvas.data.delay, fire_timer)

# Increments the projectile loop
def fire_projectile_timer():
    redraw_all()
    if not canvas.data.is_game_over:
        move_player_bullets()
        move_bug_bullets()
    canvas.after(canvas.data.bullet_delay, fire_projectile_timer)

# Fires a bullet from the swarm
def fire_bug_bullets():
    if not is_swarm_out_of_ammo():
        for row in range(len(canvas.data.board)):
            for col in range(len(canvas.data.board[0])):
                if is_last_bug_in_col(row, col) and should_bug_fire(row, col):
                    bug_shoot(row, col)

# Determines, randomly, if a bug should fire
def should_bug_fire(row, col):
    return not is_swarm_out_of_ammo() and canvas.data.bug_fire_rate > random.randint(0, 100)

# Determines if the cell is occupied by the last bug in a column
def is_last_bug_in_col(row, col):
    if is_bug(row, col):
        for row in range(len(canvas.data.board), row, 1):
            if not is_empty(canvas.data.board[row][col]):
                return False
        return True
    return False

# Determines if the given row is the last row in which bugs
# appear on the board.
def is_last_bug_row(row):
    return row == last_bug_row()

# Returns the vertical coordinate of the row closest to the 
# bottom of the board which contains bugs.
def last_bug_row():
    last_row = 0
    for row in range(len(canvas.data.board)):
        if contains_bugs(row):
            last_row = row
    return last_row

# Returns the vertical coordinate of the top row on the board
def top_row():
    return 0

# Returns the vertical coordinate of the bottom row on the board
def bottom_row():
    return len(canvas.data.board) - 1

# Keyboard event interceptor
def key_pressed(event):
    if 'y' == event.keysym:
        init()
    elif not canvas.data.is_game_over:
        if "Left" == event.keysym:
            move_player(0, -1)
        elif "Right" == event.keysym:
            move_player(0, +1)
        elif "space" == event.keysym or "Up" == event.keysym:
            player_shoot()
    redraw_all()

# Run the game
run(30, 20)

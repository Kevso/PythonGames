#!/usr/bin/env python
import Tkinter, tkFont

def run():
    global canvas, canvas_width, canvas_height
    root = Tkinter.Tk()
    canvas_width = 300
    canvas_height = 200
    canvas = Tkinter.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()
    
    class Data: 
        pass
    canvas.data = Data()
    canvas.data.canvas_width = canvas_width
    canvas.data.canvas_height = canvas_height
    init()
    timer_fired()
    root.bind("<Button-1>", mouse_clicked)
    root.bind("<Key>", key_pressed)
    root.mainloop()

def init():
    canvas.data.radius = 10
    canvas.data.score = 0
    canvas.data.cx = 10
    canvas.data.cy = 100
    canvas.data.delay = 10
        
def timer_fired():
    do_timer_fired()
    delay = canvas.data.delay
    canvas.after(delay, timer_fired)
    
def do_timer_fired():
    move_right()
    redraw_all()

def move_right():
    canvas.data.cx += 5
    if canvas.data.cx + canvas.data.radius >= canvas_width:
        canvas.data.cx = canvas.data.radius

def move_left():
    canvas.data.cx -= 5
    if canvas.data.cx - canvas.data.radius <= canvas_width:
        canvas.data.cx = canvas.data.radius

def redraw_all():
    canvas.delete(Tkinter.ALL)
    r = canvas.data.radius
    cx = canvas.data.cx
    cy = canvas.data.cy
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="cyan")
    score  = canvas.data.score
    helv18 = tkFont.Font ( family="Helvetica", size=18, weight="bold" )
    canvas.create_text(150,20, font=helv18, justify="center", text="SCORE = " + str(score) )
    delay_time  = canvas.data.delay
    canvas.create_text(150,50, font=helv18, justify="center", text="Delay = " + str(delay_time)  

def mouse_clicked(event):
    count_score(event)
    redraw_all()

def count_score(event):
    if(is_inside(event)):
        canvas.data.score += 1
    else:
        if(canvas.data.score > 0):
            canvas.data.score -= 1

def is_inside(event):
    x,y = (event.x, event.y)
    cx = canvas.data.cx
    cy = canvas.data.cy
    r = canvas.data.radius
    if(cx-r <= x <= cx+r and cy-r <= y <= cy+r):
        return True
    else:
        return False

def key_pressed(event):
    if(event.keysym == "Up"):
        canvas.data.delay -= 5
    elif(event.keysym == "Down"):
        canvas.data.delay += 5

run()

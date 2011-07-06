#!/usr/bin/env python
import Tkinter, tkFont

class Ball:
    def __init__(self, id, x, y, radius, color="cyan"):
        self.id, self.x, self.y, self.radius, self.color = id, x, y, radius, color
        
    def move_right(self):
        self.x += 5
        if self.x + self.radius >= canvas_width:
            self.x = self.radius

    def move_left(self):
        self.x -= 5
        if self.x - self.radius < 0:
            self.x = canvas_width

    def draw(self):
        canvas.create_oval(self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius, fill=self.color)

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
    canvas.data.delay = 15
    canvas.data.balls = []
    canvas.data.balls += [Ball(id=0, x=0, y=100, radius=10)]
    canvas.data.balls += [Ball(id=1, x=canvas_width, y=100, radius=10)]
        
def timer_fired():
    do_timer_fired()
    delay = canvas.data.delay
    canvas.after(delay, timer_fired)
    
def do_timer_fired():
    canvas.delete(Tkinter.ALL)
    move_balls()
    draw_reports()

def move_balls():
    for ball in canvas.data.balls:
        if ball.id % 2 == 0:
            ball.move_left()
        else:
            ball.move_right()
        ball.draw()
            
def draw_reports():
    score  = canvas.data.score
    helv18 = tkFont.Font ( family="Helvetica", size=18, weight="bold" )
    canvas.create_text(150,20, font=helv18, justify="center", text="SCORE = " + str(score))
    delay_time  = canvas.data.delay
    canvas.create_text(150,50, font=helv18, justify="center", text="Delay = " + str(delay_time))

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
    for ball in canvas.data.balls:
        if(ball.x-ball.radius <= x <= ball.x+ball.radius and ball.y-ball.radius <= y <= ball.y+ball.radius):
            return True
        else:
            return False

def key_pressed(event):
    if(event.keysym == "Up"):
        canvas.data.delay -= 5
    elif(event.keysym == "Down"):
        canvas.data.delay += 5

run()

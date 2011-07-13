# events-sierpinski.py
# Demos timer, mouse, and keyboard events
# as we will use them in Spring 2011's 15-110

from Tkinter import *

def mousePressed(event):
    redrawAll()

def keyPressed(event):
    if ((event.char >= "0") and (event.char <= "9")):
        canvas.data.sierpinskiDepth = ord(event.char) - ord("0")
    redrawAll()

def timerFired():
    pass # do nothing and turn off timerFired, since we don't use it here

# draw a Sierpinski Triangle of the given depth connecting the given points
# of a triangle
def drawSierpinski(depth, x0, y0, x1, y1, x2, y2):
    if (depth <= 0):
        canvas.create_polygon(x0, y0, x1, y1, x2, y2, fill="black")
    else:
        # top triangle
        drawSierpinski(depth-1,
                       x0, y0,
                       average(x0,x1), average(y0,y1),
                       average(x0,x2), average(y0,y2))
        # lower left triangle
        drawSierpinski(depth-1,
                       average(x0,x1), average(y0,y1),
                       x1, y1,
                       average(x1,x2), average(y1, y2))
        # lower right triangle
        drawSierpinski(depth-1,
                       average(x0,x2), average(y0,y2),
                       average(x1,x2), average(y1, y2),
                       x2, y2)

def average(u, v):
    return (u+v)/2

def redrawAll():
    canvas.delete(ALL)
    drawSierpinski(canvas.data.sierpinskiDepth,
                   canvas.data.canvasWidth/2, 0,
                   0, canvas.data.canvasHeight,
                   canvas.data.canvasWidth, canvas.data.canvasHeight)

def init():
    canvas.data.sierpinskiDepth = 1

########### copy-paste below here ###########

def run():
    # create the root and the canvas
    global canvas
    root = Tk()
    canvasWidth = 300
    canvasHeight = 200
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    init()
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired()
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()
1

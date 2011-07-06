#!/usr/bin/env python
import Tkinter
root = Tkinter.Tk()
canvas = Tkinter.Canvas(root, width=300, height=200)
canvas.pack()
canvas.create_rectangle(50, 50, 150, 100, fill="yellow")
#canvas.create_oval(5, 5, 300, 200, fill="green")
#canvas.create_text(150, 100, text="Amazing!", fill="purple", font="Helvetica 26 bold underline")
root.mainloop()

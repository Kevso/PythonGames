#!/usr/bin/env python
import Tkinter

class App:
    def __init__(self, master):
        
        frame = Tkinter.Frame(master)
        frame.pack()

        self.button = Tkinter.Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side=Tkinter.LEFT)

        self.hi_there = Tkinter.Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=Tkinter.LEFT)
    
    def say_hi(self):
        print "Hi there, everyone!"

root = Tkinter.Tk()
app = App(root)
root.mainloop()

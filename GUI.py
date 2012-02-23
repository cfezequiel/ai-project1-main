#!/usr/bin/python
#
# 
#
# Description.
#
# Copyright (c) 2012 Benjamin Geiger <begeiger@mail.usf.edu>

import tkinter as tk

class GUI(object):

    def __init__(self, root):
        frame = tk.Frame(root)
        frame.pack()

        self.canvas = tk.Canvas(frame, width=800, height=800)
        self.canvas.pack(side=tk.LEFT)

        buttonframe = tk.Frame(frame)
        buttonframe.pack(side=tk.LEFT)

        drawbutton = tk.Button(buttonframe, text="Draw", command=self.foo)
        drawbutton.pack(side=tk.TOP)

        quitbutton = tk.Button(buttonframe, text="Quit", command=frame.quit)
        quitbutton.pack(side=tk.TOP)

    def foo(self):
        print("NARF!")

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    
    root.mainloop()


# vim: set et sw=4 ts=4: 

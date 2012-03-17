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
        frame.pack(fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(frame,
                                width=800, height=800,
                                relief=tk.SUNKEN,
                                borderwidth=1)
        self.canvas.pack(side=tk.LEFT,
                         fill=tk.NONE,
                         expand=False)

        sideframe = tk.Frame(frame)
        sideframe.pack(side=tk.RIGHT,
                       fill=tk.BOTH,
                       expand=1)

        buttonframe = tk.Frame(sideframe)
        buttonframe.pack(side=tk.TOP)
        
        previmage = tk.PhotoImage(file="images/left_button.gif")
        nextimage = tk.PhotoImage(file="images/right_button.gif")

        prevbutton = tk.Button(buttonframe,
                               image=previmage,
                               command=self.do_previous)
        prevbutton.image = previmage
        prevbutton.pack(side=tk.LEFT)
        
        nextbutton = tk.Button(buttonframe,
                               image=nextimage,
                               command=self.do_next)
        nextbutton.image = nextimage
        nextbutton.pack(side=tk.RIGHT)

        self.log = tk.Listbox(sideframe)
        self.log.pack(side=tk.BOTTOM,
                      fill=tk.BOTH,
                      expand=1)

        #print(root.geometry())
        #frame.minsize(width=frame.width(), height=frame.height())


    def do_previous(self):
        pass

    def do_next(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    
    root.mainloop()


# vim: set et sw=4 ts=4: 

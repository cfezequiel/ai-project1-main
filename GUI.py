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

        self._initialize_window(root)

    def _initialize_window(self, root):

        # Set minimum size, prevent vertical stretching.
        root.minsize(width=1000, height=800)
        root.resizable(width=True, height=False)



        # On the left, create a canvas.
        self.canvas = tk.Canvas(root,
                                width=800, height=800,
                                relief=tk.SUNKEN,
                                borderwidth=1)
        self.canvas.pack(side=tk.LEFT,
                         fill=tk.NONE,
                         expand=False)

        # Everything else goes in a frame.
        sideframe = tk.Frame(root)
        sideframe.pack(side=tk.RIGHT,
                       fill=tk.BOTH,
                       expand=1)

        # The top of the side frame gets buttons.
        buttonframe = tk.Frame(sideframe)
        buttonframe.pack(side=tk.TOP)
        
        # Images to put in the buttons.
        previmage = tk.PhotoImage(file="images/left_button.gif")
        nextimage = tk.PhotoImage(file="images/right_button.gif")

        # "Previous Step" button.
        prevbutton = tk.Button(buttonframe,
                               image=previmage,
                               command=self.do_previous)
        prevbutton.image = previmage
        prevbutton.pack(side=tk.LEFT)
        
        # "Next Step" button.
        nextbutton = tk.Button(buttonframe,
                               image=nextimage,
                               command=self.do_next)
        nextbutton.image = nextimage
        nextbutton.pack(side=tk.RIGHT)

        # A place to log actions.
        self.log = tk.Listbox(sideframe)
        self.log.pack(side=tk.BOTTOM,
                      fill=tk.BOTH,
                      expand=1)

    # What do we do when they click "previous"?
    def do_previous(self):
        pass

    # What do we do when they click "next"?
    def do_next(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    
    root.mainloop()


# vim: set et sw=4 ts=4: 

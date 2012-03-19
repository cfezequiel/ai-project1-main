#!/usr/bin/python
#
# 
#
# Description.
#
# Copyright (c) 2012 Benjamin Geiger <begeiger@mail.usf.edu>

import tkinter as tk
import tkinter.filedialog as tkfile
from AStarSearch import AStarSearch
from FileParsers import parse_locations_file, parse_connections_file

class GUI(object):

    def __init__ (self, root):
        self.root = root

        self._initialize_menus()
        self._initialize_window()

    
    def _initialize_menus (self):
        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open locations file...",
                             command=self.do_open_locations)
        self.filemenu.add_command(label="Open connections file...",
                             command=self.do_open_connections,
                             state=tk.DISABLED)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Quit",
                             command=self.do_quit)

        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.searchmenu = tk.Menu(self.menubar, tearoff=0)
        self.searchmenu.add_command(label="Start search",
                               command=self.do_reset_search,
                               state=tk.DISABLED)

        self.menubar.add_cascade(label="Search", menu=self.searchmenu)

        self.root.config(menu=self.menubar)


    def _initialize_window (self):

        # Set minimum size, prevent vertical stretching.
        self.root.minsize(width=1000, height=800)
        self.root.resizable(width=True, height=False)



        # On the left, create a canvas.
        self.canvas = tk.Canvas(self.root,
                                width=800, height=800,
                                relief=tk.SUNKEN,
                                borderwidth=1)
        self.canvas.pack(side=tk.LEFT,
                         fill=tk.NONE,
                         expand=False)

        # Everything else goes in a frame.
        sideframe = tk.Frame(self.root)
        sideframe.pack(side=tk.RIGHT,
                       fill=tk.BOTH,
                       expand=1)

        selectorframe = tk.Frame(sideframe)
        selectorframe.pack(side=tk.TOP)

        self.searchmode = tk.IntVar(root)
        #searchmode.set(0)

        distancebutton = tk.Radiobutton(selectorframe,
                                        text="Measure distance",
                                        variable=self.searchmode,
                                        value=0)
        hopsbutton = tk.Radiobutton(selectorframe,
                                    text="Measure hops",
                                    variable=self.searchmode,
                                    value=1)

        distancebutton.pack(side=tk.TOP)
        hopsbutton.pack(side=tk.TOP)

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



    # Callbacks

    # What do we do when they click "previous"?
    def do_previous(self):
        pass

    # What do we do when they click "next"?
    def do_next(self):
        pass

    def do_open_locations(self):
        self.location_file_name = tkfile.askopenfilename()
        self.connection_file_name = None

        try:
            locationsfile = open(self.location_file_name)
        except IOError:
            print("AIEEEE")
            return

        self.cities = parse_locations_file(locationsfile)

        self.filemenu.entryconfig(1, state=tk.NORMAL)
        self.searchmenu.entryconfig(0, state=tk.DISABLED)

    
    def do_open_connections(self):
        self.connection_file_name = tkfile.askopenfilename()

        try:
            connectionsfile = open(self.connection_file_name)
        except IOError:
            print("AIEEEE")
            return

        self.cities = parse_connections_file(connectionsfile, self.cities)
        
        self.searchmenu.entryconfig(0, state=tk.NORMAL)

    def do_reset_search(self):
        self.search_object = AStarSearch()

        # DEBUG. TODO: Replace with actual specification.
        self.search_object.origin = [x for x in self.cities if x.name == "A1"][0]
        self.search_object.destination = [x for x in self.cities if x.name == "G5"][0]
        self.search_object.potholes = [x for x in self.cities if x.name == "B2"] # no index

        if self.searchmode.get() == 0:
            self.search_object.heuristic = lambda x: x.distance_to(self.search_object.destination)
            self.search_object.distance_func = lambda x, y: x.distance_to(y)
        else:
            self.search_object.heuristic = lambda x: 1
            self.search_object.distance_func = lambda x, y: 1

        self.search_object.start_search()

    def do_quit(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    
    root.mainloop()


# vim: set et sw=4 ts=4: 

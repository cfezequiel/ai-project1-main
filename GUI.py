#!/usr/bin/python
#
# 
#
# Description.
#
# Copyright (c) 2012 Benjamin Geiger <begeiger@mail.usf.edu>

import tkinter as tk
import tkinter.filedialog as tkfile
import tkinter.messagebox as tkmsg
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
        self.searchmenu.add_command(label="Start search by distance",
                command=lambda: self.do_start_search("distance"),
                state=tk.DISABLED)
        self.searchmenu.add_command(label="Start search by link count",
                command=lambda: self.do_start_search("linkcount"),
                state=tk.DISABLED)

        self.menubar.add_cascade(label="Search", menu=self.searchmenu)

        self.root.config(menu=self.menubar)


    def _initialize_window (self):

        # Set minimum size, prevent vertical stretching.
        self.root.minsize(width=1000, height=800)
        self.root.resizable(width=True, height=False)

        # Top frame
        self.topframe = tk.Frame(self.root)
        self.topframe.pack(side=tk.TOP)

        # Start city option menu
        startlabel = tk.Label(self.topframe, text="Start city")
        startlabel.pack(side=tk.LEFT)
        self.startcity = tk.StringVar(self.topframe)
        self.startcity.set("")
        self.startoptionmenu = tk.OptionMenu(self.topframe, self.startcity, "")
        self.startoptionmenu.pack(side=tk.LEFT)

        # End city option menu
        endlabel = tk.Label(self.topframe, text="End city")
        endlabel.pack(side=tk.LEFT)
        self.endcity = tk.StringVar(self.topframe)
        self.endcity.set("")
        self.endoptionmenu = tk.OptionMenu(self.topframe, self.endcity, "")
        self.endoptionmenu.pack(side=tk.LEFT)

        # On the left, create a canvas.
        canvasframe = tk.Frame(self.root)
        canvasframe.pack(side=tk.LEFT)
        self.canvas = tk.Canvas(canvasframe,
                                width=800, height=800,
                                relief=tk.SUNKEN,
                                borderwidth=1)
        self.canvas.pack(side=tk.LEFT,
                         fill=tk.NONE,
                         expand=False)

        # On the right, we have the side panel.
        sideframe = tk.Frame(self.root)
        sideframe.pack(side=tk.RIGHT,
                       fill=tk.BOTH,
                       expand=1)

        # The top of the side frame gets buttons.
        buttonframe = tk.Frame(sideframe)
        buttonframe.pack(side=tk.TOP)
        
        # Images to put in the buttons.
        #previmage = tk.PhotoImage(file="images/left_button.gif")
        nextimage = tk.PhotoImage(file="images/right_button.gif")

        # "Previous Step" button.
        #prevbutton = tk.Button(buttonframe,
        #                       image=previmage,
        #                       command=self.do_previous)
        #prevbutton.image = previmage
        #prevbutton.pack(side=tk.LEFT)
        
        # "Next Step" button.
        self.nextbutton = tk.Button(buttonframe,
                               image=nextimage,
                               command=self.do_next,
                               state=tk.DISABLED)
        self.nextbutton.image = nextimage
        self.nextbutton.pack(side=tk.RIGHT)

        # A place to log actions.
        logframe = tk.Frame(sideframe)
        logframe.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        logscroll = tk.Scrollbar(logframe, orient=tk.VERTICAL)
        self.log = tk.Listbox(logframe, yscrollcommand=logscroll.set)
        logscroll.config(command=self.log.yview)
        logscroll.pack(side=tk.RIGHT, fill=tk.Y, expand=0)
        self.log.pack(side=tk.LEFT,
                      fill=tk.BOTH,
                      expand=1)



    # Callbacks

    # What do we do when they click "previous"?
    def do_previous(self):
        pass

    # What do we do when they click "next"?
    def do_next(self):
        # Slow way but it works.

        if self.search_object is None: return

        current_road, total_distance, distance, estimate = self.search_object.next_step()

        if current_road is None:
            # Hooray, we found it.

            for road in self.search_object.generate_path_from(self.current_city):
                road.highlight()

            self.nextbutton.config(state=tk.DISABLED)
            return

        for road in current_road.destination.neighbors:
            road.probe()
        current_road.travel()

        self.current_city = current_road.destination

        if current_road.origin is None:
            self.log_message("Beginning search at " + current_road.destination.name)
        else:
            self.log_message("Going from " + current_road.origin.name + " to " + current_road.destination.name)
            self.log_message("Total distance traveled: " + str(distance + total_distance))
            self.log_message("Estimated distance from " + current_road.destination.name + ": " + str(estimate))

    def do_open_locations(self):
        newfilename = tkfile.askopenfilename()
        if not newfilename:
            return
        self.location_file_name = newfilename
        self.connection_file_name = None

        try:
            locationsfile = open(self.location_file_name)
        except IOError:
            print(repr(self.location_file_name))
            tkmsg.showwarning("Error", "Error loading locations file.")
            return

        self.cities = parse_locations_file(locationsfile)

        for city in self.cities:
            city.draw(self.canvas)
        
        self.log_message("Loaded " + str(len(self.cities)) + " cities.")

        self.filemenu.entryconfig(1, state=tk.NORMAL)
        self.searchmenu.entryconfig(0, state=tk.DISABLED)
        self.searchmenu.entryconfig(1, state=tk.DISABLED)

        citynames = [x.name for x in self.cities]

        # Add cities to the start and end city option menus
        # Remove 'dummy' menu items
        self.startoptionmenu['menu'].delete(0, 'end')
        self.endoptionmenu['menu'].delete(0, 'end')

        def startcallback(item):
            # FIXME: might not need line below
            #self.startoptionmenu.configure(text=item)
            self.startcity.set(item)

        def endcallback(item):
            # FIXME: might not need line below
            #self.endoptionmenu.configure(text=item)
            self.endcity.set(item)

        for city in citynames:
            self.startoptionmenu['menu'].add_command(label=city, \
                command=lambda item=city: startcallback(item))

            self.endoptionmenu['menu'].add_command(label=city, \
                command=lambda item=city: endcallback(item))

        # Set default start and end cities
        self.startcity.set(citynames[0])
        self.endcity.set(citynames[0])


    def do_open_connections(self):
        newfilename = tkfile.askopenfilename()
        if newfilename == ():
            return
        self.connection_file_name = newfilename

        try:
            connectionsfile = open(self.connection_file_name)
        except IOError:
            tkmsg.showwarning("Error", "Error loading connections file.")
            return

        for city in self.cities:
            city.neighbors = []

        self.cities = parse_connections_file(connectionsfile, self.cities)

        roadcount = 0
        for city in self.cities:
            roadcount += len(city.neighbors)

        for city in self.cities:
            for road in city.neighbors:
                road.draw(self.canvas)

        self.log_message("Loaded " + str(roadcount) + " roads.")

        self.searchmenu.entryconfig(0, state=tk.NORMAL)
        self.searchmenu.entryconfig(1, state=tk.NORMAL)

    def do_start_search (self, method): 
        self.search_object = AStarSearch()

        # DEBUG. TODO: Replace with actual specification.
        self.search_object.origin = [x for x in self.cities if x.name == self.startcity.get()][0]
        self.search_object.destination = [x for x in self.cities if x.name == self.endcity.get()][0]
        self.search_object.potholes = [x for x in self.cities if x.name == "B2"] # no index

        if method == "distance":
            self.search_object.heuristic = lambda x: x.distance_to(self.search_object.destination)
            self.search_object.distance_func = lambda x, y: x.distance_to(y)
        elif method == "linkcount":
            self.search_object.heuristic = lambda x: 1
            self.search_object.distance_func = lambda x, y: 1

        for city in self.cities:
            for road in city.neighbors:
                road.reset()
        self.nextbutton.config(state=tk.NORMAL)

        self.search_object.start_search()

    def do_quit(self):
        self.root.quit()

    def log_message (self, message):
        self.log.insert(tk.END, message)
        self.log.see(tk.END)

    def undraw_all (self):
        for obj in self.canvas.find_all():
            self.canvas.delete(obj)



if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    
    root.mainloop()


# vim: set et sw=4 ts=4: 

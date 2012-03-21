#!/usr/bin/python
#
# 
#
# /file GUI.py
#
# Copyright (c) 2012 
#
# Benjamin Geiger <begeiger@mail.usf.edu>
# Carlos Ezequiel <cfezequiel@mail.usf.edu>

"""Graphical User Interface for the A* Algorithm."""

import tkinter as tk
import tkinter.filedialog as tkfile
import tkinter.messagebox as tkmsg
from AStarSearch import AStarSearch
from FileParsers import parse_locations_file, parse_connections_file

class GUI(object):

    def __init__ (self, root):
        """Initialize all GUI widgets."""
        self.root = root
        self.root.title("A* Algorithm")

        self._initialize_menus()
        self._initialize_window()

    
    def _initialize_menus (self):
        """Initialize menu bar items."""

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
        """Initialize window widgets."""

        # Set minimum size, prevent vertical stretching.
        self.root.minsize(width=1200, height=800)
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

        # Excluded cities entry
        excludelabel = tk.Label(self.topframe, text="Excluded cities")
        excludelabel.pack(side=tk.LEFT)
        self.excludeentry = tk.Entry(self.topframe)
        self.excludeentry.pack(side=tk.LEFT)

        # Excluded cities update button
        self.excludebutton = tk.Button(self.topframe, 
                                       text = 'Update', 
                                       state=tk.DISABLED,
                                       command=self.do_update_excluded_cities)
        self.excludebutton.pack(side=tk.LEFT)

        # Clear excluded cities button
        self.clearexcludebutton = tk.Button(self.topframe, 
                                            text = 'Clear all', 
                                            state=tk.DISABLED,
                                            command=self.do_clear_all_exclusions)
        self.clearexcludebutton.pack(side=tk.LEFT)

        # On the left, create a canvas.
        canvasframe = tk.Frame(self.root)
        canvasframe.pack(side=tk.LEFT)
        self.canvas = tk.Canvas(canvasframe,
                                width=910, height=800,
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
        playimage = tk.PhotoImage(file="images/play_button.gif")
        nextimage = tk.PhotoImage(file="images/next_button.gif")

        # "Play" button.
        self.playbutton = tk.Button(buttonframe,
                               image=playimage,
                               command=self.do_play,
                               state=tk.DISABLED)
        self.playbutton.image = playimage
        self.playbutton.pack(side=tk.LEFT)
        
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

    def do_next(self):
        """Search the next adjacent cities for the next best path."""

        if self.search_object is None: return

        current_road, total_distance, distance, estimate = self.search_object.next_step()

        if current_road is None:
            # Hooray, we found it.

            for road in self.search_object.generate_path_from(self.current_city):
                road.highlight()

            self.nextbutton.config(state=tk.DISABLED)
            self.playbutton.config(state=tk.DISABLED)
            return 0

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

        return 1

    def do_open_locations(self):
        """Open the locations file and extract city locations."""

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

        # Add cities to the start and end city option menus
        citynames = [x.name for x in self.cities]

        # Remove 'dummy' menu items
        self.startoptionmenu['menu'].delete(0, 'end')
        self.endoptionmenu['menu'].delete(0, 'end')

        # Add each city as a menu item
        for city in citynames:
            self.startoptionmenu['menu'].add_command(label=city, \
                command=lambda item=city: self.do_set_start_city(item))

            self.endoptionmenu['menu'].add_command(label=city, \
                command=lambda item=city: self.do_set_end_city(item))

        # Set default start and end cities
        self.do_set_start_city(citynames[0])
        self.do_set_end_city(citynames[0])

        # Enable exclude button
        self.excludebutton.config(state=tk.NORMAL)
        self.clearexcludebutton.config(state=tk.NORMAL)

    def do_set_start_city(self, cityname):
        """Set a new origin city on the canvas."""

        self.startcity.set(cityname)
        try:
            prevstartcity = [x for x in self.cities if x.state == 'starting'][0]
            prevstartcity.set_normal()
            prevstartcity.draw(self.canvas)
        except IndexError:
            pass
        city = [x for x in self.cities if x.name == cityname][0]
        city.set_starting()
        city.draw(self.canvas)

    def do_set_end_city(self, cityname):
        """Set a new destination city on the canvas."""

        self.endcity.set(cityname)
        try:
            prevendcity = [x for x in self.cities if x.state == 'ending'][0]
            prevendcity.set_normal()
            prevendcity.draw(self.canvas)
        except IndexError:
            pass
        city = [x for x in self.cities if x.name == cityname][0]
        city.set_ending()
        city.draw(self.canvas)

    def do_open_connections(self):
        """Open the connections file and extract roads connecting cities."""

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
        """Start the search algorithm based on the given method.

        Supported methods:
            'distance'  Straight-line distance
            'linkcount' Shortest-hop-count 
           
        """


        self.search_object = AStarSearch()

        self.search_object.origin = [x for x in self.cities if x.name == self.startcity.get()][0]
        self.search_object.destination = [x for x in self.cities if x.name == self.endcity.get()][0]
        self.search_object.potholes = [x for x in self.cities if x.state == "blocking"] # no index

        if method == "distance":
            self.search_object.heuristic = lambda x: x.distance_to(self.search_object.destination)
            self.search_object.distance_func = lambda x, y: x.distance_to(y)
        elif method == "linkcount":
            self.search_object.heuristic = lambda x: 1
            self.search_object.distance_func = lambda x, y: 1

        for city in self.cities:
            for road in city.neighbors:
                road.reset()

        # Enable search buttons
        self.nextbutton.config(state=tk.NORMAL)
        self.playbutton.config(state=tk.NORMAL)

        self.search_object.start_search()

    def do_play(self):
        """Run the entire search algorithm."""

        while self.do_next():
            continue

    def do_update_excluded_cities(self):
        """Update the states of the selected cities in the entry field to
           "blocking".
        """

        entry = self.excludeentry.get()
        blockedcities = "".join(entry.split()).split(',')
        for city in self.cities:
            if city.name in blockedcities:
                city.set_blocking()
            elif city.state == "blocking":
                city.set_normal()
            city.draw(self.canvas)

    def do_clear_all_exclusions(self):
        """Set all 'blocking' cities to 'normal'."""

        for city in self.cities:
            if city.state == "blocking":
                city.set_normal()
                city.draw(self.canvas)

    def do_quit(self):
        """Exit program."""

        self.root.quit()

    def log_message (self, message):
        """Prints out a message to the log window."""

        self.log.insert(tk.END, message)
        self.log.see(tk.END)

    def undraw_all (self):
        """Removes all objects in the canvas."""

        for obj in self.canvas.find_all():
            self.canvas.delete(obj)

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    
    root.mainloop()


# vim: set et sw=4 ts=4: 

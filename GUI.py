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


        # Yes, this code is fugly.

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
        self.searchmenu.add_command(label="Stop search",
                command=self.do_stop_search,
                state=tk.DISABLED)

        self.menubar.add_cascade(label="Search", menu=self.searchmenu)

        self.root.config(menu=self.menubar)




    def _initialize_window (self):
        """Initialize window widgets."""

        # Set minimum size, prevent vertical stretching.
        self.root.minsize(width=1200, height=800)
        self.root.resizable(width=True, height=False)

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
        buttonframe.pack(side=tk.TOP, fill=tk.X)
        buttonframe.grid_columnconfigure(2, weight=1)

        # Start city option menu
        startlabel = tk.Label(buttonframe, text="Start city")
        startlabel.grid(row=0, column=0)
        self.startcity = tk.StringVar(buttonframe)
        self.startcity.set("")
        self.startoptionmenu = tk.OptionMenu(buttonframe, self.startcity, "")
        self.startoptionmenu.grid(row=0, column=1)

        # End city option menu
        endlabel = tk.Label(buttonframe, text="End city")
        endlabel.grid(row=1, column=0)
        self.endcity = tk.StringVar(buttonframe)
        self.endcity.set("")
        self.endoptionmenu = tk.OptionMenu(buttonframe, self.endcity, "")
        self.endoptionmenu.grid(row=1, column=1)

        # Images to put in the buttons.
        playimage = tk.PhotoImage(file="images/play_button.gif")
        nextimage = tk.PhotoImage(file="images/next_button.gif")

        # "Play" button.
        self.playbutton = tk.Button(buttonframe,
                               image=playimage,
                               command=self.do_play,
                               state=tk.DISABLED)
        self.playbutton.image = playimage
        self.playbutton.grid(row=0, rowspan=2, column=3)
        
        # "Next Step" button.
        self.nextbutton = tk.Button(buttonframe,
                               image=nextimage,
                               command=self.do_next,
                               state=tk.DISABLED)
        self.nextbutton.image = nextimage
        self.nextbutton.grid(row=0, rowspan=2, column=4)

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




    def enable_search_GUI (self):
        """Enable the widgets having to do with search."""

        # Enable search buttons
        self.nextbutton.config(state=tk.NORMAL)
        self.playbutton.config(state=tk.NORMAL)
        for city in self.cities:
            city.lock_state()
        
        # Enable/disable search menu items
        self.searchmenu.entryconfig(0, state=tk.DISABLED)
        self.searchmenu.entryconfig(1, state=tk.DISABLED)
        self.searchmenu.entryconfig(2, state=tk.NORMAL)

    def disable_search_GUI (self):
        """Disable the widgets having to do with search."""

        # Disable search buttons
        self.nextbutton.config(state=tk.DISABLED)
        self.playbutton.config(state=tk.DISABLED)
        for city in self.cities:
            city.unlock_state()

        # Enable/disable search menu items
        self.searchmenu.entryconfig(0, state=tk.NORMAL)
        self.searchmenu.entryconfig(1, state=tk.NORMAL)
        self.searchmenu.entryconfig(2, state=tk.DISABLED)





    # Callbacks

    def do_next(self):
        """Search the next adjacent cities for the next best path."""
        
        # If somehow we got here without a valid search object,
        # disable the button and stop.
        if self.search_object is None:
            self.disable_search_GUI()
            return

        # Run one iteration of the algorithm, and get information back.
        try:        
            current_road, total_distance, distance, estimate = self.search_object.next_step()
        
        # The code throws a RuntimeError if no route exists.
        except RuntimeError as ex:
            self.disable_search_GUI()
            tkmsg.showerror(
                    "Invalid Search State", 
                    "No valid route exists between the selected cities.")
            return

        # If the current road is None, we've reached the end.
        if current_road is None:
            # Hooray, we found it.
            
            # Now that the search is over, disable the search buttons.
            self.disable_search_GUI()

            # Highlight the roads we've traveled.
            for road in self.search_object.generate_path_from(self.current_city):
                road.highlight()

            return 0
        else:
            # Keep this information for the next iteration if needed.
            self.current_city = current_road.destination

        # Otherwise, show all neighboring roads as probed.
        for road in current_road.destination.neighbors:
            road.probe()
        # Mark the current road as being traveled.
        current_road.travel()

        # Dump some information to the log.
        if current_road.origin is None:
            self.log_message("Beginning search at " + current_road.destination.name)
        else:
            self.log_message("Going from " + current_road.origin.name + " to " + current_road.destination.name)
            self.log_message("Total distance traveled: %.2f" % total_distance)
            self.log_message("Estimated distance from " + current_road.destination.name + ": %.2f" % estimate)
        return 1





    def do_open_locations(self):
        """Open the locations file and extract city locations."""

        # Get the filename.
        newfilename = tkfile.askopenfilename()
        # If they press "cancel", skip the rest.
        if not newfilename:
            return

        # Set the filenames; setting location should clear connections.
        self.location_file_name = newfilename
        self.connection_file_name = None

        # Try to open the file.
        try:
            locationsfile = open(self.location_file_name)
        # Complain if the file can't be opened.
        except IOError:
            print(repr(self.location_file_name))
            tkmsg.showerror("Error", "Error loading locations file.")
            return

        # Read the cities from the file.
        self.cities = parse_locations_file(locationsfile)

        # Clear the old cities from the canvas.
        self.canvas.delete(tk.ALL)

        # Draw all of the cities.
        for city in self.cities:
            city.draw(self.canvas)
        
        # Show some log information.
        self.log_message("Loaded " + str(len(self.cities)) + " cities.")

        # Set states of menu items.
        self.filemenu.entryconfig(1, state=tk.NORMAL)
        self.searchmenu.entryconfig(0, state=tk.DISABLED)
        self.searchmenu.entryconfig(1, state=tk.DISABLED)

        # Add cities to the start and end city option menus
        citynames = sorted([x.name for x in self.cities])

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
        self.startcity.set(citynames[0])
        self.endcity.set(citynames[-1])
        self.do_set_endpoint_cities()

        # Enable exclude button
        #self.excludebutton.config(state=tk.NORMAL)
        #self.clearexcludebutton.config(state=tk.NORMAL)


    def do_set_start_city (self, city):
        self.startcity.set(city)
        self.do_set_endpoint_cities()

    def do_set_end_city (self, city):
        self.endcity.set(city)
        self.do_set_endpoint_cities()

    def do_set_endpoint_cities(self):
        """Update origin and destination cities on the canvas."""

        prevcities = [x for x in self.cities if x.state in ['starting', 'ending']]
        for city in prevcities:
            city.set_normal()
            city.draw(self.canvas)
       
        startcity = [x for x in self.cities if x.name == self.startcity.get()][0]
        startcity.set_starting()
        startcity.draw(self.canvas)

        endcity = [x for x in self.cities if x.name == self.endcity.get()][0]
        endcity.set_ending()
        endcity.draw(self.canvas)





    def do_open_connections(self):
        """Open the connections file and extract roads connecting cities."""

        # Get the filename.
        newfilename = tkfile.askopenfilename()
        # If they cancel, cancel.
        if not newfilename:
            return
        self.connection_file_name = newfilename

        # Try to open the file.
        try:
            connectionsfile = open(self.connection_file_name)
        # And complain if we can't.
        except IOError:
            tkmsg.showerror("Error", "Error loading connections file.")
            return

        # Get rid of any previous connections.
        for city in self.cities:
            city.neighbors = []

        # Load new connections from the file.
        self.cities = parse_connections_file(connectionsfile, self.cities)

        # Count the number of connections we just loaded and log it.
        roadcount = 0
        for city in self.cities:
            roadcount += len(city.neighbors)
        self.log_message("Loaded " + str(roadcount) + " roads.")

        # Draw the new connections onto the canvas.
        for city in self.cities:
            for road in city.neighbors:
                road.draw(self.canvas)

        # Let the user start a search.
        self.searchmenu.entryconfig(0, state=tk.NORMAL)
        self.searchmenu.entryconfig(1, state=tk.NORMAL)





    def do_start_search (self, method): 
        """Start the search algorithm based on the given method.

        Supported methods:
            'distance'  Straight-line distance
            'linkcount' Shortest-hop-count 
        """

        # Check for a zero-length trip.
        if self.startcity.get() == self.endcity.get():
            tkmsg.showwarning("Invalid Search State", "The start and end cities cannot be the same.")
            return

        # Create a search object...
        self.search_object = AStarSearch()

        # ... and fill its attributes.
        self.search_object.origin = [x for x in self.cities if x.name == self.startcity.get()][0]
        self.search_object.destination = [x for x in self.cities if x.name == self.endcity.get()][0]
        self.search_object.potholes = [x for x in self.cities if x.state == "blocking"] # no index


        # Here is where we choose a heuristic and distance function.
        if method == "distance":
            self.search_object.heuristic = lambda x: x.distance_to(self.search_object.destination)
            self.search_object.distance_func = lambda x, y: x.distance_to(y)
        elif method == "linkcount":
            self.search_object.heuristic = lambda x: 1
            # Distance function: One per hop (skipping the first "road" which isn't really there).
            self.search_object.distance_func = lambda x, y: (x is not None and y is not None) and 1 or 0

        # Redraw all the roads as un-probed.
        for city in self.cities:
            for road in city.neighbors:
                road.reset()

        # Enable the buttons for searching.
        self.enable_search_GUI()

        # Get the search object working.
        self.search_object.start_search()




    def do_stop_search (self):
        """Stop the search algorithm, returning control to the user."""

        self.search_object = None

        self.disable_search_GUI()


    def do_play(self):
        """Run the entire search algorithm."""

        while self.do_next():
            continue



    def do_quit(self):
        """Exit program."""

        self.root.quit()




    def log_message (self, message):
        """Prints out a message to the log window."""

        self.log.insert(tk.END, message)
        self.log.see(tk.END)


# Run this part only if this file is run from the command line.
if __name__ == "__main__":
    # Create a Tk instance.
    root = tk.Tk()

    # Start our GUI.
    gui = GUI(root)
    
    # And start the event loop.
    root.mainloop()


# vim: set et sw=4 ts=4: 

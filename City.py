#!/usr/bin/python
#
# 
#
# /file City.py
#
# Copyright (c) 2012 
#
# Benjamin Geiger <begeiger@mail.usf.edu>
# Carlos Ezequiel <cfezequiel@mail.usf.edu>

from math import sqrt
import GraphUtil


class City (object):
    """Represents a City node.

    Class attributes:
        counter  Index on the number of City objects created. 
                 This is used as an identifier for an 'unnamed' city.

    Object attributes:
        location Point object representing the center
        radius   Radius of the City
        figure   Graphical representation of the city (default: Circle)
        label    Text object for displaying city name
        name     City name
        x        X-coordinate of the city center
        y        Y-coordinate of the city center
        neighbors List of adjacent cities connected by a road
        state    The City's state (i.e. starting, ending, blocking)
                
    """

    counter = 0

    def __init__(self, name = None, x = 0, y = 0, neighbors = None):
        self.location = GraphUtil.Point(x, y)
        self.radius = len(name) * 4
        self.figure = GraphUtil.Circle(self.location, self.radius)
        self.figure.setFill("white")
        self.label = GraphUtil.Text(self.location, name)
        self.label.setSize(8)
        
        # If they don't give us a name, assign an arbitrary name.
        if name is None:
            self.name = "Unnamed City #" + str(City.counter)
            City.counter += 1
        else:
            self.name = name

        # Set the rest of the variables.
        self.x = x
        self.y = y
        self.neighbors = neighbors or []

        # State (start, end or blocking)
        self.state = "normal"

    # Compute distance to another city.
    def distance_to(self, other):
        """Returns the Euclidean distance from this City to another City."""

        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def draw(self, canvas):
        """Draws this object on the given canvas."""

        self.figure.canvas = canvas
        self.figure.draw()
        self.label.canvas = canvas
        self.label.draw()
        canvas.tag_bind(self.figure.id, "<Button-1>", self.change_state)
        canvas.tag_bind(self.label.id, "<Button-1>", self.change_state)

    def set_normal (self):
        """Sets this City as 'normal'."""

        self.state = "normal"
        self.figure.setFill("white")

    def set_starting (self):
        """Sets this City as the origin."""

        self.state = "starting"
        self.figure.setFill("green")

    def set_ending (self):
        """Sets this City as the destination."""

        self.state = "ending"
        self.figure.setFill("red")

    def set_blocking (self):
        """Mark this City to be avoided."""

        self.state = "blocking"
        self.figure.setFill("black")

    def change_state (self, event):
        """Change this City's state according to the given event."""

        if self.state == "normal":
            self.set_blocking()
        elif self.state == "blocking":
            self.set_normal()
        else:
            print("lolwut")

    # Control how the object looks when it's printed.
    def __repr__(self):
        return "City(" + self.name + ", " + str(self.x) + ", " + str(self.y) + ")"


if __name__ == "__main__":
    pass
# vim: set et sw=4 ts=4: 

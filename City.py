#!/usr/bin/python
#
# 
#
# Description.
#
# Copyright (c) 2012 Benjamin Geiger <begeiger@mail.usf.edu>

from math import sqrt
import GraphUtil


# City
class City (object):
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
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def draw(self, canvas):
        self.figure.canvas = canvas
        self.figure.draw()
        self.label.canvas = canvas
        self.label.draw()

    def set_normal (self):
        self.state = "normal"
        self.figure.setFill("white")

    def set_starting (self):
        self.state = "starting"
        self.figure.setFill("green")

    def set_ending (self):
        self.state = "ending"
        self.figure.setFill("red")

    def set_blocking (self):
        self.state = "blocking"
        self.figure.setFill("black")

    # Control how the object looks when it's printed.
    def __repr__(self):
        return "City(" + self.name + ", " + str(self.x) + ", " + str(self.y) + ")"


if __name__ == "__main__":
    pass
# vim: set et sw=4 ts=4: 

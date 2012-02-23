#!/usr/bin/python
#
# 
#
# Description.
#
# Copyright (c) 2012 Benjamin Geiger <begeiger@mail.usf.edu>

from math import sqrt

# City
class City (object):
    counter = 0

    def __init__(self, name = None, x = 0, y = 0, neighbors = None):
        
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

    # Compute distance to another city.
    def distance_to(self, other):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    # Control how the object looks when it's printed.
    def __repr__(self):
        return "City(" + self.name + ", " + str(self.x) + ", " + str(self.y) + ")"


if __name__ == "__main__":
	print("Insert unit test here.")

# vim: set et sw=4 ts=4: 

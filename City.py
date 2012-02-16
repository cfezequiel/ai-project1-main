#!/usr/bin/python
#
# 
#
# Description.
#
# Copyright (c) 2012 Benjamin Geiger <begeiger@mail.usf.edu>

from math import sqrt

class City (object):
    counter = 0

    def __init__(self, name = None, x = 0, y = 0, neighbors = None):
        if name is None:
            self.name = "Unnamed City #" + str(City.counter)
            City.counter += 1
        else:
            self.name = name
        self.x = x
        self.y = y
        self.neighbors = neighbors or []

    def distance_to(self, other):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __repr__(self):
        return "City: " + self.name


if __name__ == "__main__":
	print("Insert unit test here.")

# vim: set et sw=4 ts=4: 

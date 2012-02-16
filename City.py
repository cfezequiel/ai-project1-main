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
        self.name = name or ("City #" + str(counter)); counter = counter + 1
        self.x = x
        self.y = y
        self.neighbors = neighbors or []

    def distance_to(self, other):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


if __name__ == "__main__":
	print("Insert unit test here.")

# vim: set et sw=4 ts=4: 

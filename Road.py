#!/usr/bin/python
#
# 
#
# Description.
#
# Copyright (c) 2012 Benjamin Geiger <begeiger@mail.usf.edu>

from math import cos, sin, atan2
import GraphUtil

class Road (object):
    
    def __init__ (self, origin, destination):
        self.origin = origin
        self.destination = destination

        self.line = GraphUtil.Line(self.origin.location, self.destination.location)
        self.line.setArrow("last")

if __name__ == "__main__":
	print("Insert unit test here.")

# vim: set et sw=4 ts=4: 

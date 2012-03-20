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

        self.create_line()

    def create_line (self):
        x1 = self.origin.location.x
        y1 = self.origin.location.y
        r1 = self.origin.radius
        x2 = self.destination.location.x
        y2 = self.destination.location.y
        r2 = self.destination.radius

        theta = atan2(y2 - y1, x2 - x1)

        dx1 = r1 * cos(theta)
        dy1 = r1 * sin(theta)

        dx2 = r2 * cos(theta)
        dy2 = r2 * sin(theta)

        self.line = GraphUtil.Line(
                GraphUtil.Point(x1 + dx1, y1 + dy1), 
                GraphUtil.Point(x2 - dx2, y2 - dy2))
        self.line.setArrow("last")

if __name__ == "__main__":
	print("Insert unit test here.")

# vim: set et sw=4 ts=4: 

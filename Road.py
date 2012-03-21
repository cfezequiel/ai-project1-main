#!/usr/bin/python
#
# 
#
# /file Road.py
#
# Copyright (c) 2012 
#
# Benjamin Geiger <begeiger@mail.usf.edu>
# Carlos Ezequiel <cfezequiel@mail.usf.edu>


from math import cos, sin, atan2
import GraphUtil

class Road (object):
    """Represents the connection between two City objects."""
    
    def __init__ (self, origin, destination):
        self.origin = origin
        self.destination = destination

        self.create_line()

    def create_line (self):
        """Creates the graphical representation of the road as a line object."""

        # If origin and destination are not specified, set the line to None
        if self.origin is None or self.destination is None:
            self.line = None
        else:
            # Get the center coordinates of both origin and destination
            # As well as their radius
            x1 = self.origin.location.x
            y1 = self.origin.location.y
            r1 = self.origin.radius
            x2 = self.destination.location.x
            y2 = self.destination.location.y
            r2 = self.destination.radius

            # Compute x,y offsets so that that the line touches the boundaries
            # of origin and destination and not their centers
            theta = atan2(y2 - y1, x2 - x1)

            dx1 = r1 * cos(theta)
            dy1 = r1 * sin(theta)

            dx2 = r2 * cos(theta)
            dy2 = r2 * sin(theta)

            # Create the line
            self.line = GraphUtil.Line(
                    GraphUtil.Point(x1 + dx1, y1 + dy1), 
                    GraphUtil.Point(x2 - dx2, y2 - dy2))
            self.line.setArrow("last")
        
        self.reset()

    def draw (self, canvas):
        """Draws this object on the specified canvas."""

        self.line.canvas = canvas

        if self.status == "unprobed":
            self.line.setOutline("gray")
        elif self.status == "probed":
            self.line.setOutline("black")
        elif self.status == "traveled":
            self.line.setOutline("blue")
        else:
            self.line.setOutline("green")

        self.line.draw()

    def reset (self):
        """Resets the road state.

        This sets the road state to 'unprobed'.
        
        """

        self.status = "unprobed"
        if self.line is not None and self.line.canvas is not None:
            self.line.setOutline("gray")
            self.line.setWidth(1)

    def probe (self):
        """If the road state is 'unprobed', this sets the state to 'probed'."""

        if self.status == "unprobed":
            if self.line.canvas is not None:
                self.line.setOutline("black")
                self.line.setWidth(1)
                self.line.canvas.lift(self.line.id)
            self.status = "probed"

    def travel (self):
        """If the road state is 'probed', this sets the state to 'traveled'."""
        if self.status == "probed":
            if self.line.canvas is not None:
                self.line.setOutline("blue")
                self.line.setWidth(2)
                self.line.canvas.lift(self.line.id)
            self.status = "traveled"

    def highlight (self):
        """Highlights the road."""

        if self.line.canvas is not None:
            self.line.setOutline("red")
            self.line.setWidth(4)
            self.line.canvas.lift(self.line.id)

if __name__ == "__main__":
	print("Insert unit test here.")

# vim: set et sw=4 ts=4: 

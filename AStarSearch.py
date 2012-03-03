#!/usr/bin/python
#
# 
#
# Description.
#
# Copyright (c) 2012 Benjamin Geiger <begeiger@mail.usf.edu>


class AStarSearch (object):
    """Represents an A* search on a graph.
    
    Implementation adapted from pseudocode found on:
    http://en.wikipedia.org/wiki/A*_search_algorithm
    (Retrieved 16 February 2012)"""

    def __init__ (self, origin, destination, heuristic, distance_func = None, ghetto=[]):
        self.origin = origin
        self.destination = destination
        self.ghetto = ghetto

        self.heuristic = heuristic
        self.distance_func = distance_func or lambda x, y: x.distance_to(y)

        self.openset = [(origin, 0, heuristic(origin), None)]
        self.closedset = []

    def run_to_end (self):


        

if __name__ == "__main__":
	print("Insert unit test here.")

# vim: set et sw=4 ts=4: 

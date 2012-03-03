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
        self.ghetto = ghetto # TODO: find a non-racist name for this.

        self.heuristic = heuristic
        self.distance_func = distance_func or lambda x, y: x.distance_to(y)

        self._frontier = [(origin, 0, heuristic(origin), None)]
        self._explored = []

    def run_to_end (self):
        """Convenience method to find the shortest path.
        
        Also serves as a programming-by-wishful-thinking setup, so I know
        which functions I still need to write."""

        while self.frontier_size() > 0:
            # Should we make these variables class-level? Probably.
            current_node, distance, estimate = self.get_next_node()
            if current_node == None:
                raise Exception # This really shouldn't happen.
            if current_node == destination:
                return self.generate_path_from(current_node)

            for neighbor in self.get_neighbors(current_node):
                n_distance = self.distance_func(current_node, neighbor)

                self.update_frontier(current_node, neighbor, distance)

        raise Exception # No route from start to end.




        

if __name__ == "__main__":
	print("Insert unit test here.")

# vim: set et sw=4 ts=4: 

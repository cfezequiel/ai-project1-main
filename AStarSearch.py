#!/usr/bin/python
#
# 
#
# Description.
#
# Copyright (c) 2012 Benjamin Geiger <begeiger@mail.usf.edu>

from Road import Road
from City import City

class AStarSearch (object):
    """Represents an A* search on a graph.
    
    Implementation adapted from pseudocode found on:
    http://en.wikipedia.org/wiki/A*_search_algorithm
    (Retrieved 16 February 2012)"""

    def __init__ (self,
            origin = None,
            destination = None, 
            heuristic = None,
            distance_func = None,
            potholes = None):
        """Initialize the search.

        origin: Start of search.
        destination: End of search.
        heuristic: A* heuristic, used to estimate 'goodness' of route.
        distance_func: How to determine the length of a link.
        potholes: Places we can't visit."""

        self.origin = origin
        self.destination = destination
        self.potholes = potholes

        self.heuristic = heuristic
        self.distance_func = distance_func or (lambda x, y: x.distance_to(y))

    def start_search (self):
        self._frontier = [(Road(self.origin, self.origin), 0, self.heuristic(self.origin))]
        self._explored = []

    def run_to_end (self):
        """Convenience method to find the shortest path.
        
        Also serves as a programming-by-wishful-thinking setup, so I know
        which functions I still need to write."""

        while self.frontier_size() > 0:
            # Should we make these variables class-level? Probably.
            current_road, distance, estimate = self.get_next_road()
            if current_road == None:
                raise Exception # This really shouldn't happen.
            current_node = current_road.destination
            if current_node == self.destination:
                return self.generate_path_from(current_node)

            for neighbor_road in self.get_neighbors(current_node):
                neighbor = neighbor_road.destination
                n_distance = self.distance_func(current_node, neighbor)

                self.update_frontier(neighbor_road, distance)

        raise Exception # No route from start to end.

    def get_next_road (self):
        current_item = min(self._frontier, key=lambda x:x[1] + x[2])

        self._frontier.remove(current_item)
        self._explored.append(current_item)

        return current_item

    def generate_path_from (self, node):
        path = []
        parent = node
        while parent is not None:
            path.append(parent)
            try:
                nextparent = [x[0].origin for x in self._explored if x[0].destination == parent][0]
            except IndexError as ex:
                nextparent = None

            if nextparent == parent:
                parent = None
            else:
                parent = nextparent
        path.reverse()
        
        return path

    def get_neighbors (self, node):
        """Get all neighbors that haven't yet been explored."""

        # Yes, it's a one-line method. It's just a really ugly line.
        return [n for n in node.neighbors if n.destination not in [x[0] for x in self._explored] if n.destination not in self.potholes]

    def frontier_size (self):
        return len(self._frontier)

    def update_frontier (self, road, current_distance):
        n_distance = self.distance_func(road.origin, road.destination)
        if road.destination not in [x[0].destination for x in self._frontier]:
            self._frontier.append((road,
                    current_distance + n_distance,
                    self.heuristic(road.destination)))
        else:
            old_route = [x for x in self._frontier if x[0].destination == road.destination][0]

            if current_distance + n_distance < old_route[1]:
                self._frontier.remove(old_route)
                self._frontier.append((road,
                        current_distance + n_distance,
                        self.heuristic(road.destination)))

    def get_frontier_city_names (self):
        return [c[0].destination.name for c in self._frontier]

if __name__ == "__main__":
	print("Insert unit test here.")

# vim: set et sw=4 ts=4: 

#!/usr/bin/python
#
# 
#
# /file AStarSearch.py
#
# Copyright (c) 2012 
#
# Benjamin Geiger <begeiger@mail.usf.edu>
# Carlos Ezequiel <cfezequiel@mail.usf.edu>

""" A* Search Algorithm library """

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

        # Are we done with the search?
        self.done = False




    def start_search (self):
        """Begin the search process."""
        self._frontier = [(Road(None, self.origin), 0, self.heuristic(self.origin))]
        self._explored = []

    
    
   

    def run_to_end (self):
        """Convenience method to find the shortest path.
        
        Also serves as a programming-by-wishful-thinking setup, so I know
        which functions I still need to write."""

        while self.frontier_size() > 0:
            self.next_step()

        raise Exception # No route from start to end.


    
    
    
    def next_step (self):
        """ Search the next adjacent cities for the best path."""
        
        # If we're 
        if self.done: return (None, None, None, None)

        # Get information for the next road to be considered.
        current_road, distance, estimate = self.get_next_road()

        # Where does the current road lead?
        current_node = current_road.destination

        # If we're there, we're done.
        if current_node == self.destination:
            # Set us as being done.
            self.done = True
            # Send back the info.
            return current_road, distance, self.distance_func(current_road.origin, current_road.destination), 0

        # Otherwise, process the roads leading out.
        for neighbor_road in self.get_neighbors(current_node):
            self.update_frontier(neighbor_road, distance)
       
        # Special-case handling of the first road (origin = None).
        if current_road.origin is not None:
            distance_traveled = self.distance_func(current_road.origin, current_road.destination)
        else:
            distance_traveled = None

        # And send all the crap back.
        return (current_road, distance, distance_traveled, self.heuristic(current_road.destination))

    
    
    
    def get_next_road (self):
        """Retrieve the road on the frontier for which
        the estimated distance is lowest."""

        if len(self._frontier) <= 0:
            raise RuntimeError("All roads have been explored.")
        
        # Get the appropriate road.
        current_item = min(self._frontier, key=lambda x:x[1] + x[2])

        # Move it to the explored list.
        self._frontier.remove(current_item)
        self._explored.append(current_item)

        return current_item

    
    
    
    def generate_path_from (self, node):
        path = []
    
        # Loop until we find the start.
        while True:

            # Grab the road that leads to the current node.
            road = [x[0] for x in self._explored if x[0].destination == node][0]

            # If we're at the beginning of the path, send the whole thing back.
            # Otherwise, repeat the process.
            if road.origin is None or road.origin == road.destination:
                path.reverse()
                return path
            else:
                path.append(road)
                node = road.origin

    
    
    
    def get_neighbors (self, node):
        """Get all neighbors that haven't yet been explored."""

        # Yes, it's a one-line method. It's just a really ugly line.
        return [n for n in node.neighbors 
                if n.destination not in 
                    [x[0].destination for x in self._explored] 
                if n.destination not in self.potholes]

    
    
    
    def frontier_size (self):
        """Return the number of roads in the frontier."""
        return len(self._frontier)

    
    
    
    def update_frontier (self, road, current_distance):
        """Add road to the frontier, if it is the shortest path."""

        n_distance = self.distance_func(road.origin, road.destination)

        if road.destination not in [x[0].destination for x in self._frontier]:
            # If no road already leads to that city, add this road.
            # (Roads leading to already-explored cities are handled elsewhere.)
            self._frontier.append((road,
                    current_distance + n_distance,
                    self.heuristic(road.destination)))
        else:
            # Otherwise, find the previous route.
            old_route = [x for x in self._frontier if x[0].destination == road.destination][0]

            # If it's longer than the current route, replace it.
            if current_distance + n_distance < old_route[1]:
                self._frontier.remove(old_route)
                self._frontier.append((road,
                        current_distance + n_distance,
                        self.heuristic(road.destination)))

    
                
                
    def get_frontier_city_names (self):
        return [c[0].destination.name for c in self._frontier]

# vim: set et sw=4 ts=4: 

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

    def get_next_node (self):
        current_item = min(self.frontier, key=lambda x:x[1] + x[2])

        self.frontier.remove(current_item)
        self.explored.append(current_item)

        return (current_item[0], current_item[1], current_item[2])

    def generate_path_from (self, node):
        path = []
        parent = node
        while parent is not None:
            path.append(parent)
            try:
                parent = [x[3] for x in self.explored if x[0] == parent][0]
            except ex as IndexError:
                parent = None
        path.reverse()
        
        return path

    def get_neighbors (self, node):
        """Get all neighbors that haven't yet been explored."""

        # Yes, it's a one-line method. It's just a really ugly line.
        return [n for n in node.neighbors if n not in [x[0] for x in self.explored] if heuristic(n) is not None]

    def update_frontier (self, current_node, new_node, current_distance):
        n_distance = self.distance_func(current_node, new_node)
        if neighbor not in [x[0] for x in self.frontier]:
            self.frontier.append((neighbor,
                    current_distance + n_distance,
                    heuristic(new_node),
                    current_node))
        else:
            old_route = [x for x in self.frontier if x[0] == neighbor][0]

            if current_distance + n_distance < old_route[1]:
                self.frontier.remove(old_route)
                self.frontier.append((neighbor,
                        current_distance + n_distance,
                        heuristic(new_node),
                        current_node))

if __name__ == "__main__":
	print("Insert unit test here.")

# vim: set et sw=4 ts=4: 

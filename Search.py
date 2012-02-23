#!/usr/bin/python
#
# 
#
# Description.
#
# Copyright (c) 2012 Benjamin Geiger <begeiger@mail.usf.edu>


def astar(startnode, endnode, heuristic):
    """
    Perform an A* search on a graph.

    startnode and endnode are node-like objects, which have .name and
    .neighbors attributes. .neighbors is a sequence of 2-tuples
    (node, distance).

    heuristic is a function that accepts an object of the type of startnode
    and endnode and returns a value with a total ordering.

    Code adapted from pseudocode found on:
    http://en.wikipedia.org/wiki/A*_search_algorithm
    (Retrieved 16 February 2012)

    """


    # Create the open set, containing only the start node (and its associated data).
    openset = [(startnode, 0, heuristic(startnode), heuristic(startnode), None)]
    closedset = []

    while len(openset) > 0:
        # Grab the element of the open set that has the lowest total estimated
        # cost, and split it into its parts.
        currentitem = min(openset, key=lambda x: x[3])
        currentnode, distance, estimate, totaldistance, parent = currentitem

        # If we're done, rebuild the path and exit.
        if currentnode.name == endnode.name:
            parents = [currentnode]
            while parent is not None:
                parents.append(parent)
                potentialparents = [x[4] for x in closedset if x[0] == parent]
                parent = potentialparents[0]

            parents.reverse()
            return parents

        # Otherwise, we close this particular node.
        openset = [x for x in openset if x[0].name != currentnode.name]
        closedset.append(currentitem)

        # Get all neighbors of this node which are not already represented in
        # the closed set.
        neighbors = [n for n in currentnode.neighbors if n not in [x[0] for x in closedset]]

        for n in neighbors:
            neighbor, neighbordistance = n

            # If the neighbor isn't in the open set, add it.
            if neighbor.name not in [x[0].name for x in openset]:
                openset.append((neighbor,
                                distance + neighbordistance,
                                heuristic(neighbor),
                                distance + neighbordistance + heuristic(neighbor),
                                currentnode))
            else:
                neighboritem = [x for x in openset if x[0] == neighbor][0]

                # If this route to the neighbor is closer than the existing estimate,
                # update the route costs to reflect this.
                if neighbordistance + distance < neighboritem[1]:
                    openset.remove(neighboritem)
                    openset.append((neighbor,
                                    neighbordistance + distance,
                                    heuristic(neighbor),
                                    neighbordistance + distance + heuristic(neighbor),
                                    currentnode))
                else:
                    # Otherwise, do nothing.
                    pass

    # If we get here, there's no way from the start to the end.
    raise Exception



# Test script.
if __name__ == "__main__":
    import City

    A = City.City("A", 0, 100, [])
    B = City.City("B", 0, 200, [(A, 100)])
    C = City.City("C", 0, 300, [(A, 200)])
    D = City.City("D", 0, 400, [(B, 200), (C, 100)])

    print("Path: ", astar(D, A, lambda x: 1))

# vim: set et sw=4 ts=4: 

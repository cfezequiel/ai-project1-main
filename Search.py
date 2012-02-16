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
    .neighbors attributes.

    heuristic is a function that accepts an object of the type of startnode
    and endnode and returns a value with a total ordering.

    """


    openset = [(startnode, 0, heuristic(startnode), None)]
    closedset = []

    while len(openset) > 0:
        print("Closed set:", closedset)
        print("Open set:", openset)

        currentitem = min(openset, key=lambda x: x[2])
        currentnode, distance, estimate, parent = currentitem

        if currentnode.name == endnode.name:
            parents = [currentnode]
            while parent is not None:
                parents.append(parent)
                print("Backtracking through:", parent.name)
                potentialparents = [x[3] for x in closedset if x[0] == parent]
                print("Potential parents:", potentialparents)
                parent = potentialparents[0]

            parents.reverse()
            return parents

        openset.remove(currentitem)
        closedset.append(currentitem)

        neighbors = [n for n in currentnode.neighbors if n not in [x[0] for x in closedset]]

        for n in neighbors:
            neighbor, neighbordistance = n

            if neighbor not in [x[0] for x in openset]:
                openset.append((neighbor, distance + neighbordistance, heuristic(neighbor), currentnode))
            else:
                neighboritem = [x for x in openset if x[0] == neighbor][0]
                print(neighboritem)
                if neighbordistance + distance < neighboritem[1] + neighboritem[2]:
                    openset.remove(neighboritem)
                    openset.append((neighbor, neighbordistance + distance, heuristic(neighbor), currentnode))
                else:
                    pass

    # If we get here, there's no way from the start to the end.
    raise Exception



if __name__ == "__main__":
    import City

    A = City.City("A", 0, 100, [])
    B = City.City("B", 0, 200, [(A, 100)])
    C = City.City("C", 0, 300, [(A, 200)])
    D = City.City("D", 0, 400, [(B, 200), (C, 100)])

    print("Path: ", astar(D, A, lambda x: 1))

# vim: set et sw=4 ts=4: 

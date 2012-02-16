#!/usr/bin/python
#
# 
#
# Description.
#
# Copyright (c) 2012 Benjamin Geiger <begeiger@mail.usf.edu>

import City

def parse_locations_file(locationsfile):

    locations = []

    for line in locationsfile.readlines():
        tokens = line.split("#")[0].split()

        if len(tokens) == 0:
            continue
        
        if len(tokens) == 1 and tokens[0].lower() == "end":
            return locations
        
        if len(tokens) < 3:
            print("Invalid input line:", line)
            continue

        if tokens[0] in [l.name for l in locations]:
            print("Duplicate city definition:", line)
            continue

        try:
            newlocation = City.City(tokens[0], int(tokens[1]), int(tokens[2]))
        except ex as ValueError:
            print("Invalid input line (invalid integer):", line)
            continue

        locations.append(newlocation)

    return locations

        
def parse_connections_file(connectionsfile, locations):

    for line in connectionsfile.readlines():
        # Cut off anything after a hash, then split the rest on whitespace.
        tokens = line.split("#")[0].split()

        if len(tokens) == 0:
            continue

        if len(tokens) == 1 and tokens[0].lower() == "end":
            return locations

        try:
            currentlocation = [x for x in locations if x.name == tokens[0]][0]
        except ex as IndexError:
            print("Invalid connection (could not find source city):", line)
            continue

        for neighborname in tokens[2:]:
            try:
                neighbor = [x for x in locations if x.name == neighborname][0]
            except ex as IndexError:
                print("Invalid connection (could not find destination " + neighborname + ")", line)
                continue

            currentlocation.neighbors.append(neighbor)

    return locations


if __name__ == "__main__":
    locations = parse_locations_file(open("locations.txt"))
    connectedlocations = parse_connections_file(open("connections.txt"), locations)
    for l in connectedlocations:
        print(l.name, end=" ")
        print(len(l.neighbors), end=": ")
        for n in l.neighbors:
            print(n.name, end=" ")
        print()

# vim: set et sw=4 ts=4: 

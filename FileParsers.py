#!/usr/bin/python
#
# 
#
# Description.
#
# Copyright (c) 2012 Benjamin Geiger <begeiger@mail.usf.edu>

import City
import Road
from math import sqrt

# Input: an open file containing city data.
# Output: a list of City objects, one for each valid city record.

def parse_locations_file(locationsfile):
    """Read in a file containing city data and return City objects for each."""

    locations = []

    # Loop over each line.
    for line in locationsfile.readlines():
        # Cut off anything after a hash, and split the rest on whitespace.
        tokens = line.split("#")[0].split()

        # If the line is blank, go to the next.
        if len(tokens) == 0:
            continue
        
        # If we've reached the end of the file, return.
        if len(tokens) == 1 and tokens[0].lower() == "end":
            return locations
        
        # If we've got a malformed input line, say so.
        if len(tokens) < 3:
            print("Invalid input line:", line)
            continue

        # If we've got the same city twice, say so.
        if tokens[0] in [l.name for l in locations]:
            print("Duplicate city definition:", line)
            continue

        try:
            # Create a new city.
            newlocation = City.City(tokens[0], int(tokens[1]), int(tokens[2]))
        except ValueError:
            # If the ints don't parse, try the next line.
            print("Invalid input line (invalid integer):", line)
            continue

        # Add the new city to our list.
        locations.append(newlocation)

    return locations

        
def parse_connections_file(connectionsfile, locations):
    """Read in a connections file and update the cities to include those connections."""

    for line in connectionsfile.readlines():
        # Cut off anything after a hash, and split the rest on whitespace.
        tokens = line.split("#")[0].split()

        # Skip empty lines.
        if len(tokens) == 0:
            continue

        # At the end of the file, return.
        if len(tokens) == 1 and tokens[0].lower() == "end":
            return locations

        # Find the source city.
        try:
            currentlocation = [x for x in locations if x.name == tokens[0]][0]
        except IndexError:
            # Complain if it's not there.
            print("Invalid connection (could not find source city):", line)
            continue

        # For each listed neighbor:
        for neighborname in tokens[2:]:
            # Find the neighbor.
            try:
                neighbor = [x for x in locations if x.name == neighborname][0]
            except IndexError:
                # Complain.
                print("Invalid connection (could not find destination " + neighborname + ")", line)
                continue

            # Add the connection between the cities.
            currentlocation.neighbors.append(Road.Road(currentlocation, neighbor))

    return locations


# Test script.
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

#!/usr/bin/python
#
# 
#
# /file main.py
#
# Copyright (c) 2012 
#
# Benjamin Geiger <begeiger@mail.usf.edu>
# Carlos Ezequiel <cfezequiel@mail.usf.edu>

"""Console version of the A* Algorithm program."""

import sys

from City import City
from AStarSearch import AStarSearch

from FileParsers import parse_locations_file, parse_connections_file

if sys.version_info[0] != 3:
    print("This program requires Python 3.")
    exit(1)

if len(sys.argv) < 5:
    print("Usage: python {} <locations> <connections> <origin> <destination> [<avoid>]".format(sys.argv[0]))
    exit(1)

try:
    locationsfile = open(sys.argv[1])
except IOError:
    print("Could not open file", sys.argv[1])
    exit(1)

try:
    connectionsfile = open(sys.argv[2])
except IOError:
    print("Could not open file", sys.argv[2])
    exit(1)

locations = parse_connections_file(connectionsfile, parse_locations_file(locationsfile))

try:
    startcity = [x for x in locations if x.name == sys.argv[3]][0]
except IndexError:
    print("Could not find origin city:", sys.argv[3])
    exit(1)

try:
    destcity = [x for x in locations if x.name == sys.argv[4]][0]
except IndexError:
    print("Could not find destination city:", sys.argv[4])
    exit(1)

avoidcities = [x for x in locations if x.name in sys.argv[5:]]


# Create the search object
search = AStarSearch(startcity, destcity, lambda x: x.distance_to(destcity), potholes=avoidcities)

# Run the search algorithm
search.start_search()

# Get the shortest path traversed
path = search.run_to_end()

# Output path to standard output
print("->".join([x.name for x in path]))

# vim: set et sw=4 ts=4: 

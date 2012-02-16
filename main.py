#!/usr/bin/python
#
# 
#
# Description.
#
# Copyright (c) 2012 Benjamin Geiger <begeiger@mail.usf.edu>

import sys

from City import City
import Search

from FileParsers import parse_locations_file, parse_connections_file

def make_heuristic(dest, avoid):
    return lambda x: x == avoid and 1000000 or x.distance_to(dest)

if sys.version_info[0] != 3:
    print("This program requires Python 3.")
    exit(1)

if len(sys.argv) < 3:
    print("Usage: python {} <locations file> <connections file>".format(sys.argv[0]))
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

# test

startcity = [x for x in locations if x.name == "A1"][0]
destcity = [x for x in locations if x.name == "G5"][0]
avoidcity = [x for x in locations if x.name == "B2"][0]

print(Search.astar(startcity, destcity, make_heuristic(destcity, avoidcity)))



# vim: set et sw=4 ts=4: 

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

if len(sys.argv) >= 6:
    try:
        avoidcity = [x for x in locations if x.name == sys.argv[5]][0]
    except IndexError:
        print("Could not find city to avoid:", sys.argv[5])
        exit(1)
else:
    avoidcity = None




print(Search.astar(startcity, destcity, make_heuristic(destcity, avoidcity)))



# vim: set et sw=4 ts=4: 

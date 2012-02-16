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

        


if __name__ == "__main__":
    print(parse_locations_file(open("locations.txt")))

# vim: set et sw=4 ts=4: 

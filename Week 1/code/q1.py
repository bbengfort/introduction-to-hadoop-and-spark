#!/usr/bin/env python

from collections import defaultdict

def mapper(key, line):
    parts = line.split("/")
    if len(parts) > 2:
        return parts[1], 1
    return None, 1

def reducer(key, values):
    return key, sum(values)

if __name__ == '__main__':

    # Create an intermediary data store for Map Results
    data = defaultdict(list)

    # Open the file and read each line from it
    with open('apache.log', 'r') as logfile:
        for idx, line in enumerate(logfile):

            # Pass each line to the Mapper
            key, val = mapper(idx, line)
            data[key].append(val)

    # Pass mapped key, values to reducer
    for key, values in data.items():
        print reducer(key, values)

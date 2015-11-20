#!/usr/bin/env python
# reducer
# A reducer that computes the average number of flights per airport per day.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Nov 06 12:48:17 2015 -0500

"""
A reducer that computes the average number of flights per airport per day.
This reducer will read sorted key/value pairs from stdin that have been
outputted by the mapper. This reducer expects to be fed data using Unix pipes
and output ((hour, origin), sum) key/value pairs to stdout.

To use this reducer on the command line:

    $ cat ontime_flights.tsv | python mapper.py | sort | python reducer.py

You should see (airport, flights) pairs printed to the terminal.
"""

##########################################################################
## Imports
##########################################################################

import sys

from itertools import groupby
from operator import itemgetter

##########################################################################
## Reducing Functionality
##########################################################################

SEP  = "\t" # Delimiter to separate key/value pairs
DAYS = 31   # The number of days in January to average by day

def parse_input(sep=SEP):
    """
    Read and parse input, spliting on the sep character, creating a generator
    that can be passed into group by for efficient aggregation.
    """
    for line in sys.stdin:
        yield line.rstrip().split(sep, 1)

def reducer(sep=SEP):
    """
    Uses groupby and parse_input to compute the average number of flights
    per day, in this case there are 31 days in January.
    """

    for key, values in groupby(parse_input(sep), itemgetter(0)):
        try:
            total = sum(int(count) for _, count in values)
            average = float(total) / float(DAYS)
            sys.stdout.write(
                "{}{}{:0.2f}\n".format(key, sep, average)
            )
        except ValueError:
            sys.stderr.write("Could not sum for key: {}\n".format(key))
            continue


##########################################################################
## Main Method
##########################################################################

if __name__ == '__main__':
    reducer()

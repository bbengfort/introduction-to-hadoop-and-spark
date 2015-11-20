#!/usr/bin/env python
# reducer
# A reducer that computes the number of hits per hour, per origin.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Nov 06 12:30:57 2015 -0500

"""
A reducer that computes the number of hits per hour, per origin.
This reducer will read sorted key/value pairs from stdin that have been
outputted by the mapper. This reducer expects to be fed data using Unix pipes
and output ((hour, origin), sum) key/value pairs to stdout.

To use this reducer on the command line:

    $ cat apache.log | python mapper.py | sort | python reducer.py

You should see ((hour, origin), sum) pairs printed to the terminal.
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

SEP = "\t" # Delimiter to separate key/value pairs

def parse_input(sep=SEP):
    """
    Read and parse input, spliting on the sep character, creating a generator
    that can be passed into group by for efficient aggregation.
    """
    for line in sys.stdin:
        yield line.rstrip().split(sep, 1)

def reducer(sep=SEP):
    """
    Sum the number of hits per hour, origin on the web server. Use the
    `groupby` function in `itertools` to group by key.
    """

    for key, values in groupby(parse_input(sep), itemgetter(0)):
        try:
            total = sum(int(count) for _, count in values)
            sys.stdout.write(
                "{}{}{}\n".format(key, sep, total)
            )
        except ValueError:
            sys.stderr.write("Could not sum for key: {}\n".format(key))
            continue


##########################################################################
## Main Method
##########################################################################

if __name__ == '__main__':
    reducer()

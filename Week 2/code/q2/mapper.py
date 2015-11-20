#!/usr/bin/env python
# mapper.py
# A mapper that emits the airport and counter from the ontime flights dataset.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Nov 06 12:43:59 2015 -0500

"""
A mapper that emits the airport and counter from the ontime flights dataset.
This mapper will read CSV data that is input via stdin then output its
key/value pairs to stdout so that it can be used with Unix pipes.

To use this mapper on the command line:

    $ cat ontime_flights.tsv | python mapper.py

You should see (airport, 1) pairs printed to the terminal.
"""

##########################################################################
## Imports
##########################################################################

import sys
import csv

##########################################################################
## Mapping Functionality
##########################################################################

SEP = "\t" # Delimiter to separate key/value pairs


def mapper(sep=SEP):
    """
    Read input from stdin, parse the TSV file and emit (airport, 1) for each
    origin and destination airport (e.g. this is counting the number of
    arriving and departing flights at all airports).
    """
    reader = csv.reader(sys.stdin, delimiter='\t')
    for row in reader:
        origin      = row[6]
        destination = row[9]

        # First emit the origin airport
        sys.stdout.write(
            "{}{}{}\n".format(origin, sep, 1)
        )

        # Then emit the destination airport
        sys.stdout.write(
            "{}{}{}\n".format(destination, sep, 1)
        )

##########################################################################
## Main Method
##########################################################################

if __name__ == '__main__':
    mapper()

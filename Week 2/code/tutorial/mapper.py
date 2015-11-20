#!/usr/bin/env python
# mapper.py
# A mapper that emits the airport and delay from the  Ontime flights dataset.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Nov 06 09:12:41 2015 -0500

"""
A mapper that emits the airport and delay from the ontime flights dataset.
This mapper will read CSV data that is input via stdin then output its
key/value pairs to stdout so that it can be used with Unix pipes.

To use this mapper on the command line:

    $ cat ontime_flights.tsv | python mapper.py

You should see (airport, delay) pairs printed to the terminal.
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
    Read input from stdin, parse the TSV file and emit (airport, delay).
    """
    reader = csv.reader(sys.stdin, delimiter='\t')
    for row in reader:
        airport = row[6]
        delay   = row[15]
        sys.stdout.write(
            "{}{}{}\n".format(airport, sep, delay)
        )

##########################################################################
## Main Method
##########################################################################

if __name__ == '__main__':
    mapper()

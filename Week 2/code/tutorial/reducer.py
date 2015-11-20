#!/usr/bin/env python
# reducer
# A reducer that computes the average flight delay per airport.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Nov 06 09:20:50 2015 -0500

"""
A reducer that computes the average flight delay per airport.
This reducer will read sorted key/value pairs from stdin that have been
outputted by the mapper. This reducer expects to be fed data using Unix pipes
and output (airport, mean) key/value pairs to stdout.

To use this reducer on the command line:

    $ cat ontime_flights.tsv | python mapper.py | sort | python reducer.py

You should see (airport, mean) pairs printed to the terminal.
"""

##########################################################################
## Imports
##########################################################################

import sys

##########################################################################
## Reducing Functionality
##########################################################################

SEP = "\t" # Delimiter to separate key/value pairs


def reducer(sep=SEP):
    """
    Read input from the mapper from stdin. Parse and convert the key/value
    pairs then compute the average delay per airport. Emit (airport, mean).

    This reducer shows a basic groupby algorithm, but you would use the
    groupby function in the itertools library in real life. We'll take a look
    about how to do this in our Python Hadoop miniframework.

    Note that key/value pairs are sorted, so we should be seeing a stream
    of contiguous airports and values per line that we can compute on. This
    means that we have to keep track of which airport we're on.
    """

    # Track which airport we are currently on
    current_airport = None
    current_total   = 0
    current_count   = 0

    for line in sys.stdin:
        # Split the line only once according to the sep character
        airport, delay = line.split(sep, 1)

        # Parse the delay into a float value
        # If there is no delay, continue processing
        if not delay.strip(): continue
        delay = float(delay)

        if current_airport == airport:
            # This means we're still computing the mean for an airport.
            current_total += delay
            current_count += 1

        else:
            # This means that we have seen a new airport, so we have to
            # finish processing the previoius airport and start again.
            if current_airport is not None:
                mean = current_total / current_count
                sys.stdout.write(
                    "{}{}{:0.3f}\n".format(current_airport, sep, mean)
                )

            current_total   = delay
            current_count   = 1
            current_airport = airport

    # Don't forget to emit the last airport!
    mean = current_total / current_count
    sys.stdout.write(
        "{}{}{:0.3f}\n".format(airport, sep, mean)
    )


##########################################################################
## Main Method
##########################################################################

if __name__ == '__main__':
    reducer()

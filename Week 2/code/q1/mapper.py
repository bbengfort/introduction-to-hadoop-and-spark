#!/usr/bin/env python
# mapper.py
# A mapper that emits the origin and hour from a web log with a counter value.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Nov 06 12:29:25 2015 -0500

"""
A mapper that emits the origin and hour from a web log with a counter value.

To use this mapper on the command line:

    $ cat apache.log | python mapper.py

You should see ((hour, origin), 1) pairs printed to the terminal.
"""

##########################################################################
## Imports
##########################################################################

import sys

##########################################################################
## Mapping Functionality
##########################################################################

SEP = "\t"


def mapper(sep=SEP):
    """
    Read input from stdin, parse the log file and emit ((hour, origin), 1).
    """

    for line in sys.stdin:
        try:
            origin = line.split()[0]
            hour   = int(line.split(':')[1])
            key    = (hour, origin)

            sys.stdout.write(
                "{}{}{}\n".format(key, sep, 1)
            )
        except (IndexError, ValueError):
            sys.stderr.write("Couldn't parse line \"{}\"\n".format(line))
            continue

##########################################################################
## Main Method
##########################################################################

if __name__ == '__main__':
    mapper()

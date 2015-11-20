# Emulating MapReduce using a Unix Pipeline

In Chapter Two, we have started to learn how to program in MapReduce &mdash; the distributed programming abstraction that is used to easily parallelize computations across a cluster. However, although we have started to look at the Hadoop architecture and cluster operations, we still do not have the ability to write jobs to submit to the cluster since the MapReduce application API is written in Java. Luckily, there is a way to get us started writing mappers and reducers using Python and Unix Pipes that emulates the processing of Hadoop on a single cluster. In this tutorial we will describe how to write mappers and reducers in Python and execute them on the command line so that we can start writing MapReduce code in advance of us using Hadoop Streaming and Python on the cluster in the following week.

To do this, we'll put together a simple analysis on a toy dataset - the on time performance of U.S. airlines. In the resources section, download the dataset called `ontime_flights.zip` and unzip this file both in your local working directory.

## Dataset

The On Time Performance dataset is one month of U.S. airport flight data from January 2013 collected by the [Research and Innovative Technology Administration (RITA) Bureau of Transportation Studies](http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time). These data sets can also be downloaded directly from the RITA website, but the data in the resources section has been cleaned up a bit. For a single month, you’ll find 509,519 flights with data that comprises 62 MB on disk. This dataset is a very good one to explore, as a single month of data is easy to develop and debug, but if you accumulated the entire dataset parallel processing would be extremely valuable.

Each row in the data is a tab-delimited series of values. To inspect them, use the `head` command on the command line:

    $ head ontime_flights.tsv
    2013	1	17	1/17/13	9E	Endeavor Air Inc.	DFW	Dallas/Fort Worth, TX    TX	JFK	New York, NY	NY	1038	-7	1451	-14	0	193	175	1391
    2013	1	18	1/18/13	9E	Endeavor Air Inc.	DFW	Dallas/Fort Worth, TX	TX	JFK	New York, NY	NY	1037	-8	1459	-6	0	202	178	1391
    2013	1	19	1/19/13	9E	Endeavor Air Inc.	DFW	Dallas/Fort Worth, TX	TX	JFK	New York, NY	NY	1035	-5	1515	17	0	220	201	1391
    2013	1	20	1/20/13	9E	Endeavor Air Inc.	DFW	Dallas/Fort Worth, TX	TX	JFK	New York, NY	NY	1037	-8	1455	-10	0	198	176	1391
    2013	1	21	1/21/13	9E	Endeavor Air Inc.	DFW	Dallas/Fort Worth, TX	TX	JFK	New York, NY	NY	1044	-1	1446	-19	0	182	162	1391
    2013	1	22	1/22/13	9E	Endeavor Air Inc.	DFW	Dallas/Fort Worth, TX	TX	JFK	New York, NY	NY	1054	9	1502	-3	0	188	171	1391
    2013	1	23	1/23/13	9E	Endeavor Air Inc.	DFW	Dallas/Fort Worth, TX	TX	JFK	New York, NY	NY	1036	-9	1504	-1	0	208	186	1391
    2013	1	24	1/24/13	9E	Endeavor Air Inc.	DFW	Dallas/Fort Worth, TX	TX	JFK	New York, NY	NY	1036	-9	1520	15	0	224	204	1391
    2013	1	25	1/25/13	9E	Endeavor Air Inc.	DFW	Dallas/Fort Worth, TX	TX	JFK	New York, NY	NY	1042	-3	1525	20	0	223	174	1391
    2013	1	26	1/26/13	9E	Endeavor Air Inc.	DFW	Dallas/Fort Worth, TX	TX	JFK	New York, NY	NY	1034	-6	1509	11	0	215	189	1391

Although there is no header row, some important records are the date of the flight (year, month, day, full date), the airline identifier and carrier, the origination airport code, city, and state as well as the destination airport code, city, and state. The numeric values at the end of the row describe the airport, in particular the first four values are the departure time and delay, and the arrival time and delay. Negative delays mean early arrivals or departures. For more details on the records in the dataset, see the `README.md` that is included with the data.

In this example we will compute the mean arrival delays per airport using a Unix pipeline and _two_ Python files: a mapper and a reducer.

## Unix Pipelines

In Unix (and Linux) a [pipeline](https://en.wikipedia.org/wiki/Pipeline_(Unix)) enables a set of processes to communicate together by passing data through the standard streams. Of the standard streams, you're probably most familiar with `stdout` - the stream that is written two when you `print` in Python. The [standard streams](https://en.wikipedia.org/wiki/Standard_streams) are communication channels that are automatically connected to programs by the operating system at runtime.

- Standard input (`stdin`) is a communication channel that allows programs to _read_ data into the program. If there is no redirection, this input is usually typed directly from the keyboard which started the program.

- Standard output (`stdout`) is a communication channel with which programs _write_ output data. If there is no redirection, this output is usually printed on the text terminal that started the program.

- Standard error (`stderr`) is a third channel that programs can _write_ data to, usually error messages or diagnostics. Because it is independent of `stdout` it allows programs to return multiple values, distinguishing output and errors. However, `stderr` is usually redirected to the same destination as `stdout`, and if there is no redirection, it is printed to the text terminal that started the program.

In the pipeline, these communication channels are used to chain process such that the output of each process (`stdout`) feeds directly as input (`stdin`) to the next. The standard shell syntax for pipelines is to invoke programs in one command as follows:

    $ progA | progB | progC

Pipelines are unidirectional, with data flowing through the pipeline from left to right. Therefore `progA` accepts either no input from stdin (generating data on its own) or accepts input from the computer. It's output is piped to `progB` via `progB`'s `stdin` whose output is piped to `progC` in a similar fashion. In the end `progC` will write it's output to `stdout` which in this case will simply be written to the terminal.

Typically, `progA` will be some file reading program, for example `cat`, `less`, or `head` that opens a file and spits the content to stdout. Subsequent programs will filter or process the file's data. The final command (`progC`) will either print out to the terminal or will provide some other data viewing functionality, for example `less` or `more` which provide scrolling pages.

A classic example is a multiline search of a large file:

    $ cat large-file.txt | grep key | less

This sends the output of the large file in a streaming fashion to `grep`, which filters lines that don't contain "key" and then outputs that data to `less` which can be interacted with by the user.

## MapReduce Pipeline

The MapReduce application on YARN is just a series of many processes that are coordinated by an ApplicationMaster. Data is streamed into many mappers, which perform some computation on individual instances of the data. The output of the mappers is pulled into a shuffle and sort phases which orders the data by key and then streams that data to many reducers such that each reducer is guaranteed to have all values associated with a particular key. The reducers then stream their aggregated output by key back to disk.

With this in mind, it is easy to emulate the MapReduce application on Linux using a four process pipeline with the Linux commands `cat` and `sort` along with two Python scripts - a `mapper.py` and a `reducer.py` as follows:

    $ cat input.txt | python mapper.py | sort | python reducer.py > output.txt

The two Python files, `mapper.py` and `reducer.py` must accept input from `stdin` as text data, parse and compute using it, then output data as text to `stdout`. To do this, you would simply use the `sys` module, which provides access to the standard streams as file-like objects, `sys.stdin` and `sys.stdout`.

Because the standard streams are text based, it is important to output data in a parseable text format. Typically key/value pairs are separated by a delimiter (usually a tab `"\t"`), and numeric values must be stringified. More complex data types can be serialized as JSON or CSV, so long as they are written with a key to a single line of output.

A basic template of a mapper process written in Python is as follows:

    #!/usr/bin/env python

    import sys

    SEP = "\t"

    def mapper(sep=SEP):
        for line in sys.stdin:
            # Process the incoming Data
            key = ...
            val = ...

            # Write the key/value to stdout, separated by the sep char.
            sys.stdout.write(key + sep + val + "\n")

    if __name__ == "__main__":
        mapper()

Similarly the basic template of a reducer process is as follows:

    #!/usr/bin/env python

    import sys

    SEP = "\t"

    def reducer(sep=SEP):

        # Track the current key to group on
        current_key = None

        for line in sys.stdin:
            # Process the incoming Data
            key, val = line.split(sep, 1)

            if key == current_key:
                # Process current reduction
            else:
                # This is a new key, so output values to stdout
                sys.stdout.write(outkey + sep + outval + "\n")

                # Reset the current key
                current_key = key

        # Don't forget to output the last key!
        sys.stdout.write(outkey + sep + outval + "\n")

    if __name__ == "__main__":
        reducer()

These templates are very lightweight, and real mappers and reducers will utilize the Python standard library for memory safe computation via iterators. Especially notable are the `csv` and `json` modules for serialization and deserialization of data, as well as the `itertools` and `operator` libraries for computing using generators. In the next section we'll look at a specific example.

## Computing Average Arrival Delay

In order to compute the mean arrival delay per airport using a Unix pipeline, we have to create two Python scripts, a `mapper.py` and a `reducer.py`. The mapper's job is to parse the TSV file and to perform a key space change while targeting only a specific value. That is it changes the "key" from the line number (which is just implied in this context) to the airport code, and converts the value (previously the text of each line in the input data) to simply be the arrival delay. It is implemented as follows:

    import sys
    import csv

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

    if __name__ == '__main__':
        mapper()

Here, we utilize the `csv` module to parse the TSV input. The `csv.reader` is actually a memory safe generator, that reads data from input one line at a time. As a result it's a very useful module to employ in a streaming context. For each row in the dataset, we simply output the airport code, separated by the tab character, and the delay, each on a new line.

To test the execution of the mapper, `cat` the input data to the `mapper.py` and then pipe to `head` so you don't get all 500k+ lines of output!

    $ cat ontime_flights.tsv | python mapper.py | head
    DFW	-14
    DFW	-6
    DFW	17
    DFW	-10
    DFW	-19
    DFW	-3
    DFW	-1
    DFW	15
    DFW	20
    DFW	11

If you get an `IOError: [Errno 32] Broken pipe` - don't worry, this is just Python's response when the `head` command cuts off the input stream after receiving only the data it needs. You can eliminate this error by wrapping the call in `try/except` if you'd like.

The reducer's job is to take all of the per-airport delay input and aggregate them into a single value &mdash; the mean. However this is a bit more complicated since data is coming into the reducer one key/value pair at a time. Therefore the reducer has to track which key it is currently computing on, grouping as necessary. Below is a very simple implementation of the reducer:

    import sys

    SEP = "\t" # Delimiter to separate key/value pairs


    def reducer(sep=SEP):

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
                # finish processing the previous airport and start again.
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

    if __name__ == '__main__':
        reducer()

In real life you'd probably use `itertools.groupby` in the Python standard library to perform the group by key in a memory safe manner. However, this code demonstrates what's required to aggregate (reduce) the mean delay per airport. Note that the reducer depends on the keys coming in as contiguous blocks, therefore in order to pass data to the reducer, it must be sorted first. In order to run the reducer, execute the following pipeline:

    $ cat ontime_flights.tsv | python mapper.py | sort | python reducer.py
    ABI	6.382
    ABQ	1.649
    ABR	0.256
    ABY	-1.864
    ACT	-1.036
    ACV	1.453
    ADK	8.637
    ADQ	3.143
    AEX	15.922
    AGS	5.321
    ALB	-2.959
    ALO	3.299
    AMA	-0.036
    ANC	5.344
    APN	-1.218
    ART	-10.796
    [snip ...]

As you can see this takes a little time to process sequentially. By using multiple nodes to perform both the mapping and reducing, hopefully we will achieve improved performance, particularly across extremely large data sets.

## Conclusion

In this tutorial we have explored the use of Unix Pipelines to emulate MapReduce on a cluster. Unix Pipelines allow us to create processes that communicate by "piping" the output of one process to the input of the next using standard streams. Therefore by piping our input data to a mapper, the mapper output to a sort, and the sort output to a reducer then reducing to a file, we can achieve a sequential effect as parallel processing on a cluster.

The good news is that this is exactly how Hadoop Streaming works as well! So by writing these applications, we've already started implementing MapReduce functionality that can be written on the cluster. In fact, on Amazon EMR, you can upload a mapper.py and a reducer.py file as we've specified above and have it parallelized across the cluster.

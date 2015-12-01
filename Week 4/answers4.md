# Assignment Four Model Answers
**Big Data with Hadoop Week Four Lesson**

The following document describes model answers for questions one and two in the homework assignment. Please compare your results and work with the work described here. Note that your answer may not be exactly the same as the answer below, but should be well represented by what is described.

Keep in mind that you only had to turn in one or the other of these assignments.

## Question One

In this question you were required to submit the following:

1. All Python file(s) with the various mapper code
2. All Python file(s) with the various reducer code
3. A test file containing the output of your analysis for the specific words identified in the problem assignment.

In order to compute TF-IDF, you need to create a chained MapReduce job with three independent tasks: the computation of the term frequency, the computation of the document-term frequency, and finally the computation of TF-IDF.

The first Mapper breaks the input into (word, document) pairs along with a
counter variable to sum the frequency of all terms.

    import re
    import sys

    from framework import Mapper

    header = re.compile(r'^=+\s(\d+)\s=+$', re.I)

    class TermFrequencyMapper(Mapper):

        def __init__(self, *args, **kwargs):
            super(TermFrequencyMapper, self).__init__(*args, **kwargs)

            self.stopwords = set()
            self.tokenizer = re.compile(r'\W+')
            self.current   = None

            # Read the stopwords from the text file.
            with open('stopwords.txt') as stopwords:
                for line in stopwords:
                    self.stopwords.add(line.strip())

        def tokenize(self, text):
            """
            Tokenizes and normalizes a line of text (yields only non-stopwords
            that aren't digits, punctuation, or empty strings).
            """
            for word in re.split(self.tokenizer, text):
                if word and word not in self.stopwords and word.isalpha():
                    yield word

        def map(self):
            for line in self:

                if header.match(line):
                    # We have a new document! Get the document id:
                    self.current = header.match(line).groups()[0]

                else:
                    # Only emit words that have a document id.
                    if self.current is None: continue

                    # Otherwise tokenize the line and emit every (word, docid).
                    for word in self.tokenize(line):
                        self.emit((word, self.current), 1)

    if __name__ == '__main__':
        mapper = TermFrequencyMapper(sys.stdin)
        mapper.map()

The first reducer is a simple sum reducer:

    import sys
    from framework import Reducer

    class SumReducer(Reducer):

        def reduce(self):
            for key, values in self:
                total = sum(int(count[1]) for count in values)
                self.emit(key, total)

    if __name__ == '__main__':
        reducer = SumReducer(sys.stdin)
        reducer.reduce()

The next mapper performs a key space change to compute the document frequency.

    import sys

    from ast import literal_eval as make_tuple
    from framework import Mapper

    class DocumentTermsMapper(Mapper):

        def map(self):
            for line in self:
                key, tf = line.split(self.sep)  # Split line into key, val parts
                word, docid = make_tuple(key)   # Parse the tuple string
                self.emit(word, (docid, tf, 1))

    if __name__ == '__main__':
        mapper = DocumentTermsMapper(sys.stdin)
        mapper.map()

And the second reducer is a more complex sum reducer along with a value and key space change in preparation for a map-only job that computes TF-IDF.

    import sys

    from framework import Reducer
    from operator import itemgetter
    from ast import literal_eval as make_tuple

    class DocumentTermsReducer(Reducer):

        def reduce(self):
            for key, values in self:
                terms = sum(int(item[2]) for item in values)
                for docid, tf, num in values:
                    self.emit((key, docid), (int(tf), terms))

        def __iter__(self):
            for current, group in super(DocumentTermsReducer, self).__iter__():
                yield current, map(make_tuple, [item[1] for item in group])

    if __name__ == '__main__':
        reducer = DocumentTermsReducer(sys.stdin)
        reducer.reduce()

Finally the Mapper for the TF-IDF is as follows:

    import sys
    import math

    from framework import Mapper
    from ast import literal_eval as make_tuple

    class TFIDFMapper(Mapper):

        def __init__(self, *args, **kwargs):
            self.N = kwargs.pop("documents")
            super(TFIDFMapper, self).__init__(*args, **kwargs)

        def map(self):
            for line in self:
                key, val = map(make_tuple, line.split(self.sep))
                tf, n = (int(x) for x in val)
            if n > 0:
                idf = math.log(self.N/n)
                self.emit(key, idf*tf)

    if __name__ == '__main__':
        mapper = TFIDFMapper(sys.stdin, documents=41)
        mapper.map()

The Reducer is just an IdentityReducer because this is a map-only job.

    import sys

    from operator import itemgetter
    from framework import Reducer

    class IdentityReducer(Reducer):

        def reduce(self):
            for current, group in self:
                for item in group:
                    self.emit(current, item[1])

    if __name__ == '__main__':
        reducer = IdentityReducer(sys.stdin)
        reducer.reduce()

To execute this code on Hadoop you would use the following commands:

    $ hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
        -input reuters \
        -output reuters_term_frequency \
        -mapper mapper1.py \
        -reducer reducer1.py \
        -file mapper1.py \
        -file reducer1.py \
        -file stopwords.txt \
        -file framework.py

    $ hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
        -input reuters_term_frequency \
        -output reuters_document_term_frequency \
        -mapper mapper2.py \
        -reducer reducer2.py \
        -file mapper2.py \
        -file reducer2.py \
        -file framework.py

    $ hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
        -input reuters_document_term_frequency \
        -output reuters_tfidf \
        -mapper mapper3.py \
        -reducer reducer3.py \
        -file mapper3.py \
        -file reducer3.py \
        -file framework.py

Note that you would probably use a scheduler like Oozie to put this together in real life.

The output should be similar to:

    ('beacon', 8015)    9.28618968425962
    ('beacons', 21002)  18.57237936851924
    ('draconian', 10642)    8.593042503699674
    ('draconian', 10779)    8.593042503699674
    ('espionage', 17925)    9.28618968425962
    ('matrix', 10)  8.18757739559151
    ('matrix', 2121)    8.18757739559151
    ('matrix', 6419)    16.37515479118302
    ('pizza', 11416)    7.206748142579785
    ('pizza', 1153) 72.06748142579785
    ('pizza', 12853)    7.206748142579785
    ('pizza', 17576)    14.41349628515957
    ('pizza', 4841) 43.24048885547871
    ('pizza', 5409) 21.620244427739355
    ('pizza', 6338) 7.206748142579785
    ('pizza', 9434) 21.620244427739355
    ('shasta', 15920)   9.28618968425962
    ('zuccherifici', 10139) 8.18757739559151
    ('zuccherifici', 11292) 8.18757739559151
    ('zuccherifici', 11344) 8.18757739559151

#### Spark Submission (alternative)

For an answer implemented with Spark, you were required to submit the following:

1. A Python file with the spark application, submittable using `spark-submit`
2. A test file containing the output of your analysis for the specific words identified in the problem assignment.

The Python Spark application is as follows:

    import re
    import math

    from operator import add
    from functools import partial
    from pyspark import SparkConf, SparkContext

    APP_NAME  = "TF-IDF of Reuters Corpus"
    N_DOCS    = 41

    # Regular expressions
    header    = re.compile(r'^=+\s(\d+)\s=+$', re.I)
    tokenizer = re.compile(r'\W+')

    def chunk(args):
        """
        Splits a text file into smaller document id, text pairs.
        """

        def chunker(text):
            """
            Inner generator function.
            """
            docid    = None
            document = []
            for line in text.split("\n"):
                # Check to see if we are on a header line.
                hdr = header.match(line)
                if hdr is not None:
                    # If we are on a current document, emit it.
                    if docid is not None:
                        yield (docid, document)

                    # If so, extract the document id and reset the document.
                    docid = hdr.groups()[0]
                    document = []
                    continue
                else:
                    document.append(line)

        fname, text = args
        return list(chunker(text))


    def tokenize(document, stopwords=None):
        """
        Tokenize and return (docid, word) pairs with a counter.
        """

        def inner_tokenizer(lines):
            """
            Inner generator for word tokenization.
            """
            for line in lines:
                for word in re.split(tokenizer, line):
                    if word and word not in stopwords.value and word.isalpha():
                        yield word

        docid, lines = document
        return [
            ((docid, word), 1) for word in inner_tokenizer(lines)
        ]


    def term_frequency(v1, v2):
        """
        Compute the term frequency by splitting the complex value.
        """
        docid, tf, count1   = v1
        _docid, _tf, count2 = v2
        return (docid, tf, count1 + count2)


    def tfidf(args):
        """
        Compute the TF-IDF given a ((word, docid), (tf, n)) argument.
        """
        (key, (tf, n)) = args
        if n > 0:
            idf = math.log(N_DOCS/n)
            return (key, idf*tf)

    def main(sc):
        """
        Primary analysis mechanism for Spark application
        """

        # Load stopwords from the dataset
        with open('stopwords.txt', 'r') as words:
            stopwords = frozenset([
                word.strip() for word in words.read().split("\n")
            ])

        # Broadcast the stopwords across the cluster
        stopwords = sc.broadcast(stopwords)

        # Load the corpus as whole test files and chunk them.
        corpus  = sc.wholeTextFiles('reuters.txt').flatMap(chunk)

        # Phase one: tokenize and sum (word, docid), count pairs (document frequency).
        docfreq = corpus.flatMap(partial(tokenize, stopwords=stopwords))
        docfreq = docfreq.reduceByKey(add)

        # Phase two: compute term frequency then perform keyspace change.
        trmfreq = docfreq.map(lambda (key, tf): (key[1], (key[0], tf, 1)))
        trmfreq = trmfreq.reduceByKey(term_frequency)
        trmfreq = trmfreq.map(lambda (word, (docid, tf, n)): ((word, docid), (tf, n)))

        # Phase three: comptue the tf-idf of each word, document pair.
        tfidfs  = trmfreq.map(tfidf)

        # Write the results out to disk
        tfidfs.saveAsTextFile("reuters-tfidfs")

    if __name__ == '__main__':
        # Configure Spark
        conf = SparkConf().setAppName(APP_NAME)
        sc   = SparkContext(conf=conf)

        # Execute Main functionality
        main(sc)

To execute this code on Hadoop you would use the following command:

    $ spark-submit --master yarn-client spark-app.py

The output should be similar to above.

## Question Two

In this question you were required to submit the following:

1. A Python file with the mapper code.
2. A Python file with the reducer code.
3. A text file containing the results for the airports mentioned above.

The stripes mapper is as follows:

    import csv
    import sys

    from framework import Mapper

    class DelayStatsMapper(Mapper):

        def __init__(self, delimiter="\t", quotechar='"', **kwargs):
            super(DelayStatsMapper, self).__init__(**kwargs)
            self.delimiter = delimiter
            self.quotechar = quotechar

        def map(self):
            for row in self:
                try:
                    airport = row[6]
                    delay   = float(row[15])
                except ValueError:
                    # Could not parse the delay, which is zero.
                    delay   = 0.0

                self.emit(airport, (1, delay, delay ** 2))

        def read(self):
            """
            Parse the tab delimited flights dataset with the CSV module.
            """
            reader = csv.reader(self.infile, delimiter=self.delimiter)
            for row in reader:
                yield row

    if __name__ == '__main__':
        mapper = DelayStatsMapper(infile=sys.stdin)
        mapper.map()

And the statistical aggregation reducer is as follows:

    import sys
    import math

    from framework import Reducer
    from ast import literal_eval as make_tuple

    class StatsReducer(Reducer):

        def reduce(self):
            for key, values in self:

                count   = 0
                delay   = 0.0
                square  = 0.0
                minimum = None
                maximum = None

                for value in values:
                    count  += value[0]
                    delay  += value[1]
                    square += value[2]

                    if minimum is None or value[1] < minimum:
                        minimum = value[1]

                    if maximum is None or value[1] > maximum:
                        maximum = value[1]

                mean   = delay / float(count)
                stddev = math.sqrt((square-(delay**2)/count)/count-1)

                self.emit(key, (count, mean, stddev, minimum, maximum))

        def __iter__(self):
            for current, group in super(StatsReducer, self).__iter__():
                yield current, map(make_tuple, [item[1] for item in group])

    if __name__ == '__main__':
        reducer = StatsReducer(infile=sys.stdin)
        reducer.reduce()

To execute this code on Hadoop you would use the following command:

    $ hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
        -input ontime_flights.tsv \
        -output airport_delay_stats \
        -mapper mapper.py \
        -reducer reducer.py \
        -file mapper.py \
        -file reducer.py \
        -file framework.py

The output should be similar to:

    JFK 9031    1.37    39.80   -70.00  1272.00
    SFO 13015   0.01    27.77   -55.00  389.00
    IAD 5883    8.57    40.34   -56.00  483.00
    BWI 7758    2.80    30.04   -49.00  849.00
    ORD 23178   11.81   42.09   -64.00  842.00
    SEA 7185    0.67    28.87   -55.00  859.00
    LAX 17385   0.57    26.95   -58.00  521.00
    MSP   11000   1.02    34.38   -65.00  704.00
    HOU 4713    3.30    29.10   -39.00  1062.00

#### Spark Submission (alternative)

For an answer implemented with Spark, you were required to submit the following:

1. A Python file with the spark application, submittable using `spark-submit`.
2. A text file containing the results for the airports mentioned above.

The Python Spark application is as follows:

    import sys
    import csv
    import math

    from functools import partial
    from StringIO import StringIO
    from pyspark import SparkConf, SparkContext

    APP_NAME = "Summary Statistics of Arrival Delay by Airport"

    def counters(line):
        """
        Splits the line on a CSV and parses it into the key and summary counters.
        A counter is as follows: (count, total, square, minimum, maximum).
        """
        reader = csv.reader(StringIO(line), delimiter='\t')
        row = reader.next()

        airport = row[6]

        try:
            delay = float(row[15])
        except ValueError:
            delay = 0.0

        return (airport, (1, delay, delay ** 2, delay, delay))

    def aggregation(item1, item2):
        """
        For an (airport, counters) item, perform summary aggregations.
        """
        count1, total1, squares1, min1, max1 = item1
        count2, total2, squares2, min2, max2 = item2

        minimum = min((min1, min2))
        maximum = max((max1, max2))
        count   = count1 + count2
        total   = total1 + total2
        squares = squares1 + squares2

        return (count, total, squares, minimum, maximum)

    def summary(aggregate):
        """
        Compute summary statistics from aggregation.
        """
        (airport, (count, total, square, minimum, maximum)) = aggregate

        mean   = total / float(count)
        stddev = math.sqrt((square-(total**2)/count)/count-1)

        return (airport, (count, mean, stddev, minimum, maximum))

    def main(sc):
        """
        Primary analysis mechanism for Spark application
        """

        # Load data set and parse out statistical counters
        delays = sc.textFile('ontime_flights/ontime_flights.tsv').map(counters)

        # Perform summary aggregation by key
        delays = delays.reduceByKey(aggregation)
        delays = delays.map(summary)

        # Write the results out to disk
        delays.saveAsTextFile("delays-summary")

    if __name__ == '__main__':
        # Configure Spark
        conf = SparkConf().setAppName(APP_NAME)
        sc   = SparkContext(conf=conf)

        # Execute Main functionality
        main(sc)


To execute this code on Hadoop you would use the following command:

    $ spark-submit --master yarn-client spark-app.py

The output should be similar to above.

# Assignment Four Model Answers
**Big Data with Hadoop Week Four Lesson**

The following document describes model answers for questions one, two, and three in the homework assignment. Please compare your results and work with the work described here. Note that your answer may not be exactly the same as the answer below, but should be well represented by what is described.

## Question One

In this question you were required to submit the following:

1. A Python file with the mapper code
2. A Python file with the reducer code
3. A test file containing the output of your analysis (this will be the part-00000 file on HDFS when you execute it on the cluster).

The Python mapper is as follows:

    N = 10788.0 # Number of documents, in float to make division work.
    stopwords = 'stopwords.txt'

    class TermMapper(object):

        def __init__(self):
            with open(stopwords, 'r') as excludes:
                self.stopwords = set(line.strip() for line in excludes)

            self.curdoc = None

        def __call__(self, key, value):
            if value.startswith('='*34):
                self.curdoc = int(value.strip("=").strip())
            else:
                for word in value.split():
                    word = self.normalize(word)
                    if word and not word in self.stopwords:
                        yield (word, self.curdoc), 1

        def normalize(self, word):
            word = word.lower()
            for char in string.punctuation:
                word = word.replace(char, '')
            return word

    class UnitMapper(object):

        def __call__(self, key, value):
            term, docid = key
            yield term, (docid, value, 1)

    class IDFMapper(object):

        def __call__(self, key, value):
            term, docid = key
            tf, n = value
            idf = math.log(N/n)
            yield (term, docid), idf*tf

    class SumReducer(object):

        def __call__(self, key, values):
            yield key, sum(values)

    class BufferReducer(object):

        def __call__(self, key, values):
            term   = key
            values = list(values)
            n = sum(g[2] for g in values)
            for g in values:
                yield (term, g[0]), (g[1], n)

    class IdentityReducer(object):

        def __call__(self, key, values):
            for value in values:
                yield key, value

    def runner(job):
        job.additer(TermMapper, SumReducer, combiner=SumReducer)
        job.additer(UnitMapper, BufferReducer)
        job.additer(IDFMapper, IdentityReducer)

    def starter(prog):
        excludes = prog.delopt("stopwords")
        if excludes: prog.addopt("param", "stopwords="+excludes)

    if __name__ == "__main__":
        import dumbo
        dumbo.main(runner, starter)

For this question, the reducer is just a simple mean reducer (one that you will probably use routinely in your Hadoop analytics):



To execute this code on Hadoop you would use the following command:

    $ hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
        -input reuters \
        -output reuters-tfidf \
        -mapper mapper.py \
        -reducer reducer.py \
        -file mapper.py \
        -file reducer.py \
        -file stopwords.txt

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
2. A test file containing the output of your analysis (this will be the part-00000 file on HDFS when you execute it on the cluster).

The Python Spark application is as follows:



To execute this code on Hadoop you would use the following command:

    $ spark-submit --master yarn-client spark-app.py

The output should be similar to above.

## Question Two

In this question you were required to submit the following:

1. A Python file with the mapper code
2. A Python file with the reducer code
3. A test file containing the output of your analysis

The Python mapper is as follows:

    #!/usr/bin/env python

    import math
    import dumbo

    class DelayMapper(object):

        SEP = '\t'

        def __call__(self, key, value):
            value = value.split(self.SEP)
            try:
                airport = value[6]
                delay   = float(value[15])
                if airport and delay:
                    yield (airport, delay)
            except:
                pass

    class StatsCombiner(object):

        def __call__(self, key, values):

            count   = 0
            delay   = 0.0
            square  = 0.0
            minimum = None
            maximum = None

            for value in values:
                count  += 1
                delay  += value
                square += value ** 2

                if minimum is None or value < minimum:
                    minimum = value

                if maximum is None or value > maximum:
                    maximum = value

            yield (key, (count, delay, square, minimum, maximum))

    class StatsReducer(object):

        def __call__(self, key, values):

            count   = 0
            delay   = 0.0
            square  = 0.0
            minimum = None
            maximum = None

            for value in values:
                count  += value[0]
                delay  += value[1]
                square += value[2]

                if minimum is None or value[3] < minimum:
                    minimum = value[3]

                if maximum is None or value[4] > maximum:
                    maximum = value[4]

            mean   = delay / float(count)
            stddev = math.sqrt((square-(delay**2)/count)/count-1)

            yield (key, (count, mean, stddev, minimum, maximum))

    if __name__ == '__main__':
        dumbo.run(DelayMapper, StatsReducer, combiner=StatsCombiner)

The Python reducer is simply a sum reducer:



To execute this code on Hadoop you would use the following command:

    $ hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
        -input ontime \
        -output ontime-stats \
        -mapper mapper.py \
        -reducer reducer.py \
        -file mapper.py \
        -file reducer.py \
        -file params.txt

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

1. A Python file with the spark application, submittable using `spark-submit`
2. A test file containing the output of your analysis (this will be the part-00000 file on HDFS when you execute it on the cluster).

The Python Spark application is as follows:




To execute this code on Hadoop you would use the following command:

    $ spark-submit --master yarn-client spark-app.py

The output should be similar to above.

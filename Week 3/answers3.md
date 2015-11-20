# Assignment Three Model Answers
**Big Data with Hadoop Week Three Lesson**

The following document describes model answers for questions one, two, and three in the homework assignment. Please compare your results and work with the work described here. Note that your answer may not be exactly the same as the answer below, but should be well represented by what is described.

## Question One

In this question you were required to submit the following:

1. A Python file with the mapper code
2. A Python file with the reducer code
3. A test file containing the output of your analysis (this will be the part-00000 file on HDFS when you execute it on the cluster).

The Python mapper is as follows:

    import sys
    import csv

    from framework import Mapper

    class MSEMapper(Mapper):

        def __init__(self, *args, **kwargs):
            """
            On initialization, load the coefficients and intercept of the linear
            model for use in downstream processing of the MSE.
            """
            super(MSEMapper, self).__init__(*args, **kwargs)

            # Store required computation
            self.coef = []
            self.intercept = None

            # Load the parameters from the text file
            with open('params.txt', 'r') as params:
                # Read the file and split on new lines
                data = params.read().split("\n")

                # Parse the data into floats
                data = [float(row.strip()) for row in data if row.strip()]

                # Everything but the last value are the thetas (coefficients)
                self.coef = data[:-1]

                # The last value is the intercept
                self.intercept = data[-1]

        def read(self):
            """
            Adapt the read function to be a CSV parser, since this is CSV data.
            """
            reader = csv.reader(super(MSEMapper, self).read())
            for row in reader:
                # Parse the row into floats
                yield [float(x) for x in row]

        def compute_error(self, row):
            vals = row[:-1] # The dependent variables from the row
            y    = row[-1]  # The independent variable is the last item in the row

            # Compute the predicted value based on the linear model
            yhat = sum([b*x for (b,x) in zip(self.coef, vals)]) + self.intercept

            # Compute the square error of the prediction
            return (y - yhat) ** 2

        def map(self):
            """
            The mapper will compute the MSE for each row in the data set and emit
            it with a "dummy key" that is, we'll compute the total for the entire
            data set, so we don't need to group by a key for multiple reducers.
            """
            for row in self:
                self.emit(1, self.compute_error(row))


    if __name__ == '__main__':
        mapper = MSEMapper(sys.stdin)
        mapper.map()

For this question, the reducer is just a simple mean reducer (one that you will probably use routinely in your Hadoop analytics):

    from framework import Reducer

    class MeanReducer(Reducer):

        def reduce(self):
            for key, values in self:
                count = 0
                total = 0.0

                for value in values:
                    count += 1
                    total += float(value[1])

                self.emit(key, (total / count))


    if __name__ == '__main__':
        import sys

        reducer = MeanReducer(sys.stdin)
        reducer.reduce()

To execute this code on Hadoop you would use the following command:

    $ hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
        -input blogData \
        -output blogMSE \
        -mapper mapper.py \
        -reducer reducer.py \
        -file mapper.py \
        -file reducer.py \
        -file params.txt

The output should be similar to:

1	646.70518996

#### Spark Submission (alternative)

For an answer implemented with Spark, you were required to submit the following:

1. A Python file with the spark application, submittable using `spark-submit`
2. A test file containing the output of your analysis (this will be the part-00000 file on HDFS when you execute it on the cluster).

The Python Spark application is as follows:

    import sys
    import csv

    from functools import partial
    from StringIO import StringIO
    from pyspark import SparkConf, SparkContext

    APP_NAME = "MSE of Blog Comments Regression"

    def parse(line):
        """
        Splits the line on a CSV and parses it into floats. Returns a tuple of:
        (X, y) where X is the vector of independent variables and y is the target
        (dependent) variable; in this case the last item in the row.
        """
        reader = csv.reader(StringIO(line))
        row = [float(x) for x in reader.next()]
        return (tuple(row[:-1]), row[-1])


    def cost(row, coef, intercept):
        """
        Computes the square error given the row.
        """
        X, y = row # extract the dependent and independent vals from the tuple.

        # Compute the predicted value based on the linear model
        yhat = sum([b*x for (b,x) in zip(coef.value, X)]) + intercept.value

        # Compute the square error of the prediction
        return (y - yhat) ** 2


    def main(sc):
        """
        Primary analysis mechanism for Spark application
        """

        # Load coefficients and intercept from local file
        coef = []
        intercept = None

        # Load the parameters from the text file
        with open('params.txt', 'r') as params:
            # Read the file and split on new lines and parse into floats
            data = [
                float(row.strip())
                for row in params.read().split("\n")
                if row.strip()
            ]

            coef = data[:-1]        # Everything but the last value are the thetas (coefficients)
            intercept = data[-1]    # The last value is the intercept

        # Broadcast the parameters across the Spark cluster
        # Note that this data is small enough you could have used a closure
        coef      = sc.broadcast(coef)
        intercept = sc.broadcast(intercept)

        # Create an accumulator to sum the squared error
        sum_square_error = sc.accumulator(0)

        # Load and parse the blog data from HDFS and insert into an RDD
        blogs = sc.textFile("hdfs://user/student/blogData").map(parse)

        # Map the cost function and accumulate the sum.
        error = blogs.map(partial(cost, coef=coef, intercept=intercept))
        error.foreach(lambda cost: sum_square_error.add(cost))

        # Print and compute the mean.
        print sum_square_error.value / error.count()


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

1. A Python file with the mapper code
2. A Python file with the reducer code
3. A test file containing the output of your analysis

The Python mapper is as follows:

    import re
    import sys
    import string

    from framework import Mapper


    class TrigramMapper(Mapper):

        def __init__(self, infile=sys.stdin, separator='\t'):
            super(TrigramMapper, self).__init__(infile, separator)

            # Load the stopwords from the associated stopwords file
            with open('stopwords.txt', 'r') as words:
                self.stopwords = frozenset([
                    word.strip() for word in words.read().split("\n")
                ])

        def exclude(self, token):
            """
            Do not allow punctuation or stopwords in trigrams.
            """
            return token in self.stopwords or token in string.punctuation

        def normalize(self, token):
            """
            Any type of normalization is allowed, here we simply lowercase and remove the part of speech that has already been tagged.
            """
            return token.lower().split("/")[0]

        def tokenize(self, value):
            """
            Entry point for tokenization, normalization, and exclusion.
            """
            for token in value.split():
                token = self.normalize(token)
                if not self.exclude(token):
                    yield token

        def trigrams(self, words):
            """
            Emits all trigrams from a list of words.
            """
            words = list(words)  # force generator to iterate
            return zip(*[words[idx:] for idx in xrange(3)])

        def map(self):
            for value in self:
                for trigram in self.trigrams(self.tokenize(value)):
                    self.counter("ngrams") # Count the total number of trigrams
                    self.emit(trigram, 1)   # Emit the trigram and a frequency to sum


    if __name__ == '__main__':
        mapper = TrigramMapper()
        mapper.map()

The Python reducer is simply a sum reducer:

    from framework import Reducer


    class SumReducer(Reducer):

        def reduce(self):
            for key, values in self:
                total = sum(int(count[1]) for count in values)
                self.emit(key, total)

    if __name__ == '__main__':
        import sys

        reducer = SumReducer(sys.stdin)
        reducer.reduce()

To execute this code on Hadoop you would use the following command:

    $ hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
        -input textcorpus \
        -output trigrams \
        -mapper mapper.py \
        -reducer reducer.py \
        -file mapper.py \
        -file reducer.py \
        -file params.txt

The output should be similar to:

    ('.mp4', 'still', 'image')	1
    ('1', 'billion', 'today')	1
    ('1', 'billion', 'two')	1
    ('1', 'second', 'shutter')	1
    ('1,000', 'requests', 'sent')	1
    ('10', 'purchase', 'whole')	1
    ('10', 'sticks', 'four')	1
    ('10.9', 'billion', '2100')	1
    ('10.9', 'billion', 'also')	1
    ('100', 'fps', '19-megapixel')	1
    ('100', 'fps', 'red')	1
    ('100', 'mbps', 'give')	1
    ('100', 'mbps', 'video')	1
    ('100', 'percent', 'mobile')	1
    ('100', 'time', 'launching')	1
    ('11th', 'bravely', 'vow')	1
    ('12', 'previously', 'unreleased')	1
    ('13,000', 'employees', 'lighter')	1
    ('13.2', 'billion', '2100')	1
    ('14.99', 'instead', '20')	1
    ('149.99', 'us', '\xc2\xa3149.99')	1
    ('15', 'fps', 'red')	1
    ('15', 'months', 'ago')	1
    ('15.95', 'split', 'everything')	1
    ('16', 'bits', 'color')	1
    ('16,700', 'body', '100')	1
    ('16.5-stop', 'dynamic', 'range')	1
    ('160', 'degrees', 'fahrenheit')	1
    ('16:9', '4:3', '3:2')	1
    ('17', 'lay', 'claim')	1
    ('17,000', 'red', 'scarlet')	1
    ('18', 'months', 'development')	1
    ('18,', '2014.', 'posts')	1
    ('18,000', 'jobs', 'next')	1
    ('19', 'megapixels', 'half')	1
    ('19-megapixel', 'raw', 'stills')	1
    ('1977', 'position', 'made')	1
    ('1987', 'teamed', 'youtube')	1
    ('199.99', '149.99', 'us')	1
    ('1:1', 'hello', 'instagram')	1
    ('2', 'confessions', 'trickbaby')	1
    ('2', 'featuring', 'cat')	1
    ('2', 'hours', 'setting')	1
    ('2,100', 'employees', 'let')	1
    ('20', 'percent', 'non-manufacturing')	1
    ('2013', 'although', 'improving')	1
    ('2013', 'first', 'half')	1
    ('2013', 'keynote', 'ios-only')	1
    ('2013', 'lost', '1')	1
    ('2014', 'dropped', 'canary')	1
    ('2014', 'important', 'feature')	1
    ('2014', 'monster', 'hunter')	1
    ('2014', 'though', 'red')	1
    ('2050', 'start', 'decline')	1
    ('2100', 'whereas', 'earlier')	1
    ('215', 'usa', 'patriot')	1
    ('25,000', 'new', 'employees')	1
    ('250', 'number', 'change')	1
    ('250', 'zero', '250')	1
    ('299', 't-mobile', 'wants')	1
    ('29th', 'said', 'band')	1
    ('29th', 'today', 'network')	1
    ('3', 'buy', '10')	1
    ('3', 'last', 'week')	1
    ('3.5', 'foot', '8.5')	1
    ('30', 'days', 'left')	1
    ('30', 'fps', '100')	1
    ('30', 'percent', 'price')	1
    ('300', 'tv', 'unit')	1
    ('3000', 'distributors', 'bring')	1
    ('30m', 'compared', '50m')	1
    ('31.24', 'next', '24')	1
    ('36', 'blog', 'posts')	1
    ('3:2', 'even', '1:1')	1
    ('3am', 'last', 'week')	1
    ('3d', 'content', 'rest')	1
    ('3d-printed', 'marvel', 'superhero')	1
    ('3ds', 'family', 'two')	1
    ('3ds', 'hardware', 'new')	1
    ('3ds', 'll', 'japanese')	1
    ('3ds', 'screens', 'bright')	1
    ('3ds', 'well', 'larger')	1
    ('3ds', 'xl', 'arrive')	1
    ('3ds', 'xl', 'home')	1
    ('3ds', 'xl', 'honest')	1
    ('4', 'billion', 'end')	1
    ('4', 'bog-standard', 'two')	1
    ('4', 'hit', 'us')	1
    ('4', 'little', 'improvements')	1
    ('4.4', 'billion', 'expected')	1
    ('400-plus', 'kb', 'much')	1
    ('4:3', '3:2', 'even')	1
    ('4g', 'gaming', 'test')	1
    ('4g', 'right', 'stick')	1
    ('4k', '30', 'fps')	1
    ('4k', 'give', '8-megapixel')	1
    ('4k', 'photo', 'allows')	1
    ('4k', 'photo', 'feature')	1
    ('4k', 'raw', 'dpx')	1
    ('4k', 'video', 'becoming')	1
    ('4k', 'video', 'search')	1
    ('5', 'billion', '2050')	1
    ('50', '\xc2\xa350', 'anyway')	1
    ('50', 'billion', 'gets')	1
    ('500', 'hours', 'performances')	1
    ('50m', 'shine', 'less')	1
    ('6', '6', 'plus')	5
    ('6', 'iphone', '6')	1
    ('6', 'plus', 'already')	1
    ('6', 'plus', 'austin')	1
    ('6', 'plus', 'feature')	1
    ('6', 'plus', 'instead')	1
    ('6', 'plus', 'largest')	1
    ('6', 'plus', 'like')	1
    ('6', 'plus', 'making')	1
    ('6', 'plus', 'owners')	1
    ('6', 'plus', 'preorders')	1
    ('6', 'plus', 'purchase')	1
    ('6', 'plus', 'shipping')	1
    ('60', 'seconds', 'ensuring')	1
    ('69.99', 'purchase', 'retailers')	1
    ('6k', 'raw', 'video')	1
    ('7', 'billion', 'people')	1
    ('7', 'billion', 'took')	1
    ('70', 'oracle', 'first')	1
    ('70', 'percent', 'compressed')	1
    ('70,000', 'tickets', 'per')	1
    ('700hp', 'disposal', 'managed')	1
    ('8', 'came', 'yesterday')	1
    ('8', 'clamoring', 'attention')	1
    ('8', 'finally', 'live')	1
    ('8', 'first', 'bundles')	1
    ('8', 'letting', 'retweet')	1
    ('8', 'may', 'trickling')	1
    ('8', 'users', 'exactly')	1
    ('8-bit', 'game', 'plugged')	1
    ('8-megapixel', 'photo', 'still')	1
    ('8-megapixel', 'still', 'compared')	1
    ('8.5', 'foot', 'race')	1
    ('80', 'cleared', 'episodes')	1
    ('80', 'percent', 'people')	1
    ('9', 'billion', '13.2')	1
    ('900', 'employees', '20')	1
    ('900', 'jobs', 'part')	1
    ('900', 'new', 'lx100')	1
    ('95', 'percent', 'chance')	1
    ('99', 'slated', 'arrive')	1
    ('999', 'national', 'security')	1
    ('\xc2\xa350', 'anyway', 'launches')	1
    ('\xe2\x80\x94', 'aubrey', 'plaza')	1
    apollo:q2 benjamin$ head -n 100 trigrams.txt
    ('.mp4', 'still', 'image')	1
    ('1', 'billion', 'today')	1
    ('1', 'billion', 'two')	1
    ('1', 'second', 'shutter')	1
    ('1,000', 'requests', 'sent')	1
    ('10', 'purchase', 'whole')	1
    ('10', 'sticks', 'four')	1
    ('10.9', 'billion', '2100')	1
    ('10.9', 'billion', 'also')	1
    ('100', 'fps', '19-megapixel')	1
    ('100', 'fps', 'red')	1
    ('100', 'mbps', 'give')	1
    ('100', 'mbps', 'video')	1
    ('100', 'percent', 'mobile')	1
    ('100', 'time', 'launching')	1
    ('11th', 'bravely', 'vow')	1
    ('12', 'previously', 'unreleased')	1
    ('13,000', 'employees', 'lighter')	1
    ('13.2', 'billion', '2100')	1
    ('14.99', 'instead', '20')	1
    ('149.99', 'us', '\xc2\xa3149.99')	1
    ('15', 'fps', 'red')	1
    ('15', 'months', 'ago')	1
    ('15.95', 'split', 'everything')	1
    ('16', 'bits', 'color')	1
    ('16,700', 'body', '100')	1
    ('16.5-stop', 'dynamic', 'range')	1
    ('160', 'degrees', 'fahrenheit')	1
    ('16:9', '4:3', '3:2')	1
    ('17', 'lay', 'claim')	1
    ('17,000', 'red', 'scarlet')	1
    ('18', 'months', 'development')	1
    ('18,', '2014.', 'posts')	1
    ('18,000', 'jobs', 'next')	1
    ('19', 'megapixels', 'half')	1
    ('19-megapixel', 'raw', 'stills')	1
    ('1977', 'position', 'made')	1
    ('1987', 'teamed', 'youtube')	1
    ('199.99', '149.99', 'us')	1
    ('1:1', 'hello', 'instagram')	1
    ('2', 'confessions', 'trickbaby')	1
    ('2', 'featuring', 'cat')	1
    ('2', 'hours', 'setting')	1
    ('2,100', 'employees', 'let')	1
    ('20', 'percent', 'non-manufacturing')	1
    ('2013', 'although', 'improving')	1
    ('2013', 'first', 'half')	1
    ('2013', 'keynote', 'ios-only')	1
    ('2013', 'lost', '1')	1
    ('2014', 'dropped', 'canary')	1
    ('2014', 'important', 'feature')	1
    ('2014', 'monster', 'hunter')	1
    ('2014', 'though', 'red')	1
    ('2050', 'start', 'decline')	1
    ('2100', 'whereas', 'earlier')	1
    ('215', 'usa', 'patriot')	1
    ('25,000', 'new', 'employees')	1
    ('250', 'number', 'change')	1
    ('250', 'zero', '250')	1
    ('299', 't-mobile', 'wants')	1
    ('29th', 'said', 'band')	1
    ('29th', 'today', 'network')	1
    ('3', 'buy', '10')	1
    ('3', 'last', 'week')	1
    ('3.5', 'foot', '8.5')	1
    ('30', 'days', 'left')	1
    ('30', 'fps', '100')	1
    ('30', 'percent', 'price')	1
    ('300', 'tv', 'unit')	1
    ('3000', 'distributors', 'bring')	1
    ('30m', 'compared', '50m')	1
    ('31.24', 'next', '24')	1
    ('36', 'blog', 'posts')	1
    ('3:2', 'even', '1:1')	1
    ('3am', 'last', 'week')	1
    ('3d', 'content', 'rest')	1
    ('3d-printed', 'marvel', 'superhero')	1
    ('3ds', 'family', 'two')	1
    ('3ds', 'hardware', 'new')	1
    ('3ds', 'll', 'japanese')	1
    ('3ds', 'screens', 'bright')	1
    ('3ds', 'well', 'larger')	1
    ('3ds', 'xl', 'arrive')	1
    ('3ds', 'xl', 'home')	1
    ('3ds', 'xl', 'honest')	1
    ('4', 'billion', 'end')	1
    ('4', 'bog-standard', 'two')	1
    ('4', 'hit', 'us')	1
    ('4', 'little', 'improvements')	1
    ('4.4', 'billion', 'expected')	1
    ('400-plus', 'kb', 'much')	1
    ('4:3', '3:2', 'even')	1
    ('4g', 'gaming', 'test')	1
    ('4g', 'right', 'stick')	1
    ('4k', '30', 'fps')	1
    ('4k', 'give', '8-megapixel')	1
    ('4k', 'photo', 'allows')	1
    ('4k', 'photo', 'feature')	1
    ('4k', 'raw', 'dpx')	1
    ('4k', 'video', 'becoming')	1

#### Spark Submission (alternative)

For an answer implemented with Spark, you were required to submit the following:

1. A Python file with the spark application, submittable using `spark-submit`
2. A test file containing the output of your analysis (this will be the part-00000 file on HDFS when you execute it on the cluster).

The Python Spark application is as follows:

    from operator import add
    from functools import partial
    from string import punctuation
    from pyspark import SparkConf, SparkContext


    APP_NAME = "Trigram Frequency"


    def tokenize(line):
        """
        Normalizes the line (making it all lowercase) then tokenizes it, removing
        the part of speech tag.
        """
        words = line.lower().split()
        return [word.split("/")[0] for word in words]


    def include(word, stopwords):
        """
        Returns True if the word is not an exclusion word, either punctuation or a
        stopword. Use this helper function in a filter.
        """
        return word not in punctuation and word not in stopwords.value


    def ngrams(words, n):
        """
        Returns the NGrams by performing a sliding window over a list of words.
        """
        words = list(words) # Convert the generator to a list
        return zip(*[words[idx:] for idx in xrange(n)])


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

        # Create an accumulator to count total number of trigrams and words.
        words     = sc.accumulator(0)
        trigrams  = sc.accumulator(0)

        # Load and parse the corpus from HDFS and insert into an RDD
        tokens = sc.textFile("textcorpus").flatMap(tokenize)

        # Perform the word count
        tokens.foreach(lambda w: words.add(1))

        # Filter stopwords and extract trigrams
        tokens = tokens.filter(partial(include, stopwords=stopwords))
        tokens = tokens.mapPartitions(partial(ngrams, n=3))

        # Perform the trigram count
        tokens.foreach(lambda ng: trigrams.add(1))

        # Counter per-trigram frequency
        tokens = tokens.map(lambda t: (t, 1)).reduceByKey(add)

        # Write output to disk
        tokens.saveAsTextFile("trigrams")

        print "Number of trigrams: {} in {} words.".format(trigrams.value, words.value)
        for trigram, frequency in tokens.sortBy(lambda (t,c): c).take(100):
            print "{}: {}".format(frequency, trigram)

    if __name__ == '__main__':
        # Configure Spark
        conf = SparkConf().setAppName(APP_NAME)
        sc   = SparkContext(conf=conf)

        # Execute Main functionality
        main(sc)


To execute this code on Hadoop you would use the following command:

    $ spark-submit --master yarn-client spark-app.py

The output should be similar to above.

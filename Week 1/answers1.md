# Assignment One Model Answers
**Big Data with Hadoop Week One Lesson**

The following document describes model answers for questions one and two in the homework assignment. Please compare your results and work with the work described here. Note that your answer may not be exactly the same as the answer below, but should be well represented by what is described.

## Question One

In this question you were required to submit the following:

1. A Python program used to perform the computation on the log file.
2. A text file containing the output or results of your program.

The Python code that performs the analysis with a mapper and reducer is as follows:

    #!/usr/bin/env python

    from collections import defaultdict

    def mapper(key, line):
        parts = line.split("/")
        if len(parts) > 2:
            return parts[1], 1
        return None, 1

    def reducer(key, values):
        return key, sum(values)

    if __name__ == '__main__':

        # Create an intermediary data store for Map Results
        data = defaultdict(list)

        # Open the file and read each line from it
        with open('apache.log', 'r') as logfile:
            for idx, line in enumerate(logfile):

                # Pass each line to the Mapper
                key, val = mapper(idx, line)
                data[key].append(val)

        # Pass mapped key, values to reducer
        for key, values in data.items():
            print reducer(key, values)

The output should be similar to:

    ('Mar', 99761)
    ('Feb', 72114)
    ('Aug', 66077)
    ('Sep', 89095)
    ('Apr', 65011)
    ('Jun', 53720)
    ('Jul', 54941)
    ('Jan', 43666)
    ('May', 63778)
    ('Nov', 41251)
    ('Dec', 29803)
    ('Oct', 45907)
    (None, 1614)

## Question Two

In this question you were required to submit the following:

1. A Python program used to perform the computation on the log file.
2. A text file containing the output or results of your program.

The Python code that performs the analysis with a mapper and reducer is as follows:

    def mapper(key, line):

        # Split on tab to get the title@lineno and text parts
        parts = line.split("\t")
        if len(parts) > 1:
            # Split the text part on space to get the words.
            for word in parts[1].split(" "):
                if len(word) > 0:
                    # Yield the first letter and the length of the word.
                    yield word[0], len(word)

    def reducer(key, values):
        average = float(sum(values)) / len(values) if len(values) > 1 else 0.0
        return key, average

    # The main program
    if __name__ == "__main__":

        # Create an intermediary data store for Map results
        data = {}

        # Open the file and read each line from it.
        with open('data/shakespeare.txt', 'r') as corpus:
            for idx, line in enumerate(corpus):
                line = line.strip()

                # Pass each line to the Mapper, then for each result from
                # the mapper iterator, store the key and value in the
                # intermediary data store, a hash whose key is the first
                # letter of the alphabet, and whose value is a list of the
                # lengths of words in Shakespeare.
                for key, value in mapper(idx, line):
                    if key in data:
                        data[key].append(value)
                    else:
                        data[key] = [value,]

        # The final step is to pass the data in the intermediary store to
        # the reducer function and print out the results.
        for key, values in data.items():
            print reducer(key, values)

The output should be similar to:

    ('A', 5.566363837801906)
    ('B', 6.566345194546059)
    ('C', 7.26914968376669)
    ('D', 5.546750524109014)
    ('E', 6.313278008298755)
    ('F', 6.055056179775281)
    ('G', 8.078791469194313)
    ('H', 5.673769287288758)
    ('I', 2.7835727670206123)
    ('J', 5.188361408882082)
    ('K', 4.604444444444445)
    ('L', 5.679537953795379)
    ('M', 6.808011049723757)
    ('N', 6.593103448275862)
    ('O', 4.379264510412051)
    ('P', 6.733662503630555)
    ('Q', 5.543778801843318)
    ('R', 6.831570996978852)
    ('S', 6.127062706270627)
    ('T', 5.153846153846154)
    ('U', 6.613636363636363)
    ('V', 4.890666666666666)
    ('W', 5.9698085419734905)
    ('X', 3.857142857142857)
    ('Y', 4.030516431924883)
    ('Z', 0.0)
    ('a', 3.5072)
    ('b', 4.82360146998775)
    ('c', 6.510845175766642)
    ('d', 5.3997785160575855)
    ('e', 5.489685124864278)
    ('f', 5.131147540983607)
    ('g', 5.52)
    ('h', 4.039719626168225)
    ('i', 2.9812362030905075)
    ('j', 5.371134020618556)
    ('k', 5.191780821917808)
    ('l', 5.041053921568627)
    ('m', 4.081137599330824)
    ('n', 4.065420560747664)
    ('o', 3.0949781659388647)
    ('p', 6.372469635627531)
    ('q', 5.8538461538461535)
    ('r', 6.185983827493262)
    ('s', 5.339555100997187)
    ('t', 4.037562344139651)
    ('u', 5.815718157181572)
    ('v', 5.910505836575876)
    ('w', 4.787362442314519)
    ('x', 0.0)
    ('y', 4.132762312633833)
    ('z', 0.0)
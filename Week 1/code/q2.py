#!/usr/bin/env python

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

# Exercises for Week One: The Age of the Data Product

The assignments this week are designed to be simple because there is a lot of work this week with reading and setting up the development environment. However, these two programs are important - they will eventually highlight the differences between writing a sequential analytical program of this kind (e.g. a non-distributed one) and the impact of parallelization or distributed computing. In the weeks to come we will perform similar types of analyses on the same datasets and compare and contrast the development experience as well as the speed of the analysis. 

It is probably wise to run your Python programs on your virtual machine - that way not only will you guarantee that you have a good setup and that you're ready for the rest of the course, but also that you have the data and code on your VM ready to go. 

Note that all datasets can be found in the "Resources" section of the LMS.

## Discussion 

Please answer the following questions on the discussion board. You will be graded on the quality of your answer, and how well you participate in follow up discussions. The discussion is worth a total of 10 points, 5 points for each topic.

1. Why does a data product require "Big Data"? This seemingly simple question has multiple dimensions that you might want to explore. For example - what constitutes Big Data, contextualized by the three Vs? Or, why does machine learning or data mining require large datasets to be effective? Or, why does a data generating engine require lots of fuel? Provocative answers or anecdotal experience will be the best answers. 

2. What does it mean to be "embarrassingly parallel?" Consider the homework assignments, why are these applications parallelizable? What synchronization is required? How would you build a parallel analytical system to do these tasks? Moreover, starting from these simple analytics, what types of data products could you develop?

## Question One

There is a small data set of Apache Log records in the
Resources section of the course materials called "apache.log". In any
programming language, implement a program that computes the number of hits
to the server per calendar month (e.g. Jan, Feb, Mar, etc.)

Apache web log records are formatted in Common Log format as follows:

    local - - [24/Oct/1994:13:47:19 -0600] "GET index.html HTTP/1.0" 200 150

Where the first word is either `local` or `remote` indicating the source of
the request, this is followed by `- -` and spaces, and the date of the
request in brackets. The request itself follows the date in quotes,
including the HTTP verb (GET, POST, PUT, DELETE, HEAD, etc) and the version
of HTTP used. The following integer is the HTTP response code (200 is OK,
404 is Not Found and 500 is error to name a few) and finally the size in
bytes of the response.

To parse this field for every line you simply need to split this string up,
either by using a regular expression or a string manipulation function.
Find the three letter month name, and count!

### Submission

Please submit the following:

1. A Python file with the analytics code
2. A test file containing the output of your analysis

Consider the following method of running your program:

    $ python myprog.py > output.txt

As a way to collect the results for submission.

### Dataset Info

This data is from: [http://ita.ee.lbl.gov/html/contrib/Calgary-HTTP.html](http://ita.ee.lbl.gov/html/contrib/Calgary-HTTP.html)

It contains about one year's worth of web requests to the University of
Calgary's Computer Science department server from October 24, 1994 through
October 11, 1995. There were 726,738 requests, but not all lines have a
month or timestamp associated with them, so beware!

The data itself is 5.4 MB compressed, and 52.3 MB uncompressed.

## Question Two

There is a data set containing the collected works of
Shakespeare in the Resources section of the course materials called
shakespeare.txt. In any programming language, implement a program that
computes the average word length per letter of the alphabet.

The complete Shakespeare data set is captured as one single stream file,
and whose lines are in the following format:

    I    the line from the play at this position.

For example, from Hamlet line 77902 you would find:

    hamlet@77902    HAMLET  To be, or not to be: that is the question:

In this case you would split each line of the text by tab, '\t' - the
first part of the resulting array is the title@lineno, and the second part
is the text. Use a regular expression to split the text on words, '\W' and
then, for each word, if the word length is longer than 0, add the length
of that word to the length of other words starting with the same letter,
the letter at index 0. Compute the average per word.

### Submission

Please submit the following:

1. A Python file with the analytics code
2. A test file containing the output of your analysis

Consider the following method of running your program:

    $ python myprog.py > output.txt

As a way to collect the results for submission.

### Dataset Info

This data is from: [http://www.ipl.org/div/shakespeare/](http://www.ipl.org/div/shakespeare/)

It contains the collected works of Shakespeare in a single ASCII file. It
is 8.9 MB uncompressed and 2.1 MB compressed.

## Evaluation

The discussion is worth 10 points, 5 points per question.

Grading for both questions is as follows:

* 10 points: code completeness and execution
* 10 points: correct computational results
* 5 extra points: implemented using mappers or reducers

Total possible score: 50 points.
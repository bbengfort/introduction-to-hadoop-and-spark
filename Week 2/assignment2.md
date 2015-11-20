# Exercises for Week One: An Operating System for Big Data

In this assignment we will get started working with MapReduce by writing mapper and reducer code, though we won't get to submitting it to the cluster (in the next week we will talk about using Hadoop Streaming with Python in order to submit MapReduce applications on YARN). We will revisit code from the first week so that we can see what it takes to change code from a sequential format to a distributed one - then we'll move to a classic big data set, a record of all domestic travel in the United States.  

A couple of notes:

- All datasets can be found in the "Resources" section of the LMS.
- There are some technical details in Python, particularly using `stdin` and `stdout` for use with Unix pipes that are required for this assignment. If you have any questions please ask on the discussion board!

## Discussion

Please answer the following questions on the discussion board. You will be graded on the quality of your answer, and how well you participate in follow up discussions. The discussion is worth a total of 10 points, 5 points for each topic.

1. What is better to store in a distributed storage system - billions of small files (up to 32MB per file) or millions of large files (around 256 MB per file)? Why or why not? Which Hadoop system or service will suffer from a poor file structure? What can be done to remedy that problem?

2. MapReduce is a programming abstraction that allows programmers to focus on developing algorithms and programs that can be easily parallelized and not worry about the cluster computing details. What features of MapReduce allow this to be true? Can you think of another abstraction that might similarly aid in the development of distributed computations?

## Question One

In assignment one you performed a computation that computed the number of
hits per calendar month from an apache log file. Apache web log records
are formatted in Common Log format:

    local - - [24/Oct/1994:13:47:19 -0600] "GET index.html HTTP/1.0" 200 150

Please see assignment one for more details about the structure of log
records and information about the data set.

For this assignment, determine the most popular hours of traffic for both
local and remote traffic. Your final output should report the hour twice
for each origination type with the number of hits associated with.

In order to accomplish this task write a single Mapper function that
outputs the key (hour, origin) with the value 1 (to count the hit, similar
to counting hits on a per month basis). Then create a sum reducer that
totals the hits from the mapper.

### Submission

Please submit the following:

1. A Python file with the mapper code
2. A Python file with the reducer code
3. A test file containing the output of your analysis

### Dataset Info

This data is from: [http://ita.ee.lbl.gov/html/contrib/Calgary-HTTP.html](http://ita.ee.lbl.gov/html/contrib/Calgary-HTTP.html)

It contains about one year's worth of web requests to the University of
Calgary's Computer Science department server from October 24, 1994 through
October 11, 1995. There were 726,738 requests, but not all lines have a
month or timestamp associated with them, so beware!

The data itself is 5.4 MB compressed, and 52.3 MB uncompressed.

## Question Two

Use the data set of airline on time performance from January 2013 to
complete question two. This data set was discussed in the tutorial
and the details of the columnar structure can be found in the README from
the zip file.

In the tutorial, we computed the mean delay per origin airport by
inspecting the difference in arrival time at the destination airport with
the scheduled arrival time. In this exercise, let's compute the average
flights per day for each airport in the dataset.

To do this, write a mapper that counts the number of flights per day by
outputting a key that is the airport and a value of one. Then
use an average reducer to sum the total flights and divide by the number
of days in the dataset. The reducer will output the airport key and the
computed mean.

### Submission

Please submit the following:

1. A Python file with the mapper code
2. A Python file with the reducer code
3. A test file containing the output of your analysis

### Dataset Info

This data set is from: [http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time](http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time)

It contains flight information for U.S. flights for the month of January
2013, comprising of 509,519 rows of flight departure and arrival
performance with delays. It is 8.3 MB compressed and 60 MB uncompressed.

## Question Three

In this question you need to use Hadoop in pseudo-distributed mode. This question is a check in to make sure that your Hadoop environment is set up correctly, and will allow you to get started working with Hadoop this week. In particular, you should practice your command line interaction with Hadoop as well as job submission (or at least prove that you can).

Upload a corpus of text files from a variety of news sources to HDFS. Using the supplied MapReduce word count application, wc.jar &mdash; compile and run the WordCount program upon the corpus. Remember you'll need to use the command line interface to hadoop including the `hadoop fs` and `hadoop jar` commands.

### Submission

Please submit the following:

1. A one paragraph description of your interaction with HDFS and YARN. E.g. what commands did you use to move files from your local machine to HDFS. What commands did you use to execute the MapReduce job, how did you retrieve the output? How many partitions where there? What were your overall impressions of the cluster workflow?

2. Submit the first 100 words (head) of the _last_ partition file.

### Dataset Info

This data set was collected with a tool called [Baleen](https://github.com/bbengfort/baleen) that ingests RSS feeds from a predetermined list of publications. The downloaded RSS was then converted into a text format for easy processing in this course.

It contains 37 files and is 180 KB on disk, 53 KB compressed.

## Evaluation

The discussion is worth 10 points, 5 points per question.

Grading for questions one and two is 15 points per question for a total of 30 points as follows:

* 5 points: correct and complete mapper code
* 5 points: correct and complete reducer code
* 5 points: correct results and output

Grading for question three is 10 points as follows:

* 5 points: description of HDFS and MapReduce interaction
* 5 points: correct submitted output

Total possible score: 50 points.

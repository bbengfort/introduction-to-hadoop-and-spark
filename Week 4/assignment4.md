# Exercises for Week Four: Data Analysis Patterns with MapReduce and Spark

In the last week we finally got to executing jobs on the cluster against data that was stored in the distributed file system. We took two approaches: the first leveraged Python and a microframework with Hadoop Streaming and the second used Spark's Python API to create distributed applications. In this week's assignment we'll focus less on the details of implementing jobs in Spark or MapReduce. Instead we'll look at specific patterns for programming against a cluster in a distributed fashion. Hopefully these assignments will show you how to implement more complex analyses on the cluster, as well as create routine jobs that run frequently to do data analysis.

A couple of notes:

- All datasets can be found in the "Resources" section of the LMS.
- This assignment can be completed in either Hadoop Streaming or Spark so long as only map and reduce operations are used. However, the answers will be in Hadoop Streaming format.
- In the "Resources" section there is also a `framework.py` with the micro-framework that was implemented in Chapter 3 for you to use.
- In this assignment you can turn in either question, which will be graded for the full 40 points, or both questions which will each be graded at 20 points.

## Discussion

Please answer the following question on the discussion board. You will be graded on the quality of your answer, and how well you participate in follow up discussions. The discussion is worth a total of 10 points.

1. The title of the original chapter was &ldquo;Towards Last Mile Computing&rdquo; which expresses one of the fundamental patterns for analytics with Hadoop &mdash; decreasing the analytical space from a dataset that is too big to be computed upon in a sequential fashion, to one that can be computed upon in memory. What does &ldquo;last-mile computing&rdquo; mean? Is it required for distributed analytics, why or why not?

## Question One

Compute the TF-IDF (term frequency - inverse document frequency) for words in the dataset of Reuters newswire articles. This analysis attempts to select the most important words to a document by measuring their relative frequency in the document as compared to the rest of the corpus. For example, in a news corpus, words like "baseball" or "pitcher" might not be frequent across the entire corpus, but their relative frequency in the sports section might make them more important to sports related articles. It is for this reason that TF-IDF along with simple term frequency is often used as a feature of choice in natural language processing, particularly document classification and topic modeling.

The Reuters newswire dataset includes articles from the newswire combined
into a single text document. The first thing you'll have to do is separate each document out to map them individually. This is possible because each article is headed by its document ID surrounded by 34 "=" signs as below:

    ================================== 14826 ==================================

To extract the document id simply check if the first and last character of
the line is an "=" sign, then strip them off as well as spaces, and you'll
be left with the document id.

TF-IDF is not a memory safe operation since it has to load the entire list of terms per document. Therefore

Because TF-IDF is not a memory safe operation, I have also included a list
of stopwords as part of the dataset. Please use this list of stopwords to
exclude words from the TF-IDF computation.

For more details about how to compute TF-IDF please see the discussion in
the lecture notes for Week Three. Keep in mind that in order to perform
this task, you will need to write perform three distinct MapReduce jobs.

The resulting output should be significantly long. Feel free to turn in
the whole thing, but also submit the following terms' computation for
grading:

* beacon
* draconian
* espionage
* matrix
* pizza
* shasta
* zuccherifici

### Submission

Please submit the following:

1. All Python file(s) with the various mapper code
2. All Python file(s) with the various reducer code
3. A text file containing the output of your analysis (this will be the part-00000 file on HDFS when you execute it on the cluster).

#### Spark Submission

If submitting a Spark application please submit the following:

1. A Python file with the Spark application, submittable using `spark-submit`
2. A text file containing the output of your analysis (this will be the part-00000 file on HDFS when you execute it on the cluster).

### Dataset Info

This data is part of the included corpora in NLTK: [http://nltk.org/](http://nltk.org/), a
natural language toolkit written in in Python.

It contains 10,788 news wire articles and is 3.3 MB compressed and 9.7MB
uncompressed. It is only a partial sample of reuters news articles.

## Question Two

In the second and first week we computed the average flights per day and the mean arrival delay using the On Time Performance data set for January 2013. This week, let's go farther and compute all statistical metrics for each airport's arrival delay data set. Include:

1. The number of flights per airport
2. The mean arrival delay per airport
3. The arrival delay standard deviation per airport
4. The minimum arrival delay per airport
5. The maximum arrival delay per airport

The output should be as follows:

    AIRPORT    NUMFLIGHTS    AVGDELAY    STDDEV    MIN    MAX

Where the output key is the Airport Code and the output value is the
stripe of the statistical metrics.

There will be as many rows in the output as there are Airports in the
data set. To help with grading, please highlight the following airports:

* JFK
* SFO
* IAD
* BWI
* ORD
* SEA
* LAX
* MSP
* HOU

### Submission

Please submit the following:

1. A Python file with the mapper code
2. A Python file with the reducer code
3. The first partition of your output (part-00000)

#### Spark Submission

If submitting a Spark application please submit the following:

1. A Python file with the Spark application, submittable using `spark-submit`
2. The first partition of your output (part-00000)

### Dataset Info

This data set is from: [http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time](http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time)

It contains flight information for U.S. flights for the month of January
2013, comprising of 509,519 rows of flight departure and arrival
performance with delays. It is 8.3 MB compressed and 60 MB uncompressed.

## Evaluation

The discussion is worth 10 points.

Grading for questions one and two is 20 points per question for a total of 40 points as follows:

* 7 points: correct and complete mapper code
* 7 points: correct and complete reducer code
* 6 points: correct results and output

Grading for questions one and two via a Spark submission is:

* 14 points: correct and complete Spark application
* 6 points: correct results and output

Total possible score: 50 points.

**Note**: In this assignment you have the option of only submitting an answer to one question. In that case the evaluation of the question will double the number of points, e.g. 14 points each for mapper and reducer, or 28 points for the Spark application.

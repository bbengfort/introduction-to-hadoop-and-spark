# Exercises for Week Three: A Framework for Python and Hadoop Streaming

In this assignment we will continue writing MapReduce code and executing it on the cluster using the Hadoop tools that are available to us. This week should continue to allow you to flex your newly discovered MapReduce skills by continuing to write analyses and deploy them in a distributed fashion. This week will hopefully be a tad more analytical, thinking about linear regressions and mean squared error as well as trigram analysis for language modeling. If you have any questions please don't hesitate to ask, because next week we're going to be looking at more complex jobs that require chaining and striping.

A couple of notes:

- All datasets can be found in the "Resources" section of the LMS.
- This assignment can be completed in either Hadoop Streaming or Spark so long as only map and reduce operations are used. However, the answers will be in Hadoop Streaming format.
- In the "Resources" section there is also a `framework.py` with the micro-framework that was implemented in Chapter 3 for you to use.

## Discussion

Please answer the following questions on the discussion board. You will be graded on the quality of your answer, and how well you participate in follow up discussions. The discussion is worth a total of 10 points, 5 points for each topic.

1. We've used the on-time airline flight dataset several times now to write different analyses to compute descriptive statistics. Discuss the data flow of designing a system that attempts to predict possible delays either through inferential methodologies or machine learning. Would one job be sufficient, if not how many? Are there any concerns for individual tasks?

2. Do APIs make a difference to distributed computing? E.g. does it matter that the MapReduce API is in Java or that Spark has R, Python, Java, and Scala APIs? Why or why not? What are the primary concerns when using Python on a cluster?

## Question One

In this question you will compute the mean squared error of a regression model against a data set that has correct target values. A linear model computes the linear product a coefficient vector with a data vector to compute some target variable, y. In Python this is expressed as:

    sum([b*x for (b,x) in zip(coef, vals)]) + e

Where `coef` is a list of coefficients of the linear model, `vals` is a list of the independent variables in the model, and `e` is the intercept of the linear model. The `zip` builtin function pairs elements in the two lists together. In an evaluation context, this produces a predicted value, if the real value is known, then the squared error is:

    (actual - predicted) ** 2

The data provided for this assignment contains a linear model with 280 independent variables fitted on 52,397 instances located in `blogData_train.csv`. The coefficients and intercept are located in `params.txt` where the first 280 lines are the coefficients and the last line is the intercept. The data additionally provides 60 test data sets split into days of the testing. Your job is to compute the MSE for the _entire_ test data set (not including training).

To do this, map each instance from the dataset and compute the predicted value from the linear model using the first 280 values in the row. The actual value is the 281st value (the last column) - subtract and square, then emit it along with a "dummy key". The reducer should be a simple sum reducer.

Note, one important question is as follows: how will you access the `params.txt` on the cluster?

### Stretch Goal

If you can, compute the mean squared error for each _day_ of the test, rather than an aggregate mean squared error. This stretch goal will go ungraded, but should be discussed on the discussion board. What would the mapper change in order to emit per day square errors? Would the data itself have to change?

### Submission

Please submit the following:

1. A Python file with the mapper code
2. A Python file with the reducer code
3. A text file containing the output of your analysis (this will be the part-00000 file on HDFS when you execute it on the cluster).

#### Spark Submission

If submitting a Spark application please submit the following:

1. A Python file with the spark application, submittable using `spark-submit`
2. A text file containing the output of your analysis (this will be the part-00000 file on HDFS when you execute it on the cluster).

### Dataset Info

This data is from: [https://archive.ics.uci.edu/ml/datasets/BlogFeedback](https://archive.ics.uci.edu/ml/datasets/BlogFeedback)

This data originates from blog posts. The raw HTML-documents of the blog posts were crawled and processed. The prediction task associated with the data is the prediction  of the number of comments in the upcoming 24 hours. In order  to simulate this situation, we choose a basetime (in the past) and select the blog posts that were published at most 72 hours before the selected base date/time. Then, we calculate all the features of the selected blog posts from the information that was available at the basetime, therefore each instance corresponds to a blog post. The target is the number of comments that the blog post received in the next 24 hours relative to the basetime.

The data itself is 2.5 MB compressed, and 67.97 MB uncompressed.

## Question Two

A trigram is a set of three contiguous words in a piece of text, usually with stopwords and punctuation removed. For example, the trigrams for the previous sentence are as follows:

    (trigram, three, contiguous)
    (three, contiguous, words)
    (contiguous, words, piece)
    (words, piece, text)
    (piece, text, stopwords)
    (text, stopwords, punctuation)
    (stopwords, punctuation, removed)

Trigrams are typically used in NGram models of language, where machine learning algorithms use the context of the n-1 gram to predict the nth word. These features are an important part of many natural language processing algorithms.

In this assignment, use the text corpus data set upon which you ran the WordCount job last week to compute the frequency of trigrams in the data set. A `stopwords.txt` has been provided to exclude very common words from your trigrams and you can use the `string.punctuation` to remove any punctuation.

You may use NLTK for this assignment if you are familiar with it. The chapter provides an example of how to do NLP analysis using NLTK and Hadoop. However, the use of NLTK is not required.

Note, one important question is as follows: how will you access the `stopwords.txt` on the cluster?

### Submission

Please submit the following:

1. A Python file with the mapper code
2. A Python file with the reducer code
3. The first partition of your output (part-0000)

#### Spark Submission

If submitting a Spark application please submit the following:

1. A Python file with the spark application, submittable using `spark-submit`
2. The first partition of your output (part-0000)

### Dataset Info

This data set was collected with a tool called [Baleen](https://github.com/bbengfort/baleen) that ingests RSS feeds from a predetermined list of publications. The downloaded RSS was then converted into a parsed text format for easy processing in this course.

It contains 37 files and is 180 KB on disk, 53 KB compressed.

## Evaluation

The discussion is worth 10 points, 5 points per question.

Grading for questions one and two is 20 points per question for a total of 40 points as follows:

* 7 points: correct and complete mapper code
* 7 points: correct and complete reducer code
* 6 points: correct results and output

Grading for questions one and two via a Spark submission is:

* 14 points: correct and complete spark application
* 6 points: correct results and output

Total possible score: 50 points.

# Data Analysis Patterns with MapReduce and Spark
**Big Data Computing with Hadoop Week Four Lesson**

In the first week we explored _why_ distributed analyses on large datasets are important; they facilitate the creation of data products. We've also looked at _how_ you might conduct distributed analyses through the study of Hadoop and Spark. We've learned that Hadoop provides an operating system for clustered computing, particularly a distributed file system and a resource management system that makes generic computing applicable. By using the Spark and MapReduce programming models we have already created our first distributed analyses and executed them on a cluster (even if it was only in pseudo-distributed mode).  However we have yet to answer completely _what_ types of computations we might want to do.

Obviously any specific programs and algorithms will be domain specific to the types of analyses that you're conducting. However a review of Hadoop usage shows that more complex analytics are usually composed of many smaller reusable analytics. In particular, a Hadoop workflow attempts to provide _last mile computing_ &mdash; that is a decomposition in the domain of the input dataset to a data domain that is small enough to fit in memory. For example, consider how instance based methods like kNN are abstracted into a smaller decision domain by Bayesian methods by simply computing probabilities through frequency analysis. The workflow might then go the other way and validate the decomposition by running an error computation across the entire data set.

While these workflows are standard, putting them together in a meaningful way is non-trivial particularly for heterogenous datasets that might come in a variety of forms and normalizations. By applying standard _design patterns_, however, Hadoop and Spark developers can leverage existing techniques on a wide array of data and begin to compose more complex jobs through the combination of smaller, simpler ones. Design patterns are extremely important especially for novice Hadoop developers because the distributed context often subtly changes the way computation is handled.

## Syllabus

This week's topic concerns data analysis patterns for common tasks that make up the primary grind work of most MapReduce and Spark analytics. This week is meant to expose a variety of simple computations that build together to form more complex ones. By inspecting common patterns, Hadoop and Spark developers are more easily able to apply custom or specific algorithms and analytics in a heterogenous data environment.

In particular, we'll take a look at how the combination of these techniques leads to last mile computing. Many of these patterns, filtering, aggregation, sampling, etc. are designed to reduce the amount of data output from a very large input data set. By moving the computation space from petabytes to a space that can fit into memory (perhaps 256 GB), more advanced analytics and machine learning can be performed.

Topics for this week are as follows:

- Combiners, Partitioners, and Job Chaining
- Patterns for Mappers and Reducers
- Filtering, Aggregating and Searching
- Data Organization and Workflow Management

There are three, optional academic papers this week that relate to the construction of Hadoop workflows. Most Hadoop jobs are described as dataflows, that is directed acyclic diagrams of how data flows through the computation. Through the composition of smaller analyses, a dataflow can create more complex analytics. The Oozie paper describes how jobs can be scheduled and integrated in a trackable manner - even jobs that have different implementations. Oozie is one of the primary ways to create job chained algorithms using Python. In a slightly different take, the Pig paper proposes a specialized language for dataflows, pig latin, that can then be compiled into MapReduce. Finally, the Spark paper discusses GraphX, a Spark library for graph processing dataflows.

### Spark Track

In the last week we specifically forked the Spark track from the MapReduce track, allowing students to study/turn in either Spark or MapReduce code. In this week we're discussing general design patterns that involve `map` and `reduce`. While this seems specific to MapReduce, the fact is that these design patterns are fundamental to both Spark and MapReduce as the most common types of analyses on a Hadoop cluster are based on keys/values. In fact, one way to look at many of the transformations in Spark is as specialized mappers and the actions as specialized reducers.

In this week, the reading won't specifically nominate Spark vs. MapReduce, though the examples are framed as though there is a map and a reduce phase. This should be obviously implementable in Spark in a single line. The topics will also cover the implementations of transformations such as join, merge, and sample. An understanding of the implementation of these basic patterns will definitely improve your ability to develop excellent Spark applications.

As with last week, please feel free to turn in your assignment in either MapReduce or in Spark.

### Reading

- Chapter Five of _Data Analytics with Hadoop_ (PDF provided)

#### Optional Reading

These academic papers are part of the optional reading for the course, so that you can contextualize the academic context with the commercial environment. There are three papers suggested for this week, the first related to workflow management in MapReduce, the second about a higher order abstraction for programming MapReduce, and the third about graph processing on Spark.

- Islam, Mohammad, et al. "Oozie: towards a scalable workflow management system for hadoop." Proceedings of the 1st ACM SIGMOD Workshop on Scalable Workflow Execution Engines and Technologies. ACM, 2012. (PDF provided)
- Gates, Alan F., et al. "Building a high-level dataflow system on top of Map-Reduce: the Pig experience." Proceedings of the VLDB Endowment 2.2 (2009): 1414-1425. (PDF provided)
- Gonzalez, Joseph E., et al. "Graphx: Graph processing in a distributed dataflow framework." Proceedings of OSDI. 2014. (PDF provided)

## Assignments

The course is graded in two ways: through your participation in the discussion forum and through the submission of a homework assignment. There will be more details about these topics in an assignment specific document in the learning management system, but the assignments and discussions are briefly described here. _Please ensure that you refer to the assignment document for detailed instructions_.

**Note**: This is the last week, and generally speaking we don't make it an assignment intensive week. However, I believe that the best way to learn is by doing, and I have provided assignments for you to continue implementing Spark and MapReduce jobs. In order to wrap up this last week with a focus on _discussion_, here are the options for turning in the assignment:

1. Complete and submit _either_ question 1 _or_ question 2. The question you submit will be graded for the full 40 points.

2. Complete and submit _both_ questions and each will be worth 20 points (as in other homeworks).

The option is up to you, but honestly for us it's not about the points &mdash; it's about giving you a complete learning experience. The assignments are designed to promote discussion by forcing you to encounter the technical details of Hadoop. Hopefully the flexibility in the assignment will allow you to focus on what you're most interested in getting out of the course.

### Discussion

Please answer the following questions on the discussion board. You will be graded on the quality of your answer, and how well you participate in follow up discussions.

1. The title of the original chapter was &ldquo;Towards Last Mile Computing&rdquo; which expresses one of the fundamental patterns for analytics with Hadoop &mdash; decreasing the analytical space from a dataset that is too big to be computed upon in a sequential fashion, to one that can be computed upon in memory. What does &ldquo;last-mile computing&rdquo; mean? Is it required for distributed analytics, why or why not?

### Assignment

In the last week we finally got to executing jobs on the cluster against data that was stored in the distributed file system. We took two approaches: the first leveraged Python and a microframework with Hadoop Streaming and the second used Spark's Python API to create distributed applications. In this week's assignment we'll focus less on the details of implementing jobs in Spark or MapReduce. Instead we'll look at specific patterns for programming against a cluster in a distributed fashion. Hopefully these assignments will show you how to implement more complex analyses on the cluster, as well as create routine jobs that run frequently to do data analysis.

1. Compute TF-IDF (term frequency - inverse document frequency) on a corpus of news articles.

2. Use the stripes pattern to compute all descriptive statistics for the on time flights data set.

Any of these assignments can be turned in using Spark instead of Hadoop Streaming. It is up to the student to decide which path they want to follow. Note, however that the model answers will be a mapper and a reducer that should be submitted to Hadoop Streaming. Remember, you can turn in _either_ question 1 _or_ question 2 _or_ both.

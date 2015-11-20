# A Framework for Python and Hadoop Streaming
**Big Data Computing with Hadoop Week Three Lesson**

Hadoop is largely the product of a vibrant and rich _academic_ community who study distributed computing techniques. Although Hadoop's roots are in Google - the actual open source implementation was the result of _academic_ publications. Moreover, Hadoop has been well studied in the academic literature, with new ideas put forward for a number of research questions that come up when thinking about Hadoop. Spark, the other most popular distributed computation framework, also has it's roots in academia, being originally implemented at the [Berkeley AMPLab](https://amplab.cs.berkeley.edu/) by PhD student [Matei Zaharia](https://people.csail.mit.edu/matei/).

The result has been a fairly academic approach to the engineering of these systems. In particular, the Java (and Scala) programming languages are exclusively used both in APIs and services. Due to Hadoop's popularity as a data science tool, Spark has released APIs in Python, Scala, Java, and R. However the original MapReduce application still only has a Java API as do many of the other important Hadoop ecosystem tools like HBase and Titan. This of course leads to an interesting question - how do data scientists take advantage of the Hadoop computing environment, particularly when they are most familiar with R and Python?

The answer has actually come in a few surprising forms. Hive is an implementation of a variant of SQL called HiveQL that transforms declarative queries into MapReduce jobs (though it is now being implemented on top of Spark). Pig is another high level language that provides easy, extensible, optimized data analysis declaration that can be decomposed into a MapReduce context. These tools are evolving with the Hadoop ecosystem, but in this chapter we will explore another way to interact with Hadoop: the use of Hadoop Streaming to write Python mappers and reducers (or R for that matter) that execute on a cluster.

## Syllabus

In the first week we gained a lot of perspective on the nature of Big Data and why Hadoop is fundamental to the creation of data products. We also hopefully worked through a lot of the challenges of getting a development environment set up. In the second week we explored the Hadoop architecture and components. Additionally we learned generally about how to program mappers and reducers, and interacted with Hadoop on the command line &mdash; loading data into HDFS and executing a WordCount job. In this week we will (finally) get around to writing and executing jobs on Hadoop.

In order to execute jobs natively using the MapReduce application, developers have to use the Java API and create a jar file to submit as a job, similar to what we saw last week. However, using a tool called Hadoop Streaming, any executable can be connected to map and reduce processes using Unix pipes. We will leverage this to write mappers and reducers in Python and execute them accordingly.

Topics for this week are as follows:

- Data Flow inside of a MapReduce Application
- Implementing Mappers and Reducers with Python
- Executing Streaming jobs with Unix pipes and Hadoop
- Computing on CSV data with Streaming
- A micro-framework for writing Hadoop jobs with Python
- Computing Bigram frequency analysis with NLTK

We will also continue the theme of reading conference papers related to our technologies. This week we will focus on a performance evaluation of Hadoop Streaming presented by researchers from China and Japan in 2011 at ACM RACS'11. While the writing isn't especially good (probably due to the language barrier) this paper does present an important point: the ease of use of Hadoop Streaming comes at a performance penalty. What's interesting to note, however, is that this performance penalty is only for _data intensive_ applications (the majority of Hadoop applications) but for _computation intensive_ programs (many machine learning algorithms fall in this category, e.g. partitioning decision trees or computing gradients for boosting) Hadoop Streaming may actually allow more optimized languages to perform better.

### Spark Track

At this point in the course we've reached an alternate path that students can take. While it's critical to understand how cluster computing works and the abstractions of MapReduce for any distributed processing, there are choices regarding the implementation details. Students wishing to study further in Spark may therefore read the optional papers in addition to (or instead of) the Hadoop Streaming materials.

The discussion is generic enough that both Spark and Streaming answers can be discussed easily. The homework assignments can be submitted in _either_ Hadoop Streaming or as a Spark application. This is true for next week's homework assignments as well. As you move into Statistics.com's Advanced Hadoop courses, both Spark and MapReduce will be explored in more detail.

The conference paper for the Spark track concerns the implementation of SparkSQL &mdash; a module that integrates relational data processing with the RDD api. SparkSQL provides a declarative DataFrame API that integrates procedural Spark code while also allowing SQL-like queries to be made against a data set in an optimized fashion. This API therefore gives data scientists a more familiar interaction with distributed data, as well as a powerful model for performing complex analyses and machine learning.

### Reading

- Chapter Three of _Data Analytics with Hadoop_ (PDF provided)
- Ding, Mengwei, et al. "More convenient more overhead: the performance evaluation of Hadoop streaming." Proceedings of the 2011 ACM Symposium on Research in Applied Computation. ACM, 2011. (PDF provided)

#### Optional Reading

- Chapter Four of _Data Analytics with Hadoop_ (PDF provided)
- Armbrust, Michael, et al. "Spark SQL: Relational data processing in Spark." Proceedings of the 2015 ACM SIGMOD International Conference on Management of Data. ACM, 2015. (PDF provided)

## Assignments

The course is graded in two ways: through your participation in the discussion forum and through the submission of a homework assignment. There will be more details about these topics in an assignment specific document in the learning management system, but the assignments and discussions are briefly described here. _Please ensure that you refer to the assignment document for detailed instructions_.

### Discussion

Please answer the following questions on the discussion board. You will be graded on the quality of your answer, and how well you participate in follow up discussions.

1. We've used the on-time airline flight dataset several times now to write different analyses to compute descriptive statistics. Discuss the data flow of designing a system that attempts to predict possible delays either through inferential methodologies or machine learning. Would one job be sufficient, if not how many? Are there any concerns for individual tasks?

2. Do APIs make a difference to distributed computing? E.g. does it matter that the MapReduce API is in Java or that Spark has R, Python, Java, and Scala APIs? Why or why not? What are the primary concerns when using Python on a cluster?

### Assignment

In this assignment we will continue writing MapReduce code and executing it on the cluster using the Hadoop tools that are available to us. This week should continue to allow you to flex your newly discovered MapReduce skills by continuing to write analyses and deploy them in a distributed fashion. This week will hopefully be a tad more analytical, thinking about linear regressions and mean squared error as well as trigram analysis for language modeling. If you have any questions please don't hesitate to ask, because next week we're going to be looking at more complex jobs that require chaining and striping.

1. Compute the mean squared error of a model from a linear regression.

2. Compute the frequency of trigrams in our news article data set. However, this is more than advanced word count, as we'll want to also remove stop words and punctuation from our dataset.

Note that now that we're executing on the cluster - any of these assignments can be turned in using Spark instead of Hadoop Streaming. It is up to the student to decide which path they want to follow. Note, however that the model answers will be a mapper and a reducer that should be submitted to Hadoop Streaming.

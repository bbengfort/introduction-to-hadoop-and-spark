# An Operating System for Big Data
**Big Data Computing with Hadoop Week Two Lesson**

The original intended use of Hadoop was to perform parallel processing of HTML files crawled from the Internet to develop an index for search algorithms and to extract links. Indeed, Hadoop still shines in this task when using the open source web crawler, Nutch &mdash; the Internet is a big place and a web crawler generates a huge amount of data! When considering the web crawler task, the two elements of distributed computing - distributed storage and a distributed computation become very obvious. How do you store millions of files and hundreds of terabytes in such a way that you can process them easily but such that you are assured you don't lose data? How do you create a word count or an index from that data quickly?

Hadoop solves these problems with two systems: HDFS and YARN. Both of these systems are made up of daemon services that run on every node in the cluster, coordinated by master services that run on more powerful machines. Centralized coordination of the cluster means a simple architecture that is more easily managed and developed upon. Moreover, Hadoop provides guarantees for fault tolerance, consistency, durability, and recoverability through speculative execution and data duplication. This makes Hadoop a complete distributed computing system that is easily deployed, configured, and managed.

It is for this reason and because of its open source license that Hadoop has evolved from a distributed computing framework to a platform or operating system for Big Data. Hadoop clusters are spun up on demand on elastic map reduce for cheap, massive computation or are used as a permanent data warehousing technique for safe, redundant data storage. Data management frameworks like Hive and HBase mean that Hadoop can be built up as a data warehouse and specialized computing frameworks like Pig, Oozie, or Mahout mean that Hadoop can be leveraged for a wide variety of computation.   

## Syllabus

In this week we discuss Hadoop as an operating system or platform for Big Data. We'll be going over the fundamental concepts of distributed computing on a cluster of nodes; then dive into the architecture of Hadoop in particular.

Topics for this week are as follows:

- Basic concepts in distributed computing.
- The Hadoop architecture and services.
- Hadoop's Distributed File System (HDFS).
- Working with HDFS on the command line.
- Programming a distributed computation.
- The basics of MapReduce for distributed computing.
- Submitting a data analysis job to YARN.

We will also continue the theme of reading conference papers related to our technologies. This week we will focus on HDFS in our optional reading, a paper presented by Yahoo! in 2010 to IEEE MSST 2010.

### Reading

- Chapter Two of _Data Analytics with Hadoop_ (PDF provided)
- Tutorial on implementing MapReduce using Unix Pipes

#### Optional Reading

- Shvachko, Konstantin, et al. "The hadoop distributed file system." Mass Storage Systems and Technologies (MSST), 2010 IEEE 26th Symposium on. IEEE, 2010. (PDF provided)

## Assignments

The course is graded in two ways: through your participation in the discussion forum and through the submission of a homework assignment. There will be more details about these topics in an assignment specific document in the learning management system, but the assignments and discussions are briefly described here. _Please ensure that you refer to the assignment document for detailed instructions_.

### Discussion

Please answer the following questions on the discussion board. You will be graded on the quality of your answer, and how well you participate in follow up discussions.

1. What is better to store in a distributed storage system - billions of small files (up to 32MB per file) or millions of large files (around 256 MB per file)? Why or why not? Which Hadoop system or service will suffer from a poor file structure? What can be done to remedy that problem?

2. MapReduce is a programming abstraction that allows programmers to focus on developing algorithms and programs that can be easily parallelized and not worry about the cluster computing details. What features of MapReduce allow this to be true? Can you think of another abstraction that might similarly aid in the development of distributed computations?

### Assignment

In this assignment we will get started working with MapReduce by writing mapper and reducer code, though we won't get to submitting it to the cluster (in the next week we will talk about using Hadoop Streaming with Python in order to submit MapReduce applications on YARN). We will revisit code from the first week so that we can see what it takes to change code from a sequential format to a distributed one - then we'll move to a classic big data set, a record of all domestic travel in the United States.  

1. We will revisit the Apache Web logs and the parsing we did in the first week, but this time incorporate more information such as the origination and determine the frequency of traffic per hour, per origination.

2. Compute the average flights per day per airport for January 2013.

3. Submit a pre-written WordCount job on the cluster, computing on a set of files that have been loaded into HDFS.

Note - there are some technical details in Python, particularly using stdin and stdout for use with Unix pipes that are required for this assignment. If you have any questions please ask on the discussion board!

# The Age of the Data Product
**Big Data Computing with Hadoop Week One Lesson**

The term "Big Data” has come into vogue for an exciting new set of applications and techniques that are powering modern applications and whose novelty seems to be changing the way the world is computing. However, much to the statistician's chagrin, this term seems to usually refer to the application of well known statistical techniques. Although "Big Data” is now officially a buzzword (and possibly also a synergistic paradigm), the fact is that modern distributed computation techniques are allowing the analysis of data sets far larger then those that could be typically analyzed in the past.

This trend is the product of a combination of rapidly increasing data sets generated from the Internet, and the observation that these data sets are able to give better predictive power particularly because of their magnitude. It also helps that novel data sets have been exploited to the awe of the general public, e.g. Nate Silver's seemingly magical ability to predict the 2008 election using such Big Data techniques.

The source of this new trend in technology started because of the release of Apache Hadoop in 2005. Hadoop is an open source project based on two seminal papers produced by Google: The Google File System (2003) and MapReduce: Simplified Data Processing on Large Clusters (2004). These two papers discuss the two key components that make up Hadoop: a distributed File System and MapReduce functional computations. Now it seems that whenever someone says "Big Data” they probably are referring to computation using Hadoop.

Even more recently, a paper out of Berkeley: Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing (2012) introduced the core abstraction of what would eventually become Spark. Spark is truly targeted towards data science and analytics, providing an API in the most popular analytical programming languages: R and Python. Spark on top of Hadoop has truly made distributed machine learning the provenance of modern data science.

### A Broad Outline

This class will introduce statisticians to Hadoop, and provide an exemplar workflow for using Hadoop, writing MapReduce jobs, and finally leveraging Hadoop Streaming to conclude work in Python. In this course you will learn:

- What is Hadoop and the software components of the Hadoop Ecosystem
- How to manage data on a distributed file system
- How to write MapReduce jobs to perform computations with Hadoop
- How to utilize Hadoop Streaming to output jobs to Python

Please note, that although this course is introductory, it is intended for intermediate students. Knowledge of server command line operations and programming  is required.

Basically we hope to provide you with enough introductory knowledge so that you can get started working in a distributed environment. With any luck, we'll also be able to point the way forward for you to target exactly the systems and programs that you need to learn for your own work and analytics. Hadoop is a big ecosystem, and hopefully by gaining a broad perspective, you'll be able to navigate it more effectively.

## Syllabus

This week is a foundational week - the readings concern the history and motivation of Hadoop, as well as building data products. They aren't (or you can skip) the detailed technical parts. Instead the primary goals for this week are to get your development environment setup - a virtual machine running Hadoop in psuedo-distributed mode. You can use either the virtual machine we provide, set one up yourself using the instructions, or download one from Cloudera or Hortonworks.

Topics for this week are as follows:

- Data products: economic engines that generate data.
- How does the data science pipeline fit with big data?
- What is a distributed computation?
- What is a distributed file system?
- What does it mean to be embarrasingly parallel?
- Getting set up with a pseudo-distributed virtual machine.

The readings will include foundational academic papers so that you can get a better background on the foundation that the Hadoop ecosystem is built upon.

### Software

The primary goal of this week is to get your development environment set up.

Hadoop is deployed on Linux servers as a service of several background daemons to run on a networked cluster. In order to develop for Hadoop, data scientists use a "Single Node Cluster" in "Pseudo-Distributed Mode" to develop MapReduce jobs and to debug and test before moving out to the larger cluster. As such, you'll need to be familiar with utilizing Linux and be comfortable with the command line. If you're new to Linux or the command line, you might want to do [The Command Line Crash Course](http://cli.learncodethehardway.org/book/).

One common way to develop in pseudo-distributed node is through the use of a Linux virtual machine, which maintains the Hadoop environment on a guest operating system on your main development box. In order to create a virtual environment, you need some sort of virtualization software like [VirtualBox](http://www.virtualbox.org/), [VMWare](http://www.vmware.com/products/desktop-virtualization), or [Parallels](http://www.parallels.com/).

The installation instructions discuss how to setup an Ubuntu x64 virtual machine of your own. While occassionally it is better to follow the installation instructions so that you understand your setup, the course also provides a preconfigured one for use with VMWare or VirtualBox. If you're completely stuck or don't have much experience with Linux, you can instead download the VMDK from the following link:

[http://bit.ly/hfpd3vm](http://bit.ly/hfpd3vm)

The VMDKs are very large, 1.7 GB and 2.7 GB compressed (one VMDK is headless, so a terminal only, the other has a desktop GUI), so keep that in mind when downloading. It has been zipped using 7zip (a free Zip alternative) that you'll need to use to decompress the file on Windows.

To use the virtual disk, you'll create a new virtual machine in VirtualBox or VMWare and add this file as the virtual disk. Help for specific sections can be found in the forum.

### Reading

Required text is [_Data Analytics with Hadoop: An Introduction for Data Scientists_](http://shop.oreilly.com/product/0636920035275.do) by Benjamin Bengfort and Jenny Kim. This book focuses on a wide introduction to Hadoop and Data Science from the perspective of a data scientist, and not software developer. The course text is not currently available as it is in pre-release for next year, however we will happily provide you PDF copies for your use only.

Optionally the video training series, [_Hadoop Fundamentals for Data Scientists: Hadoop's Architecture, Distributed Computing Framework, and Analytical Ecosystem_](http://shop.oreilly.com/product/0636920035183.do) by Benjamin Bengfort and Jenny Kim is recommended for a deeper dive on the material. Statistics.com students who are interested in this video training may receive a discount code for the video depending on availability and interest.

#### Reading Assignments

- Chapter One of _Data Analytics with Hadoop_ (PDF provided)
- Setting up a Hadoop Development Environment (PDF provided)

#### Supplementary Reading

- Ghemawat, Sanjay, Howard Gobioff, and Shun-Tak Leung. "The Google file system." ACM SIGOPS operating systems review. Vol. 37. No. 5. ACM, 2003. (PDF provided)
- Dean, Jeffrey, and Sanjay Ghemawat. "MapReduce: simplified data processing on large clusters." Communications of the ACM 51.1 (2008): 107-113. (PDF provided)

#### Optional Reading

- The first section of Chapter Four (until page #76) of _Data Analytics with Hadoop_ (PDF provided)
- Zaharia, Matei, et al. "Resilient distributed datasets: A fault-tolerant abstraction for in-memory cluster computing." Proceedings of the 9th USENIX conference on Networked Systems Design and Implementation. USENIX Association, 2012. (PDF provided)


## Assignments

The course is graded in two ways: through your participation in the discussion forum and through the submission of a homework assignment. There will be more details about these topics in an assignment specific document in the learning management system, but the assignments and discussions are briefly described here. _Please ensure that you refer to the assignment document for detailed instructions_.

### Discussion

Please answer the following questions on the discussion board. You will be graded on the quality of your answer, and how well you participate in follow up discussions.

1. Why does a data product require "Big Data"? This seemingly simple question has multiple dimensions that you might want to explore. For example - what constitutes Big Data, contextualized by the three Vs? Or, why does machine learning or data mining require large datasets to be effective? Or, why does a data generating engine require lots of fuel? Provocative answers or anecdotal experience will be the best answers.

2. What does it mean to be "embarrassingly parallel?" Consider the homework assignments, why are these applications parallelizable? What synchronization is required? How would you build a parallel analytical system to do these tasks? Moreover, starting from these simple analytics, what types of data products could you develop?

### Assignment

The assignments this week are designed to be simple because there is a lot of work this week with reading and setting up the development environment. However, these two programs are important - they will eventually highlight the differences between writing a sequential analytical program of this kind (e.g. a non-distributed one) and the impact of parallelization or distributed computing. In the weeks to come we will perform similar types of analyses on the same datasets and compare and contrast the development experience as well as the speed of the analysis.

It is probably wise to run your Python programs on your virtual machine - that way not only will you guarantee that you have a good setup and that you're ready for the rest of the course, but also that you have the data and code on your VM ready to go.

Therefore please consider this assignment as a "checkpoint" of your ability to complete this course.

1. Compute the monthly hit frequency of a website based on web log data.

2. Compute the average word length per letter in the complete works of Shakespeare.

#### Primary Goal

The primary goal of this week is to get your development environment set up. By the end of the week you should be ready to interact with HDFS and YARN, and possibly even Spark. This is not an easy goal, which is why we have given you the entire week to do it!

## Software

Hadoop is a distributed computing framework that relies on modern server technology to deploy to a cluster. In this course we will be focusing on the analytics and software development, rather than systems administration or operations; however you will still be required to use the Linux terminal to interact with Hadoop in a meaningful way (e.g. to execute jobs or interact with HDFS). This page outlines the various software technologies that will be required as prerequisite to the course.

### Linux and Virtual Machines

Hadoop is deployed on Linux servers as a service of several background daemons to run on a networked cluster. In order to develop for Hadoop, data scientists use a "Single Node Cluster" in "Pseudo-Distributed Mode" to develop MapReduce jobs and to debug and test before moving out to the larger cluster. As such, you'll need to be familiar with utilizing Linux and be comfortable with the command line. If you're new to Linux or the command line, you might want to do [The Command Line Crash Course](http://cli.learncodethehardway.org/book/). 

One common way to develop in pseudo-distributed node is through the use of a Linux virtual machine, which maintains the Hadoop environment on a guest operating system on your main development box. In order to create a virtual environment, you need some sort of virtualization software like [VirtualBox](http://www.virtualbox.org/), [VMWare](http://www.vmware.com/products/desktop-virtualization), or [Parallels](http://www.parallels.com/).

The installation instructions discuss how to setup an Ubuntu x64 virtual machine of your own. While occassionally it is better to follow the installation instructions so that you understand your setup, the course also provides a preconfigured one for use with VMWare or VirtualBox. If you're completely stuck or don't have much experience with Linux, you can instead download the VMDK from the following link:

[http://bit.ly/hfpd3vm](http://bit.ly/hfpd3vm)

The VMDKs are very large, 1.7 GB and 2.7 GB compressed (one VMDK is headless, so a terminal only, the other has a desktop GUI), so keep that in mind when downloading. It has been zipped using 7zip (a free Zip alternative) that you'll need to use to decompress the file on Windows.

To use the virtual disk, you'll create a new virtual machine in VirtualBox or VMWare and add this file as the virtual disk. Help for specific sections can be found in the forum. 

### Hadoop

Hadoop itself is several different software processes that run as daemons on Linux, each of which comprise a YARN service and HDFS. There are many different versions of Hadoop, but at the time of this writing, you should be using a Hadoop version 2.5.0 or greater. If you'd like to configure your own Linux box in pseudo-distributed mode you can find instructions at Installing a Development Environment.

Note that there are also several distributions of Hadoop from service providers like Cloudera and Hortonworks. If your institution or company uses one of these distributions, please feel free to download their virtual machines for development upon. Some of the instructions (particularly paths) might need minor modification, but it should not be too difficult.

### Software Development

Although the MapReduce API is written in Java and intended for Java development, this course will utilize Hadoop Streaming and Python to interact with Hadoop. All code will be in Python and you'll be expected to understand how to develop with Python.

Make sure you have Python available and a text editor such as Sublime Text to write your code. Once the course opens, we will be working with Python to execute jobs via Hadoop Streaming. There are several frameworks available to assist writing Hadoop jobs in Python, which will be discussed during the course.

#### If you know Java or other languages... 

Those with experience in Java may use the Native API to implement MapReduce jobs, but the class will focus on Hadoop Streaming. To access more advanced functionality you'll need some tool to develop and compile Java. The most well known are Eclipse and NetBeans, as well as a popular, professional IDE- IntelliJIDEA. For this course, however, this is completely optional.

For the programming work, any programming language that accepts data from stdin and writes to stdout (R, Ruby, Perl, etc.) can be used, but all examples and pseudo-code will be in Python.

### SSH

One common way to interact with a Hadoop VM, especially the server edition in headless mode is to SSH in from your host machine. If you're using the desktop VM you can ignore these instructions, however.  If you're on Windows, to SSH into your VM you'll need a client called [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html), on Mac or Linux you'll be fine using SSH from the terminal. Note that this class does not cover command line usage, ssh, or virtual machine setup. The best place to ask for help on these topics will be in the forums, and if you're an expert on these topics, please help your fellow classmates as well!
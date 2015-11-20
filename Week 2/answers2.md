# Assignment Two Model Answers
**Big Data with Hadoop Week Two Lesson**

The following document describes model answers for questions one, two, and three in the homework assignment. Please compare your results and work with the work described here. Note that your answer may not be exactly the same as the answer below, but should be well represented by what is described.

## Question One

In this question you were required to submit the following:

1. A Python file with the mapper code
2. A Python file with the reducer code
3. A test file containing the output of your analysis

The Python mapper is as follows:

    import sys

    SEP = "\t"

    def mapper(sep=SEP):
        """
        Read input from stdin, parse the log file and emit ((hour, origin), 1).
        """

        for line in sys.stdin:
            try:
                origin = line.split()[0]
                hour   = int(line.split(':')[1])
                key    = (hour, origin)

                sys.stdout.write(
                    "{}{}{}\n".format(key, sep, 1)
                )
            except (IndexError, ValueError):
                sys.stderr.write("Couldn't parse line \"{}\"\n".format(line))
                continue

    if __name__ == '__main__':
        mapper()

The Python reducer is as follows:

    import sys

    from itertools import groupby
    from operator import itemgetter

    SEP = "\t" # Delimiter to separate key/value pairs

    def parse_input(sep=SEP):
        """
        Read and parse input, spliting on the sep character, creating a generator
        that can be passed into group by for efficient aggregation.
        """
        for line in sys.stdin:
            yield line.rstrip().split(sep, 1)

    def reducer(sep=SEP):
        """
        Sum the number of hits per hour, origin on the web server. Use the
        `groupby` function in `itertools` to group by key.
        """

        for key, values in groupby(parse_input(sep), itemgetter(0)):
            try:
                total = sum(int(count) for _, count in values)
                sys.stdout.write(
                    "{}{}{}\n".format(key, sep, total)
                )
            except ValueError:
                sys.stderr.write("Could not sum for key: {}\n".format(key))
                continue

    if __name__ == '__main__':
        reducer()

The output should be similar to:

    (0, 'local')	8708
    (0, 'remote')	10059
    (1, 'local')	5166
    (1, 'remote')	9229
    (10, 'local')	22755
    (10, 'remote')	20635
    (11, 'local')	26902
    (11, 'remote')	20697
    (12, 'local')	24860
    (12, 'remote')	21962
    (13, 'local')	30441
    (13, 'remote')	21032
    (14, 'local')	33169
    (14, 'remote')	21414
    (15, 'local')	30571
    (15, 'remote')	19826
    (16, 'local')	32317
    (16, 'remote')	18869
    (17, 'local')	29046
    (17, 'remote')	16044
    (18, 'local')	19209
    (18, 'remote')	14025
    (19, 'local')	15435
    (19, 'remote')	15148
    (2, 'local')	3788
    (2, 'remote')	8920
    (20, 'local')	16077
    (20, 'remote')	13632
    (21, 'local')	14286
    (21, 'remote')	13125
    (22, 'local')	11585
    (22, 'remote')	12249
    (23, 'local')	11178
    (23, 'remote')	10711
    (3, 'local')	3036
    (3, 'remote')	7869
    (4, 'local')	2310
    (4, 'remote')	7678
    (5, 'local')	2416
    (5, 'remote')	8395
    (6, 'local')	2455
    (6, 'remote')	10609
    (7, 'local')	3218
    (7, 'remote')	13466
    (8, 'local')	8860
    (8, 'remote')	17733
    (9, 'local')	15819
    (9, 'remote')	18190

## Question Two

In this question you were required to submit the following:

1. A Python file with the mapper code
2. A Python file with the reducer code
3. A test file containing the output of your analysis

The Python mapper is as follows:

    import sys
    import csv

    SEP = "\t" # Delimiter to separate key/value pairs

    def mapper(sep=SEP):
        """
        Read input from stdin, parse the TSV file and emit (airport, 1) for each
        origin and destination airport (e.g. this is counting the number of
        arriving and departing flights at all airports).
        """
        reader = csv.reader(sys.stdin, delimiter='\t')
        for row in reader:
            origin      = row[6]
            destination = row[9]

            # First emit the origin airport
            sys.stdout.write(
                "{}{}{}\n".format(origin, sep, 1)
            )

            # Then emit the destination airport
            sys.stdout.write(
                "{}{}{}\n".format(destination, sep, 1)
            )

    if __name__ == '__main__':
        mapper()

The Python reducer is as follows:

    import sys

    from itertools import groupby
    from operator import itemgetter

    SEP  = "\t" # Delimiter to separate key/value pairs
    DAYS = 31   # The number of days in January to average by day

    def parse_input(sep=SEP):
        """
        Read and parse input, splitting on the sep character, creating a generator
        that can be passed into group by for efficient aggregation.
        """
        for line in sys.stdin:
            yield line.rstrip().split(sep, 1)

    def reducer(sep=SEP):
        """
        Uses groupby and parse_input to compute the average number of flights
        per day, in this case there are 31 days in January.
        """

        for key, values in groupby(parse_input(sep), itemgetter(0)):
            try:
                total = sum(int(count) for _, count in values)
                average = float(total) / float(DAYS)
                sys.stdout.write(
                    "{}{}{:0.2f}\n".format(key, sep, average)
                )
            except ValueError:
                sys.stderr.write("Could not sum for key: {}\n".format(key))
                continue

    if __name__ == '__main__':
        reducer()

The output should be similar to:

    ABE	19.32
    ABI	13.74
    ABQ	133.81
    ABR	4.03
    ABY	5.61
    ACT	7.74
    ACV	17.06
    ADK	0.58
    ADQ	3.61
    AEX	19.65
    AGS	16.03
    ALB	53.06
    ALO	3.74
    AMA	39.32
    ANC	79.32
    APN	3.48
    ART	3.48
    ASE	40.97
    ATL	2087.65
    ATW	25.10
    AUS	241.58
    AVL	18.65
    AVP	10.74
    AZA	1.97
    AZO	14.61
    BDL	113.13
    BET	5.35
    BFL	19.84
    BGM	3.61
    BGR	1.97
    BHM	89.58
    BIL	12.55
    BIS	20.84
    BJI	3.97
    BKG	2.65
    BLI	5.16
    BMI	16.42
    BNA	301.16
    BOI	59.68
    BOS	526.87
    BQK	4.97
    BQN	8.65
    BRD	4.90
    BRO	13.10
    BRW	4.58
    BTM	3.94
    BTR	43.39
    BTV	26.52
    BUF	122.39
    BUR	132.26
    BWI	504.19
    BZN	17.10
    CAE	34.29
    CAK	48.48
    CDC	3.48
    CDV	3.87
    CEC	5.45
    CHA	25.74
    CHO	9.61
    CHS	69.23
    CIC	6.00
    CID	44.65
    CIU	3.68
    CLD	14.77
    CLE	245.42
    CLL	13.61
    CLT	737.74
    CMH	142.39
    CMI	11.48
    CMX	4.00
    COD	4.00
    COS	51.77
    COU	4.55
    CPR	12.84
    CRP	38.35
    CRW	18.32
    CSG	10.71
    CVG	200.48
    CWA	16.55
    DAB	7.97
    DAL	250.74
    DAY	63.90
    DCA	403.10
    DEN	1150.29
    DFW	1514.58
    DHN	7.48
    DLH	17.10
    DRO	9.58
    DRT	3.45
    DSM	75.90
    DTW	826.94
    EAU	4.00
    ECP	21.35
    EGE	20.39
    EKO	5.45
    ELM	9.48
    ELP	106.35
    ERI	5.29
    ESC	3.48
    EUG	24.65
    EVV	22.65
    EWN	3.68
    EWR	638.58
    EYW	24.23
    FAI	20.77
    FAR	34.39
    FAT	59.87
    FAY	14.52
    FCA	7.52
    FLG	9.61
    FLL	399.87
    FNT	21.19
    FSD	33.97
    FSM	13.29
    FWA	28.19
    GCC	9.77
    GCK	4.00
    GEG	47.23
    GFK	14.55
    GGG	4.00
    GJT	25.32
    GNV	17.39
    GPT	24.71
    GRB	30.29
    GRI	3.74
    GRK	27.77
    GRR	57.13
    GSO	51.81
    GSP	52.90
    GTF	9.16
    GTR	5.45
    GUC	2.35
    GUM	2.00
    HDN	12.58
    HIB	3.42
    HLN	8.90
    HNL	283.13
    HOB	3.16
    HOU	308.35
    HPN	45.77
    HRL	22.71
    HSV	40.03
    IAD	388.32
    IAH	968.00
    ICT	54.65
    IDA	13.71
    ILM	17.48
    IMT	3.74
    IND	159.61
    INL	3.45
    IPL	4.00
    ISN	9.94
    ISP	26.29
    ITH	3.61
    ITO	38.58
    IYK	3.94
    JAC	17.61
    JAN	52.48
    JAX	123.81
    JFK	591.39
    JLN	4.00
    JNU	19.52
    KOA	71.13
    KTN	12.00
    LAN	19.23
    LAR	4.00
    LAS	708.06
    LAW	10.00
    LAX	1132.77
    LBB	37.84
    LCH	11.42
    LEX	38.71
    LFT	31.13
    LGA	512.61
    LGB	69.84
    LIH	67.03
    LIT	78.90
    LMT	4.00
    LNK	16.23
    LRD	13.19
    LSE	5.61
    LWS	3.35
    MAF	45.81
    MBS	16.74
    MCI	260.26
    MCO	612.23
    MDT	32.52
    MDW	421.06
    MEM	190.45
    MFE	23.13
    MFR	16.77
    MGM	20.13
    MHK	9.35
    MHT	51.19
    MIA	464.23
    MKE	184.61
    MKG	4.00
    MLB	7.87
    MLI	28.77
    MLU	18.19
    MMH	6.19
    MOB	29.10
    MOD	5.97
    MOT	13.81
    MQT	5.29
    MRY	31.03
    MSN	57.61
    MSO	15.00
    MSP	724.55
    MSY	218.90
    MTJ	13.42
    MYR	19.23
    OAJ	9.06
    OAK	229.94
    OGG	127.84
    OKC	121.16
    OMA	108.97
    OME	5.87
    ONT	114.35
    ORD	1539.58
    ORF	85.48
    OTH	2.00
    OTZ	5.87
    PAH	4.00
    PBI	139.13
    PDX	255.52
    PHF	12.52
    PHL	433.68
    PHX	947.55
    PIA	27.19
    PIH	5.45
    PIT	174.94
    PLN	3.35
    PNS	49.23
    PPG	0.58
    PSC	16.19
    PSE	4.87
    PSG	4.00
    PSP	72.77
    PVD	73.87
    PWM	31.39
    RAP	17.03
    RDD	6.10
    RDM	15.52
    RDU	253.39
    RFD	0.61
    RHI	5.16
    RIC	98.29
    RKS	12.00
    RNO	93.10
    ROA	15.74
    ROC	56.58
    ROW	5.74
    RST	10.65
    RSW	179.16
    SAF	5.29
    SAN	394.94
    SAT	215.26
    SAV	41.03
    SBA	59.16
    SBN	25.19
    SBP	25.77
    SCC	3.74
    SCE	3.87
    SDF	80.90
    SEA	467.16
    SFO	852.65
    SGF	30.84
    SGU	11.13
    SHD	0.84
    SHV	37.81
    SIT	5.97
    SJC	203.61
    SJT	7.74
    SJU	146.68
    SLC	584.77
    SMF	221.55
    SMX	6.90
    SNA	216.58
    SPI	8.97
    SPS	6.00
    SRQ	26.45
    STL	302.71
    STT	24.32
    STX	5.10
    SUN	8.42
    SUX	3.74
    SWF	8.90
    SYR	42.13
    TLH	26.16
    TPA	349.06
    TRI	12.84
    TTN	0.74
    TUL	101.97
    TUS	106.58
    TVC	14.19
    TWF	6.10
    TXK	5.74
    TYR	13.45
    TYS	57.97
    VLD	5.55
    VPS	27.16
    WRG	4.00
    XNA	64.03
    YAK	3.87
    YUM	16.06

## Question Three

In this question you were required to submit the following:

1. A one paragraph description of your interaction with HDFS and YARN. E.g. what commands did you use to move files from your local machine to HDFS. What commands did you use to execute the MapReduce job, how did you retrieve the output? How many partitions where there? What were your overall impressions of the cluster workflow?

2. Submit the first 100 words (head) of the _last_ partition file.

The paragraph should include the following topics:

* uploaded the data to HDFS using `copyFromLocal` or `put`
* compiled the WordCount job using javac and the Hadoop library
* submitted the job using the `hadoop jar` command
* fetched the output using `copyFromRemote` or `get` or `getmerge`

We will review the word count output, it is too long to embed in the answers document, but it should be readily clear if it's correct or not.

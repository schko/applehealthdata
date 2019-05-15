#!/usr/bin/python
# Simple Python script to parse Apple Health Values out of the export.xml into a pipe delimited txt file
# Iniitally adapted from from: https://github.com/kdesch5000/AppleHealthData
def parseXML(inputFile):
    import re, sys
    from datetime import datetime
    import pandas as pd

    # Assumes you run the script in same location as the exported data
    healthlog = inputFile

    # Initi counter
    count =0

    # Init dataframe and dictionary
    datadict = {'startDate': [], 'endDate': [], 'source': [], 'recordType': [], 'val': [], 'unit': []}

    # determine number of lines in export.xml
    num_lines = sum(1 for line in open(healthlog,'r'))

    FMT = '%Y-%m-%d %H:%M:%S'

    # loop through export.eml
    for line in open(healthlog,'r'):
        healthdataval = None
        # find record types
        if re.search(r"<Record type=", line) or re.search(r"<Workout workoutActivityType=", line):
            if re.search(r"<Record type=", line):
                recordtype = re.search(r"<Record type=\"\S+\"",line)
            else:
                recordtype = re.search(r"<Workout workoutActivityType=\"\S+\"", line)
            recordtypeval = recordtype.group()

            # get source of value
            sourceName =re.search(r"sourceName\S\S\S+\s+\S+", line)
            sourceNameval = sourceName.group()

            # Get value of record type
            healthdata = re.search(r"value\S\S\w+",line)
            recSubString = recordtypeval[14:-1]
            if healthdata is not None:
                if recSubString == "HKCategoryTypeIdentifierSleepAnalysis":
                    starttime = re.search(r"startDate\S\S\d+\-\d+\-\d+\s+\d+\:\d+\:\d+", line)
                    endtime = re.search(r"endDate\S\S\d+\-\d+\-\d+\s+\d+\:\d+\:\d+", line)
                    tdelta = datetime.strptime(endtime.group()[9:], FMT) - datetime.strptime(starttime.group()[11:], FMT)
                    healthdataval = "0000000" + str(tdelta)[:1]
                if recSubString == "HKQuantityTypeIdentifierActiveEnergyBurned" or recSubString == "HKQuantityTypeIdentifierDistanceWalkingRunning" or \
                        recSubString == "HKQuantityTypeIdentifierBasalEnergyBurned":
                        healthdataval = re.search(r"value\S\S[+-]?([0-9]*[.])?[0-9]+", line).group()
                else:
                    healthdataval = healthdata.group()
            elif recordtypeval[30:-1] == "HKWorkoutActivityTypeRunning":
                healthdataval = re.search(r"duration\S\S[+-]?([0-9]*[.])?[0-9]+", line).group()[len("duration"):]

            # Get end date/time of data collection
            datetime2 = re.search(r"startDate\S\S\d+\-\d+\-\d+\s+\d+\:\d+\:\d+",line)
            datetime2val = datetime2.group()

            # save results to dictionary
            datadict['startDate'].append(datetime2val[11:])
            # Get end date/time of data collection
            datetime2 = re.search(r"endDate\S\S\d+\-\d+\-\d+\s+\d+\:\d+\:\d+", line)
            datetime2val = datetime2.group()
            datadict['endDate'].append(datetime2val[9:])
            datadict['source'].append(sourceNameval[12:])
            if re.search(r"<Record type=", line):
                datadict['recordType'].append(recordtypeval[14:-1])
            else:
                datadict['recordType'].append(recordtypeval[30:-1])
            if healthdataval is None:
                datadict['val'].append("NA")
            elif re.search(r"<Record type=", line):
                datadict['val'].append(healthdataval[7:])
            else:
                datadict['val'].append(healthdataval[2:])
            if re.search(r"unit\S+", line) is not None:
                datadict['unit'].append(re.search(r"unit\S+", line).group()[len("unit")+2:-1])
            else:
                datadict['unit'].append("NA")
            count = count + 1
            # print progress hash
            if count % 10000 == 0:
                print('{counts} of {nums}'.format(counts=count, nums=num_lines))
                sys.stdout.flush()


    outputDf = pd.DataFrame.from_dict(datadict)
    return outputDf

# takes in csv outputted by sampleProcess to generate summary metrics

import pandas as pd
from datetime import datetime
import numpy as np
def returnAvg(inputDf, colname):
    pass

def returnAvgHR(inputDf, dates, log, ignoreWalking = True, ignoreRunning = True):
    hroutput =[]
    walkingmeans = {}
    runningmeans = {}
    daymeans = {}
    for date in dates:
        logSS = log.loc[log['Date'] == datetime.strptime(date, '%Y-%m-%d').date()]
        df = inputDf.loc[inputDf['endDate'].dt.date == datetime.strptime(date, '%Y-%m-%d').date()]
        walkingSS = df.loc[df['recordType'] == 'HKWorkoutActivityTypeWalking']  # subset of walking information
        runningSS = df.loc[df['recordType'] == 'HKWorkoutActivityTypeRunning']  # subset of running information
        df = df.loc[df['recordType'] == 'HKQuantityTypeIdentifierHeartRate']
        df = df.loc[df['source'] != 'Nike Run']  # ignore NikeRun

        # only take waking hours
        if logSS['Sleep'].values[0] >= datetime.strptime('12:00AM','%I:%M%p').time() and logSS['Sleep'].values[0] < datetime.strptime('3:00AM','%I:%M%p').time(): #this 3am is based on this specific log, may need to change it for your own project
            # then the sleep day is next day
            sleepTime = np.datetime64(str(logSS['Date'].values[0])[:10] + 'T' + str(logSS['Sleep'].values[0]))
            sleepTime += np.timedelta64(1, 'D') # went to bed yesterday
        else:
            sleepTime = np.datetime64(str(logSS['Date'].values[0])[:10] + 'T' + str(logSS['Sleep'].values[0]))
        wakeTime =  np.datetime64(str(logSS['Date'].values[0])[:10] + 'T' + str(logSS['Wake'].values[0]))
        df = df[(df['endDate'] > wakeTime) & (df['endDate'] < sleepTime)]
        concatseries = pd.DataFrame()
        for walkidx in range(len(walkingSS['startDate'])):
            # first calculate the average for this period
            concatseries = concatseries.append(df[(df['endDate'] > walkingSS['startDate'].iloc[walkidx]) & (df['endDate'] < walkingSS['endDate'].iloc[walkidx])])
            # exclude it from our ongoing dataframe
            df = df[(df['endDate'] < walkingSS['startDate'].iloc[walkidx]) | (df['endDate'] > walkingSS['endDate'].iloc[walkidx])]
        if len(concatseries)>0:
            walkingmeans[date] = pd.to_numeric(concatseries['val']).mean()
        concatseries = pd.DataFrame()
        for runidx in range(len(runningSS['startDate'])):
            # first calculate the average for this period
            concatseries = concatseries.append(df[(df['endDate'] > runningSS['startDate'].iloc[runidx]) & (df['endDate'] < runningSS['endDate'].iloc[runidx])])
            # exclude it from our ongoing dataframe
            df = df[(df['endDate'] < runningSS['startDate'].iloc[runidx]) | (df['endDate'] > runningSS['endDate'].iloc[runidx])]
        if len(concatseries)>0:
            runningmeans[date] = pd.to_numeric(concatseries['val']).mean()
        if len(df)>0:
            daymeans[date] = pd.to_numeric(df['val']).mean()

    return (daymeans, walkingmeans, runningmeans)


# relevant initials
id = 'MK'
conditions = ['baseline', 'wr']
output = []
for condition in conditions:
    # read log info
    log = pd.read_excel('Physiological_HR.xlsx', sheet_name='Sheet1')
    log = log.loc[log['Initials'] == id]
    log['Date'] = pd.to_datetime(log['Date'])

    # read file
    inputDf = pd.read_csv(id + '_' + condition +'_output.csv')
    inputDf['startDate'] = pd.to_datetime(inputDf['startDate'])
    inputDf['endDate'] = pd.to_datetime(inputDf['endDate'])

    baselineDates = ['2019-04-10', '2019-04-11', '2019-04-12', '2019-04-13', '2019-04-14', '2019-04-15', '2019-04-16']
    WRDates = ['2019-04-17', '2019-04-18', '2019-04-19', '2019-04-20', '2019-04-21', '2019-04-22']
    if condition == 'baseline':
        bdayhr, bwalkhr, brunhr = returnAvgHR(inputDf, baselineDates, log)
    else:
        wdayhr, wwalkhr, wrunhr = returnAvgHR(inputDf, WRDates, log)
print('done')
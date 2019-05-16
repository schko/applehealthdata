# takes in csv outputted by sampleProcess to generate summary metrics

import pandas as pd
from datetime import datetime

def returnAvg(inputDf, colname):
    pass

def returnAvgHR(inputDf, dates, log, ignoreWalking = True, ignoreRunning = True):
    hroutput =[]
    walkingmeans = {}
    runningmeans = {}
    daymeans = {}
    for date in dates:
        df = inputDf.loc[inputDf['endDate'].dt.date == datetime.strptime(date, '%Y-%m-%d').date()]
        walkingSS = df.loc[df['recordType'] == 'HKWorkoutActivityTypeWalking']  # subset of walking information
        runningSS = df.loc[df['recordType'] == 'HKWorkoutActivityTypeRunning']  # subset of running information
        logSS = log.loc[log['Date'] == datetime.strptime(date, '%Y-%m-%d').date()]
        df = df.loc[df['recordType'] == 'HKQuantityTypeIdentifierHeartRate']
        df = df.loc[df['source'] != 'Nike Run'] # ignore NikeRun
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
id = 'PA'
conditions = ['baseline', 'wr']
output = []
for condition in conditions:
    # read log info
    log = pd.read_excel('Physiological.xlsx', sheet_name='Sheet1')
    log = log.loc[log['Initials'] == id]
    log['Date'] = pd.to_datetime(log['Date'])

    # read file
    inputDf = pd.read_csv(id + '_' + condition +'_output.csv')
    inputDf['startDate'] = pd.to_datetime(inputDf['startDate'])
    inputDf['endDate'] = pd.to_datetime(inputDf['endDate'])

    baselineDates = ['2019-04-10', '2019-04-11', '2019-04-12', '2019-04-13', '2019-04-14', '2019-04-15', '2019-04-16']
    WRDates = ['2019-04-17', '2019-04-18', '2019-04-19', '2019-04-20', '2019-04-21', '2019-04-22']

    dayhr, walkhr, runhr = returnAvgHR(inputDf, baselineDates, log)
print('done')
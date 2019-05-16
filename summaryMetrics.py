# takes in csv outputted by sampleProcess to generate summary metrics

import pandas as pd
from datetime import datetime

def returnAvgHR(inputDf, date, ignoreWalking = True, ignoreRunning = True):
    pass

# ignore NikeRun

# relevant initials
id = 'MK'

# read log info
log = pd.read_excel('Physiological.xlsx', sheet_name='Sheet1')
log = log.loc[log['Initials'] == id]
log['Date'] = pd.to_datetime(log['Date'])

# read file
inputdf = pd.read_csv(id + '_baseline_output.csv')
inputdf['startDate'] = pd.to_datetime(inputdf['startDate'])
inputdf['endDate'] = pd.to_datetime(inputdf['endDate'])


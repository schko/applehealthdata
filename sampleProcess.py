# Sample process, reading in an XML file and plotting HR on a specific day

from parseXML import parseXML
import matplotlib.pyplot as plt
import traces
import pandas as pd
import numpy as np
import datetime

def hrconvert(df, dateFrom, dateTo):
    # select the variable of interest
    s = df[(df['date'] > dateFrom) & (df['date'] < dateTo)]
    s = s[s['recordType'] == 'HKQuantityTypeIdentifierHeartRate']

    # sorting just in case
    s = s.sort_values('date', ascending=True)
    s["val"] = pd.to_numeric(s["val"])

    # accounts for uneven time series
    time_series = traces.TimeSeries()
    for i in range(len(s)):
        time_series[pd.to_datetime(s['date'].iloc[i])] = s['val'].iloc[i]
    # to account for the unevenness of HR data, we use a moving average to "fill in the gaps" in HR
    regular = time_series.moving_average(60, pandas=True)
    return (regular.keys().values, regular.values) # return the x, y

# read in xml data and get dataframe
df = parseXML('export.xml')

# extract time
timeextract = lambda x: datetime.datetime.utcfromtimestamp((x - np.datetime64('1970-01-01T00:00:00Z'))
                                                           / np.timedelta64(1, 's'))

# get 03-03 data
(x1, y1) = hrconvert(df, '2019-03-03', '2019-03-04')

# plot
plt.plot(list(map(timeextract, x1)), y1)
# get 02-24 data
(x1, y1) = hrconvert(df, '2019-03-10', '2019-03-11')
# overlay plot
plt.plot(list(map(timeextract, x1)), y1)

plt.xticks(rotation='vertical')
plt.show()


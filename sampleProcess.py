# Sample process, reading in an XML file and plotting HR on a specific day

from parseXML import parseXML
import matplotlib.pyplot as plt
import traces
import pandas as pd
import numpy as np
import datetime
import tensorflow

def hrconvert(df, dateFrom, dateTo):
    # select the variable of interest
    s = df[(df['endDate'] > dateFrom) & (df['endDate'] < dateTo)]
    if dateFrom == '2019-04-21':
        s.to_csv("output.csv")
    s = s[s['recordType'] == 'HKQuantityTypeIdentifierHeartRate']

    # sorting just in case
    s = s.sort_values('endDate', ascending=True)
    s["val"] = pd.to_numeric(s["val"])

    # accounts for uneven time series
    time_series = traces.TimeSeries()
    for i in range(len(s)):
        time_series[pd.to_datetime(s['endDate'].iloc[i])] = s['val'].iloc[i]
    # to account for the unevenness of HR data, we use a moving average to "fill in the gaps" in HR
    regular = time_series.moving_average(60, pandas=True)
    print(np.mean(regular.values[int(25200/60):]))
    return (regular.keys().values[int(25200/60):], regular.values[int(25200/60):]) # return the x, y

def plotPoints(x1, y1, axis, fillX = 0):
    # plot
    convertedTime = list(map(timeextract, x1))
    axis.plot(convertedTime, y1)


# read in xml data and get dataframe
df = parseXML('export.xml')

# extract time
timeextract = lambda x: datetime.datetime.utcfromtimestamp((x - np.datetime64('1970-01-01T00:00:00Z'))
                                                           / np.timedelta64(1, 's')).hour * 3600 + datetime.datetime.utcfromtimestamp((x - np.datetime64('1970-01-01T00:00:00Z'))
                                                           / np.timedelta64(1, 's')).minute * 60 + datetime.datetime.utcfromtimestamp((x - np.datetime64('1970-01-01T00:00:00Z'))
                                                           / np.timedelta64(1, 's')).second


fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, sharex=True)
# get 03-03 data
print('2019-04-10')
(x1, y1) = hrconvert(df, '2019-04-10', '2019-04-11')
plotPoints(x1, y1, ax1, 60000)
(x1, y1) = hrconvert(df, '2019-04-17', '2019-04-18')
plotPoints(x1, y1, ax1, 60000)

print('2019-04-11')
(x1, y1) = hrconvert(df, '2019-04-11', '2019-04-12')
plotPoints(x1, y1, ax2, 60000)
(x1, y1) = hrconvert(df, '2019-04-18', '2019-04-19')
plotPoints(x1, y1, ax2, 60000)

# get 03-03 data
print('2019-04-12')
(x1, y1) = hrconvert(df, '2019-04-12', '2019-04-13')
plotPoints(x1, y1, ax3, 60000)
(x1, y1) = hrconvert(df, '2019-04-19', '2019-04-20')
plotPoints(x1, y1, ax3, 60000)

plt.xticks(rotation='vertical')

print('2019-04-13')
(x1, y1) = hrconvert(df, '2019-04-13', '2019-04-14')
plotPoints(x1, y1, ax4, 60000)
(x1, y1) = hrconvert(df, '2019-04-20', '2019-04-21')
plotPoints(x1, y1, ax4, 60000)

# get 03-03 data
print('2019-04-14')
(x1, y1) = hrconvert(df, '2019-04-14', '2019-04-15')
plotPoints(x1, y1, ax5, 60000)
(x1, y1) = hrconvert(df, '2019-04-21', '2019-04-22')
plotPoints(x1, y1, ax5, 60000)

plt.xticks(rotation='vertical')
plt.show()
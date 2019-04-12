# Sample process, reading in an XML file and plotting HR on a specific day

from parseXML import parseXML
import matplotlib.pyplot as plt
import traces
import pandas as pd

# read in xml data and get dataframe
df = parseXML('export.xml')

# select the variable of interest
s = df[(df['date'] > '2019-02-02') & (df['date'] < '2019-02-03')]
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
regular.keys()
# plot
plt.plot(regular.keys().values, regular.values)
plt.xticks(rotation='vertical')
plt.xlim(s['date'].iloc[0], s['date'].iloc[len(s)-1])
plt.show()

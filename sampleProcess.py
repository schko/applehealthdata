# Sample process, reading in an XML file and plotting HR on a specific day

from parseXML import parseXML
import matplotlib.pyplot as plt
import pandas as pd

# read in xml data and get dataframe
df = parseXML('export.xml')

# select the variable of interest
s = df[(df['date'] > '2019-01-14') & (df['date'] < '2019-01-15')]
s = s[s['recordType']=='KQuantityTypeIdentifierHeartRate']
# sorting just in case
s = s.sort_values('date', ascending=True)
s["val"] = pd.to_numeric(s["val"])
plt.plot(s['date'], s['val'])
plt.xticks(rotation='vertical')
plt.show()
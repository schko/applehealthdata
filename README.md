# Analyzer for Apple's Health Data
Simple tools to read and analyze Apple HealthKit Exports (XML). This was created to handle relevant data for Function's White Rose video. 

1. parseXML.py includes a function that reads in an XML file and outputs a Pandas dataframe 
2. sampleProcess.py processes an XML and outputs a simple plot of heart rate data collected from the Apple Watch on a certain day. 

Note: Because of uneven time series (i.e. sampling time is uneven and based more on activity for HR measures), sampleProcess applies a moving average to smooth gaps without HR data. Similar techniques would need to be completed for other data points (e.g. accelorometry) and will be added in a future version. 

Python version 3.6

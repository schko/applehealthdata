# Sample process, reading in an XML file and plotting HR on a specific day, and outputs the csv in the format required for
# day to day summary metrics

from parseXML import parseXML
import matplotlib.pyplot as plt
import traces
import pandas as pd
import numpy as np
import datetime

def hrconvert(df, dateFrom, dateTo):
    # select the variable of interest
    s = df[(df['endDate'] > dateFrom) & (df['endDate'] < dateTo)]
    sortedDf = s
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
    return (regular.keys().values[int(25200/60):], regular.values[int(25200/60):], sortedDf) # return the x, y

def plotPoints(x1, y1, axis, timeextract):
    # plot
    convertedTime = list(map(timeextract, x1))
    axis.plot(convertedTime, y1)

def whiteRoseOutputs(xmlFile):
    # read in xml data and get dataframe
    df = parseXML(xmlFile)

    # extract time
    timeextract = lambda x: datetime.datetime.utcfromtimestamp((x - np.datetime64('1970-01-01T00:00:00Z'))
                                                               / np.timedelta64(1, 's')).hour * 3600 + datetime.datetime.utcfromtimestamp((x - np.datetime64('1970-01-01T00:00:00Z'))
                                                               / np.timedelta64(1, 's')).minute * 60 + datetime.datetime.utcfromtimestamp((x - np.datetime64('1970-01-01T00:00:00Z'))
                                                               / np.timedelta64(1, 's')).second


    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, sharex=True)
    baselinecsv = pd.DataFrame()
    wrcsv = pd.DataFrame()
    # get 03-03 data
    print('2019-04-10')
    (x1, y1, dfout) = hrconvert(df, '2019-04-10', '2019-04-11')
    baselinecsv = baselinecsv.append(dfout)

    plotPoints(x1, y1, ax1, timeextract)
    (x1, y1, dfout) = hrconvert(df, '2019-04-17', '2019-04-18')
    plotPoints(x1, y1, ax1, timeextract)
    wrcsv = wrcsv.append(dfout)

    print('2019-04-11')
    (x1, y1, dfout) = hrconvert(df, '2019-04-11', '2019-04-12')
    baselinecsv = baselinecsv.append(dfout)

    plotPoints(x1, y1, ax2, timeextract)
    (x1, y1, dfout) = hrconvert(df, '2019-04-18', '2019-04-19')
    plotPoints(x1, y1, ax2, timeextract)
    wrcsv = wrcsv.append(dfout)

    # get 03-03 data
    print('2019-04-12')
    (x1, y1, dfout) = hrconvert(df, '2019-04-12', '2019-04-13')
    baselinecsv = baselinecsv.append(dfout)

    plotPoints(x1, y1, ax3, timeextract)
    (x1, y1, dfout) = hrconvert(df, '2019-04-19', '2019-04-20')
    plotPoints(x1, y1, ax3, timeextract)
    wrcsv = wrcsv.append(dfout)

    plt.xticks(rotation='vertical')

    print('2019-04-13')
    (x1, y1, dfout) = hrconvert(df, '2019-04-13', '2019-04-14')
    baselinecsv = baselinecsv.append(dfout)

    plotPoints(x1, y1, ax4, timeextract)
    (x1, y1, dfout) = hrconvert(df, '2019-04-20', '2019-04-21')
    plotPoints(x1, y1, ax4, timeextract)
    wrcsv = wrcsv.append(dfout)

    # get 03-03 data
    print('2019-04-14')
    (x1, y1, dfout) = hrconvert(df, '2019-04-14', '2019-04-15')
    baselinecsv = baselinecsv.append(dfout)

    plotPoints(x1, y1, ax5, timeextract)
    (x1, y1, dfout) = hrconvert(df, '2019-04-21', '2019-04-22')
    plotPoints(x1, y1, ax5, timeextract)
    wrcsv = wrcsv.append(dfout)


    print('2019-04-15')
    (x1, y1, dfout) = hrconvert(df, '2019-04-15', '2019-04-16')
    baselinecsv = baselinecsv.append(dfout)

    plotPoints(x1, y1, ax5, timeextract)
    (x1, y1, dfout) = hrconvert(df, '2019-04-22', '2019-04-23')
    plotPoints(x1, y1, ax5, timeextract)
    wrcsv = wrcsv.append(dfout)

    print('2019-04-15')
    (x1, y1, dfout) = hrconvert(df, '2019-04-16', '2019-04-17')
    baselinecsv = baselinecsv.append(dfout)

    plotPoints(x1, y1, ax5, timeextract)
    (x1, y1, dfout) = hrconvert(df, '2019-04-23', '2019-04-24')
    plotPoints(x1, y1, ax5, timeextract)
    wrcsv = wrcsv.append(dfout)

    #baselinecsv.to_csv("baseline_output.csv", index=False)
    #wrcsv.to_csv("wr_output.csv", index=False)
    plt.xticks(rotation='vertical')
    plt.show()

#whiteRoseOutputs('PA export 042619.xml')
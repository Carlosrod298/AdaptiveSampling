
# Current  graphics


from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import pandas as pd
import pylab as pl
import numpy as np
from matplotlib.dates import DateFormatter
#%matplotlib inline
import time
import datetime



# Ble
AdvertisingBleCurrent = 10000 #uA
TimeAdvertising = 10 #ms
SensorCallBleCurrent = 18000 #uA
SleepBleCurrent = 53.7        #uA
AverageAdverCurrent = 100 #uA
Fsampling = np.arange(1,181)*10
SensorAverage = 18*18/Fsampling
SleepTimeBle =  990*Fsampling -18
SleepAverAgeCurrentBLE = (SleepBleCurrent*SleepTimeBle)/(Fsampling*1000)
TotalCurrentBLE = AverageAdverCurrent + SensorAverage + SleepAverAgeCurrentBLE
MinutesSampling = Fsampling/60

MinutesPandas = pd.to_datetime(Fsampling, unit='s')
print("time: ")
print(MinutesPandas.values)
print("F Samplin")
print(Fsampling)
# Zigbee
SleepZigbeeCurrent = 20 #uA
AverageSmCurrent = 39   #mA
TxZigbeeCurrent = 25*13/Fsampling
RxZigbeeCurrent = 27*20.6/Fsampling
SleepTimeZigbee =  998.7*Fsampling -33.6
SleepAverAgeCurrentZb = (SleepZigbeeCurrent*SleepTimeZigbee)/(Fsampling*1000)
TotalCurrentZigbee = AverageSmCurrent + TxZigbeeCurrent + RxZigbeeCurrent + SleepAverAgeCurrentZb



# BLE logger
SleepLoggerCurrent = 20
AverageSmCurrent = 39
SaveFlashCurrent = (27*15)/Fsampling
SleepTimeLogger =  998.7*Fsampling - 15
SleepAverAgeCurrentLogger = (SleepLoggerCurrent*SleepTimeLogger)/(Fsampling*1000)
TotalCurrentLogger = AverageSmCurrent + SaveFlashCurrent +  SleepAverAgeCurrentLogger


model = np.polyfit( Fsampling, TotalCurrentZigbee ,  15)
print (model)
Predic = np.poly1d(model)
PredicValues = Predic(Fsampling)
print(Fsampling)
print(PredicValues)

# curve params
from sklearn.metrics import r2_score
scorePred = r2_score(TotalCurrentZigbee, PredicValues)*100
print("Train set Accuracy: ", scorePred)

# Visualizing the Linear Regression results
fig1, ax1 = plt.subplots()
plt.scatter(MinutesSampling, TotalCurrentZigbee, color='red',label='Current Comsuption')
plt.plot(MinutesSampling,PredicValues , color='blue',label='Predicted Curve Accuracy %2.2f %%'%scorePred)
ax1.xaxis.set_major_locator(plt.MaxNLocator(41))
plt.gcf().autofmt_xdate()
#date_form = DateFormatter("%M-%S")
#ax1.xaxis.set_major_formatter(date_form)
plt.title('Current Comsuption Analisys')
plt.xlabel('Sampling Period (Minutes)')
plt.ylabel('Current Comsuption (mA)')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()




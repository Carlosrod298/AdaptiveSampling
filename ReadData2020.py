#Import Data on Json intel
#Intel: http://76.74.150.54:8092/ws_iot-agro/GetIntel/?anio=2020&mes=9&dia=12
#Libelium: http://76.74.150.54:8092/ws_iot-agro/GetLibelium/?anio=2020&mes=6&dia=4
#Omicron http://76.74.150.54:8092/ws_iot-agro/GetOmicron/?anio=2020&mes=6&dia=4




from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
from matplotlib.dates import HourLocator
import pylab as pl
import numpy as np
#%matplotlib inline
import time
import datetime



df = pd.read_json ('August12.json')
print(df.shape)
print(df.describe())
cdf = df[['fecha','ID','HAM','HSU','LUZ','BAT']]
timeDataSet = {}
# Convert field fechaDato to date time
timeDataSet['NewDateTime'] = pd.to_datetime(cdf['fecha'], format='%Y-%m-%d %H:%M:%S')
cdf.index = timeDataSet['NewDateTime']
cdf.index = cdf.index - pd.Timedelta('05:00:00') #Set Timezone


Intel4 = cdf.loc[cdf['ID']=='IN_01_T_004']
Intel5 = cdf.loc[cdf['ID']=='IN_01_T_005']
Intel6 = cdf.loc[cdf['ID']=='IN_01_T_006']
Intel4 = Intel4.drop(columns=['ID','fecha',])
Intel5 = Intel5.drop(columns=['ID','fecha',])
Intel6 = Intel6.drop(columns=['ID','fecha',])
print(Intel4.head(4))
DateBase = Intel4.index[0]

#Diff Time
column_names = ["DiffTime"]
print("Index 0: ")
TimeDiffe4 = []
for i in range(1,Intel4.index.size):
    TimeDiffe4.append( Intel4.index[i])
Intel4 = Intel4.drop(Intel4.index[len(Intel4)-1])
Intel4['EndDate'] = TimeDiffe4
Intel4['DiffTime'] = Intel4['EndDate'] - Intel4.index
print(Intel4.head(5))

TimeDiffe5 = []
for i in range(1,Intel5.index.size):
    TimeDiffe5.append( Intel5.index[i])
Intel5 = Intel5.drop(Intel5.index[len(Intel5)-1])
Intel5['EndDate'] = TimeDiffe5
Intel5['DiffTime'] = Intel5['EndDate'] - Intel5.index
print(Intel5.head(5))

TimeDiffe6 = []
for i in range(1,Intel6.index.size):
    TimeDiffe6.append( Intel6.index[i])
Intel6 = Intel6.drop(Intel6.index[len(Intel6)-1])
Intel6['EndDate'] = TimeDiffe6
Intel6['DiffTime'] = Intel6['EndDate'] - Intel6.index
print(Intel6.head(5))

#NormalST =  pd.DataFrame(data=TimeDiffe4,columns= column_names)
#AdaptativeEmbebed = pd.DataFrame(data=TimeDiffe5,columns= column_names)
#AdaptativeGW = pd.DataFrame(data=TimeDiffe6,columns= column_names)
#print(AdaptativeEmbebed.head(5))

#Normal Data
fig1, ax1 = plt.subplots()
plt.xlabel("Day " + DateBase.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel("Celsius")
plt.plot(Intel4.index, Intel4.HAM, color='red',label='Temperature minuntes ')
plt.plot(Intel6.index, Intel6.HAM, color='blue', label='T° AdaptableTime')
plt.plot(Intel5.index, Intel5.HAM, color='green', label='T° Adaptable Embebed')
ax1.xaxis.set_major_locator(plt.MaxNLocator(22))
plt.gcf().autofmt_xdate()
date_form = DateFormatter("%H-%M")
ax1.xaxis.set_major_formatter(date_form)
plt.legend(loc='upper right')
plt.grid(True)
plt.gcf().autofmt_xdate()
plt.legend(loc='upper right')
fig1.show()



#Normal Data

fig3, ax3 = plt.subplots()
plt.xlabel("Index " + DateBase.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel("Seconds")
plt.plot(Intel4.index, Intel4['DiffTime'].dt.total_seconds(), color='red',label='Sampling minuntes ')
plt.plot(Intel5.index, Intel5['DiffTime'].dt.total_seconds(), color='blue', label='T° AdaptableTime Embebed')
plt.plot(Intel6.index, Intel6['DiffTime'].dt.total_seconds(), color='green', label='T° Adaptable ')
ax3.xaxis.set_major_locator(plt.MaxNLocator(22))
plt.gcf().autofmt_xdate()
ax3.xaxis.set_major_formatter(date_form)
plt.legend(loc='upper right')
plt.grid(True)
plt.gcf().autofmt_xdate()
plt.legend(loc='upper right')
fig3.show()


#Normal Data
fig2, ax2 = plt.subplots()
plt.xlabel("Time")
plt.ylabel("%RH")
plt.plot(Intel4.index, Intel4.HSU, color='red',label='Humidity minuntes ')
plt.plot(Intel6.index, Intel6.HSU, color='blue', label='Humidity AdaptableTime')
plt.plot(Intel5.index, Intel5.HSU, color='green', label='Humidity Adaptable Embebed')
plt.gcf().autofmt_xdate()
ax2.xaxis.set_major_formatter(date_form)
ax2.xaxis.set_major_locator(plt.MaxNLocator(22))
plt.legend(loc='upper right')
plt.grid(True)
plt.gcf().autofmt_xdate()
plt.legend(loc='upper right')
plt.show()

Intel4.to_csv('Intel4.csv',float_format='%.2f',index=True) # rounded to two decimals
Intel5.to_csv('Intel5.csv',float_format='%.2f',index=True) # rounded to two decimals
Intel6.to_csv('Intel6.csv',float_format='%.2f',index=True) # rounded to two decimals
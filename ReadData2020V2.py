#Import Data on Json intel
#Intel: http://76.74.150.54:8092/ws_iot-agro/GetIntel/?anio=2020&mes=11&dia=08
#Libelium: http://76.74.150.54:8092/ws_iot-agro/GetLibelium/?anio=2020&mes=6&dia=4
#Omicron http://76.74.150.54:8092/ws_iot-agro/GetOmicron/?anio=2020&mes=6&dia=4




from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
from MasterTesis import CCFun

from matplotlib.dates import HourLocator
import pylab as pl
import numpy as np
#%matplotlib inline
import time
import datetime



df = pd.read_json ('November07.json')
print(df.shape)
print(df.describe())
cdf = df[['fecha','ID','TAM','HAM','LUZ','BAT']]
timeDataSet = {}
# Convert field fechaDato to date time
timeDataSet['NewDateTime'] = pd.to_datetime(cdf['fecha'], format='%Y-%m-%d %H:%M:%S')
cdf.index = timeDataSet['NewDateTime']
cdf.index = cdf.index - pd.Timedelta('05:00:00') #Set Timezone


Intel1 = cdf.loc[cdf['ID'] == 'IN_01_T_001']
Intel2 = cdf.loc[cdf['ID'] == 'IN_01_T_002']
Intel3 = cdf.loc[cdf['ID'] == 'IN_01_T_003']
Intel4 = cdf.loc[cdf['ID'] == 'IN_01_T_004']
Intel1 = Intel1.drop(columns=['ID', 'fecha', ])
Intel2 = Intel2.drop(columns=['ID', 'fecha', ])
Intel3 = Intel3.drop(columns=['ID', 'fecha', ])
Intel4 = Intel4.drop(columns=['ID', 'fecha', ])

daySelected = 11
stringDay = '2020-11-'+str(daySelected).zfill(2)+' '
daySelected2 = daySelected+1
stringDay2 = '2020-11-'+str(daySelected2).zfill(2)+' '
Intel1  = Intel1.loc[stringDay+'00:00': stringDay2+'00:00']
Intel2  = Intel2.loc[stringDay+'00:00': stringDay2+'00:19']
Intel3  = Intel3.loc[stringDay+'00:00': stringDay2+'00:19']
Intel4  = Intel4.loc[stringDay+'00:00': stringDay2+'00:19']
print(Intel1.head(4))
DateBase = Intel1.index[0]

#Diff Time
column_names = ["DiffTime"]
print("Index 0: ")
TimeDiffe1 = []
for i in range(1, Intel1.index.size):
    TimeDiffe1.append(Intel1.index[i])
Intel1 = Intel1.drop(Intel1.index[len(Intel1) - 1])
Intel1['EndDate'] = TimeDiffe1
Intel1['DiffTime'] = Intel1['EndDate'] - Intel1.index
print(Intel1.head(5))

TimeDiffe2 = []
for i in range(1, Intel2.index.size):
    TimeDiffe2.append(Intel2.index[i])
Intel2 = Intel2.drop(Intel2.index[len(Intel2) - 1])
Intel2['EndDate'] = TimeDiffe2
Intel2['DiffTime'] = Intel2['EndDate'] - Intel2.index
print(Intel2.head(5))

TimeDiffe3 = []
for i in range(1, Intel3.index.size):
    TimeDiffe3.append(Intel3.index[i])
Intel3 = Intel3.drop(Intel3.index[len(Intel3) - 1])
Intel3['EndDate'] = TimeDiffe3
Intel3['DiffTime'] = Intel3['EndDate'] - Intel3.index
print(Intel3.head(5))


TimeDiffe4 = []
for i in range(1, Intel4.index.size):
    TimeDiffe4.append(Intel4.index[i])
Intel4 = Intel4.drop(Intel4.index[len(Intel4) - 1])
Intel4['EndDate'] = TimeDiffe4
Intel4['DiffTime'] = Intel4['EndDate'] - Intel4.index
print(Intel4.head(5))

#Intel2.HAM = Intel2.HAM
#NormalST =  pd.DataFrame(data=TimeDiffe4,columns= column_names)
#AdaptativeEmbebed = pd.DataFrame(data=TimeDiffe5,columns= column_names)
#AdaptativeGW = pd.DataFrame(data=TimeDiffe6,columns= column_names)
#print(AdaptativeEmbebed.head(5))

Intel1Av = Intel1.resample('1800S').mean()
Intel2Av = Intel3.resample('1800S').mean()
Intel3.to_csv("./Intel2Av.csv", sep=',',index=True)
Intel1.to_csv("./Intel1Av.csv", sep=',',index=True)
print(Intel1.sum())
print(Intel3.sum())
print(Intel2Av.shape)
TimeString30M = [date_obj.strftime('%H:%M:%S') for date_obj in Intel1Av.index]
print(TimeString30M)
df = pd.DataFrame(data={ "Time": TimeString30M,"Intel1T":Intel1Av['TAM'],"Intel1H":Intel1Av['HAM']})
df.to_csv("./AveragesIntel1_30M.csv", sep=',',index=False)
TimeString30M = [date_obj.strftime('%H:%M:%S') for date_obj in Intel2Av.index]
print(TimeString30M)
df = pd.DataFrame(data={ "Time": TimeString30M,"Intel1T":Intel2Av['TAM'],"Intel1H":Intel2Av['HAM']})
df.to_csv("./AveragesIntel2_30M.csv", sep=',',index=False)

import numpy as np
#TimeDife = Intel4['DiffTime'].dt.total_seconds.astype('int16')
TimeDife = pd.to_numeric(Intel2['DiffTime'].dt.seconds, downcast='integer')
MinuteVal = [round(value/60) for value in TimeDife.values]
print("tiempo en int ")
print(MinuteVal)
#Consumptionvector = [(CCFun.Compsuption(x)) for x in Psampling]



#Normal Data
plt.rcParams.update({'font.size': 16})

fig1,ax1 = plt.subplots(figsize=(20, 10))
plt.xlabel("Day " + DateBase.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel("Celsius")
plt.plot(Intel1.index, Intel1.TAM, color='red', label='Temperature per minunte ')
plt.plot(Intel2.index, Intel2.TAM, color='blue', label='Adaptable Time 1')
plt.plot(Intel3.index, Intel3.TAM, color='green', label='Adaptable Time 2')
plt.plot(Intel4.index, Intel4.TAM, color='black', label='Adaptable Time 3')
ax1.set_ylim(10, 40)
ax1.xaxis.set_major_locator(plt.MaxNLocator(22))
plt.gcf().autofmt_xdate()
date_form = DateFormatter("%H:%M")
ax1.xaxis.set_major_formatter(date_form)
plt.legend(loc='upper right')
plt.title('Temperature Curve')
plt.grid(True)
plt.gcf().autofmt_xdate()
plt.legend(loc='upper right')
#fig1.savefig("images/ResultTemp.png")
#fig1.show()

#Normal Data
fig2, ax2 = plt.subplots(figsize=(20, 10))
plt.xlabel("Index " + DateBase.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel("%RH")
plt.plot(Intel1.index, Intel1.HAM, color='red',     label='Humidity minuntes ')
plt.plot(Intel2.index, Intel2.HAM, color='blue',    label='Humidity Adaptable 1')
plt.plot(Intel3.index, Intel3.HAM, color='green',   label='Humidity Adaptable 2')
plt.plot(Intel4.index, Intel4.HAM, color='black',   label='Humidity Adaptable 3')
ax2.set_ylim(20, 100)
plt.gcf().autofmt_xdate()
ax2.xaxis.set_major_formatter(date_form)
ax2.xaxis.set_major_locator(plt.MaxNLocator(22))
plt.legend(loc='upper right')
plt.title('Humidity Curve')
plt.grid(True)
plt.gcf().autofmt_xdate()
plt.legend(loc='upper right')
#fig2.savefig("images/ResultHume.png")
fig2.show()

#Normal Data

fig3, ax3 = plt.subplots(figsize=(20, 10))
plt.xlabel("Time " + DateBase.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel("Sampling time (Minutes)")
plt.plot(Intel2.index, (Intel2['DiffTime'].dt.total_seconds()) / 60, color='blue',   label='Adaptable Time 1')
plt.plot(Intel3.index, (Intel3['DiffTime'].dt.total_seconds()) / 60, color='green',  label='Adaptable Time 2')
plt.plot(Intel4.index, (Intel4['DiffTime'].dt.total_seconds()) / 60, color='black', label='Adaptable Time 3')
ax3.xaxis.set_major_locator(plt.MaxNLocator(22))
plt.gcf().autofmt_xdate()
ax3.xaxis.set_major_formatter(date_form)
plt.legend(loc='upper right')
plt.title('Fixed time vs Adaptable Time')
plt.grid(True)
plt.gcf().autofmt_xdate()
plt.legend(loc='upper right')
#fig3.savefig("images/AdaptableTime.png")
plt.show()




#Intel4.to_csv('Intel4.csv',float_format='%.2f',index=True) # rounded to two decimals
#Intel5.to_csv('Intel5.csv',float_format='%.2f',index=True) # rounded to two decimals
#Intel6.to_csv('Intel6.csv',float_format='%.2f',index=True) # rounded to two decimals
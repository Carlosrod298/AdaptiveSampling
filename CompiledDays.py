from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import pandas as pd
import hydroeval as he
from matplotlib.dates import DateFormatter
from sklearn.metrics import mean_squared_error
from MasterTesis import CCFun

from matplotlib.dates import HourLocator
import pylab as pl
import numpy as np
#%matplotlib inline
import time
import datetime



df = pd.read_json ('November12.json')
print(df.shape)
print(df.describe())
cdf = df[['fecha','ID','TAM','HAM']]
timeDataSet = {}
# Convert field fechaDato to date time
timeDataSet['NewDateTime'] = pd.to_datetime(cdf['fecha'], format='%Y-%m-%d %H:%M:%S')
cdf.index = timeDataSet['NewDateTime'] - pd.Timedelta('05:00:00') #Set Timezone
#cdf['Time2'] = timeDataSet['NewDateTime'] - pd.Timedelta('05:00:00')
cdf = cdf.fillna(method ='bfill')
#Select Days
Intel1 = cdf.loc[cdf['ID'] == 'IN_01_T_001']
Intel2 = cdf.loc[cdf['ID'] == 'IN_01_T_003']
Intel1 = Intel1.drop(columns=['ID','fecha' ])
Intel2 = Intel2.drop(columns=['ID','fecha' ])

DaysHours = list()
for x in range(4,14):
    stringDay = '2020-11-' + str(x).zfill(2) + ' 00:00:00'
    DaysHours.append(stringDay)
date2Save = pd.to_datetime(DaysHours, format='%Y-%m-%d %H:%M:%S')

daySelected = 14
stringDay = '2020-11-'+str(daySelected).zfill(2)+' 00:00:00'
Intel1  = Intel1.loc[stringDay: ]
Intel2  = Intel2.loc[stringDay: ]


daySelected = 18
stringDay =  '2020-11-'+str(daySelected).zfill(2)+' 00:00:00'
daySelected2 = 22
stringDay2 = '2020-11-'+str(daySelected2).zfill(2)+' 00:00:00'

# delete Data
Intel1_1  = Intel1.loc[stringDay: ]
Intel2_2  = Intel2.loc[stringDay: ]

# Select Data
Intel11  = Intel1.loc[stringDay2: ]
Intel22  = Intel2.loc[stringDay2: ]
Intel11.index = Intel11.index -  pd.Timedelta('96:00:00')
Intel22.index = Intel22.index -  pd.Timedelta('96:00:00')
daySelected3 = 25
stringDay3 = '2020-11-'+str(daySelected3).zfill(2)+' 23:00:00'
Intel1_4  = Intel11.loc[stringDay3: ]
Intel2_4  = Intel22.loc[stringDay3: ]
Intel11 = Intel11.drop(Intel1_4.index)
Intel22 = Intel22.drop(Intel2_4.index)

Intel1 = Intel1.drop(Intel1_1.index)
Intel2 = Intel2.drop(Intel2_2.index)
Intel1 = pd.concat([Intel1, Intel11]) #
Intel2 = pd.concat([Intel2, Intel22]) #


Intel1.index = Intel1.index -  pd.Timedelta('240:00:00')
Intel2.index = Intel2.index -  pd.Timedelta('240:00:00')
daySelected2 = 22
stringDay2 = '2020-11-'+str(daySelected2).zfill(2)+' 00:00:00'
DateBase = Intel1.index[0]



stringDay = '2020-11-'+str(daySelected).zfill(2)+' 00:00:00'
Intel1  = Intel1.loc['2020-11-04 01:00':'2020-11-12 14:00' ]




fig0,ax0 = plt.subplots(figsize=(20, 10))
plt.plot(Intel1.index, Intel1.TAM, color='red', label='Temperature per minunte ')
plt.plot(Intel2.index, Intel2.TAM, color='blue', label='Adaptable Time 1')
plt.title('Humidity Curve at Different Sampling Period')
plt.grid(True)
plt.show()



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

#Intel2.HAM = Intel2.HAM - 3.5
Intel2.HAM = Intel2.HAM - 2.39
#Normal Data




from scipy.interpolate import interp1d
TimeSeconds = [time.mktime(t.timetuple()) for t in Intel2.index]
#print(TimeSeconds)
TempFunction = interp1d(TimeSeconds, Intel2.TAM )
HumeFunction = interp1d(TimeSeconds, Intel2.HAM )
TimeSeconds1 = [time.mktime(t.timetuple()) for t in Intel1.index]
#print(TimeSeconds1)
TempeValues = TempFunction(TimeSeconds1)
#print(TempeValues)
HumeValues  = HumeFunction(TimeSeconds1)
#print(HumeValues)
errorTAM = mean_squared_error(Intel1.TAM, TempeValues)
errorHAM = mean_squared_error(Intel1.HAM, HumeValues)
dfm = pd.DataFrame({'tempe':TempeValues,'humi':HumeValues})
dfm.index = Intel1.index
corrTAM = Intel1.TAM.corr(dfm.tempe)
corrHAM = Intel1.HAM.corr(dfm.humi)
RealValuesT = Intel1.TAM.to_numpy()
RealValuesH = Intel1.HAM.to_numpy()
nseTAM = he.nse(TempeValues,RealValuesT)
nseHAM = he.nse(HumeValues,RealValuesH)
#Mean Absolute Relative Error
mareT = he.mare(TempeValues,RealValuesT)
mareH = he.mare(HumeValues,RealValuesH)
MBET = np.mean(TempeValues-RealValuesT) #here we calculate MBE
MBEH = np.mean(HumeValues-RealValuesH) #here we calculate MBE

TimeDife = pd.to_numeric(Intel2['DiffTime'].dt.seconds, downcast='integer')
MinuteVal = [round(value/60) for value in TimeDife.values]
sumValue = 0
for x in MinuteVal:
    powerComs = CCFun.Compsuption(x) * x
    sumValue = sumValue + powerComs

print("tiempo en int (hours)")
print(sum(MinuteVal)/60)
print("Error temp  ")
print(errorTAM)
print("Error Hume  ")
print(errorHAM)
print("Corr temp ")
print(corrTAM)
print("Corr Hume ")
print(corrHAM)
print("Comsuption ")
print(sumValue)
print("NseValsT ")
print(nseTAM)
print("NseValsH ")
print(nseHAM)
print("mares T")
print(mareT)
print("mares H")
print(mareH)





plt.rcParams.update({'font.size': 16})


fig1,ax1 = plt.subplots(3,figsize=(20, 10))
plt.xlabel("Days " + " ")
ax1[0].plot(Intel1.index, Intel1.TAM, color='red', label='Temperature per minunte ')
ax1[0].plot(Intel2.index, Intel2.TAM, color='blue', label='Adaptive Temperature')
ax1[0].vlines(date2Save, 0, 50, colors='k', linestyles='solid')
ax1[0].set( ylabel='Temperature °c', ylim= [15, 40])
ax1[0].legend(loc='upper right')
fig1.suptitle('Temperature')
ax1[0].grid(True)

ax1[1].plot(Intel1.index, Intel1.HAM, color='red',     label='Humidity per minuntes ')
ax1[1].plot(Intel2.index, Intel2.HAM, color='blue',    label='Adaptive Humidity ')
ax1[1].vlines(date2Save, 50, 102, colors='k', linestyles='solid')
ax1[1].set( ylabel='Humidity %RH',ylim= [50, 120])
ax1[1].legend(loc='upper right')
ax1[1].grid(True)
#ax1[2].plot(Intel1.index, Intel1.HAM, color='red',     label='Humidity per minuntes ')
ax1[2].plot(Intel2.index,Intel2['DiffTime'].dt.total_seconds() / 60, color='blue',    label='Adaptive Time ')
ax1[2].vlines(date2Save, 50, 102, colors='k', linestyles='solid')
ax1[2].set( ylabel='Minutes',ylim= [0, 70])
ax1[2].grid(True)
plt.gcf().autofmt_xdate()
date_form = DateFormatter("%d")
ax1[1].xaxis.set_major_formatter(date_form)
plt.legend(loc='upper right')
plt.title('Humidity ')
plt.grid(True)
fig1.savefig("images/AllDays.eps")
plt.show()


'''
fig1,ax1 = plt.subplots(figsize=(20, 10))
plt.xlabel("Days  ")
plt.ylabel("Celsius")
plt.plot(Intel1.index, Intel1.TAM, color='red', label='Temperature per minunte ')
plt.plot(Intel2.index, Intel2.TAM, color='blue', label='Adaptive Time')
#ax1.xaxis.set_major_locator(plt.MaxNLocator(22))
ax1.set_ylim(10, 35)
plt.gcf().autofmt_xdate()
date_form = DateFormatter("%d %H")
#ax1.xaxis.set_major_formatter(date_form)
ax1.vlines(date2Save, 0, 50, colors='k', linestyles='solid')
plt.legend(loc='upper right')
plt.title('Temperature Curve')
plt.grid(True)
plt.gcf().autofmt_xdate()
plt.legend(loc='upper right')
fig1.savefig("images/AllTempDays.png")
fig1.show()

#Normal Data
fig2, ax2 = plt.subplots(figsize=(20, 10))
plt.xlabel("Days ")
plt.ylabel("%RH")
plt.plot(Intel1.index, Intel1.HAM, color='red',     label='Humidity per minuntes ')
plt.plot(Intel2.index, Intel2.HAM, color='blue',    label='Adaptive Time ')
ax2.vlines(date2Save, 50, 102, colors='k', linestyles='solid')
plt.gcf().autofmt_xdate()
#ax2.xaxis.set_major_formatter(date_form)
#ax2.xaxis.set_major_locator(plt.MaxNLocator(22))
ax2.set_ylim(50, 102)
plt.legend(loc='upper right')
plt.title('Humidity Curve')
plt.grid(True)
plt.legend(loc='upper right')
fig2.savefig("images/AllHumeDays.png")
fig2.show()

#Normal Data
fig3, ax3 = plt.subplots(figsize=(20, 10))
plt.xlabel("Days")
plt.ylabel("Sampling time (Minutes)")
#plt.plot(Intel1.index, (Intel1['DiffTime'].dt.total_seconds()) / 60, color='red',   label='One Minute')
plt.plot(Intel2.index, (Intel2['DiffTime'].dt.total_seconds()) / 60, color='blue')
ax3.xaxis.set_major_locator(plt.MaxNLocator(22))
plt.gcf().autofmt_xdate()
ax3.xaxis.set_major_formatter(date_form)
ax3.vlines(date2Save, 0, 80, colors='k', linestyles='solid')
plt.legend(loc='upper right')
plt.title('Adaptative Time')
plt.grid(True)
plt.gcf().autofmt_xdate()
fig3.savefig("images/AllTimeDays.png")
plt.show()

'''
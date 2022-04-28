#//////////////////////////////////////
#
# Script to graphics from csv files
# Libelium Tags
#
# Carlos David Rodriguez
#

from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
import csv
import numpy as np
from matplotlib.ticker import MaxNLocator
import pylab as pl
import numpy as np
#%matplotlib inline
import time
import datetime
from sklearn.metrics import mean_squared_error







df = pd.read_json ('../MasterTesis1/AllIntel.json')
print(df.shape)
print(df.describe())
cdf = df[['fecha','ID','HAM','HSU','LUZ','BAT','TAM']]
timeDataSet = {}
# Convert field fechaDato to date time
timeDataSet['NewDateTime'] = pd.to_datetime(cdf['fecha'], format='%Y-%m-%d %H:%M:%S')
cdf.index = timeDataSet['NewDateTime']
cdf.index = cdf.index - pd.Timedelta('05:00:00') #Set Timezone
#Intel4 = cdf.loc[cdf['ID']=='IN_01_T_004']
Intel4 = cdf.loc[cdf['ID']=='IN_01_T_001']
Intel4 = Intel4.drop(columns=['ID','fecha',])
Intel4 = Intel4.loc[Intel4.index>= pd.to_datetime('2020-03-05 00:00:00',format='%Y-%m-%d %H:%M:%S')]
Intel4 = Intel4.loc[Intel4.index <= pd.to_datetime('2020-03-23 00:00:00',format='%Y-%m-%d %H:%M:%S')]
Intel4.index = Intel4.index #- pd.Timedelta('05:00:00') #Set Timezone





#Position of data
#0 radiacion
#1 Temperatura ambiente
#2 Humedad Ambiente
#3 Humedad suelo
#4 presion

TempData = Intel4.HSU
HumeData = Intel4.HSU
LightData = Intel4.LUZ
print("Humedad Data")
print(HumeData.head(4))

TempData = TempData.sort_index()

daySelected = 6
stringDay = '2020-03-'+str(daySelected).zfill(2)+' '
DataOneDay  = TempData.loc[stringDay+'00': stringDay+'23:59']
print(DataOneDay.head(10))
print(DataOneDay.index.max())
print(DataOneDay.index.min())
XminValue = DataOneDay.index.min()
XmaxValue = DataOneDay.index.max()


plt.rcParams.update({'font.size': 16})
'''
fig0, ax0 = plt.subplots(2,figsize=(20, 10))
plt.xlabel("Time " + " (days)") #+ DateBase.strftime("%Y-%m-%d")
ax0[0].plot(TempData.index, TempData.values, color='red',label='Temperature ')
ax0[0].set( ylabel='Temperature °c')
ax0[0].grid(True)
fig0.suptitle('Temperature and HumidityData at Coffee Farm')
ax0[1].plot(HumeData.index, HumeData.values, color='blue',label='Humidity ')
ax0[1].set( ylabel='% RH')
plt.gcf().autofmt_xdate()
ax0[1].grid(True)
#fig0.savefig("images/GroupDays.png")
fig0.show()
'''




#
minutesTotal = 60 * 24
InitialTime =  pd.to_datetime(stringDay)
errorLst = list()
#5 Min
DataOneDay5M = list()
VarValues5M = list()
DataValues5M = list()
ErrorVal5M = list()
absError5M =list()
for i in range(0,minutesTotal,5):
    InitialHour = pd.to_datetime(stringDay,infer_datetime_format=True)+ pd.Timedelta('00:'+str(i).zfill(2)+':00')
    FinalHour = pd.to_datetime(stringDay,infer_datetime_format=True) + pd.Timedelta('00:'+str(i+4).zfill(2) + ':59')
    dataHour = TempData.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
    print(dataHour.head(5))
    DataOneDay5M.append(dataHour.values.mean())
    VarValues5M.append(dataHour.values.var(ddof=0))
    meanValue = dataHour.values.mean()
    errorLst.clear()
    for i in range(dataHour.values.size):
        DataValues5M.append(meanValue)
        errorLst.append(meanValue)
        absError5M.append(abs(dataHour.values[i]-meanValue))
    if(dataHour.values.size >0):
         ErrorVal5M.append(mean_squared_error(dataHour.values, errorLst) )
    else:
        ErrorVal5M.append(0)
TotalTime = DataOneDay.resample('300S').mean()
Time5M = TotalTime.index

#15 Min
DataOneDay15M = list()
VarValues15M = list()
DataValues15M = list()
ErrorVal15M = list()
absError15M = list()
for i in range(0,minutesTotal,15):
    InitialHour = pd.to_datetime(stringDay,infer_datetime_format=True)+ pd.Timedelta('00:'+str(i).zfill(2)+':00')
    FinalHour = pd.to_datetime(stringDay,infer_datetime_format=True) + pd.Timedelta('00:'+str(i+14).zfill(2) + ':59')
    dataHour = TempData.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
    DataOneDay15M.append(dataHour.values.mean())
    VarValues15M.append(dataHour.values.var(ddof=0))
    meanValue = dataHour.values.mean()
    errorLst.clear()
    for i in range(dataHour.values.size):
        DataValues15M.append(meanValue)
        errorLst.append(meanValue)
        absError15M.append(abs(dataHour.values[i] - meanValue))
    if (dataHour.values.size > 0):
        ErrorVal15M.append(mean_squared_error(dataHour.values, errorLst) )
    else:
        ErrorVal15M.append(0)
TotalTime = DataOneDay.resample('900S').mean()
Time15M = TotalTime.index

#30 Min
DataOneDay30M = list()
VarValues30M = list()
DataValues30M = list()
ErrorVal30M = list()
absError30M = list()
for i in range(0,minutesTotal,30):
    InitialHour = pd.to_datetime(stringDay,infer_datetime_format=True)+ pd.Timedelta('00:'+str(i).zfill(2)+':00')
    FinalHour = pd.to_datetime(stringDay,infer_datetime_format=True) + pd.Timedelta('00:'+str(i+29).zfill(2) + ':59')
    dataHour = TempData.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
    DataOneDay30M.append(dataHour.values.mean())
    VarValues30M.append(dataHour.values.var(ddof=0))
    meanValue = dataHour.values.mean()
    errorLst.clear()
    for i in range(dataHour.values.size):
        DataValues30M.append(meanValue)
        errorLst.append(meanValue)
        absError30M.append(abs(dataHour.values[i] - meanValue))
    if (dataHour.values.size > 0):
        ErrorVal30M.append(mean_squared_error(dataHour.values, errorLst) )
    else:
        ErrorVal30M.append(0)
TotalTime = DataOneDay.resample('1800S').mean()
Time30M = TotalTime.index


#print("data selected")
#print(Time30M)
'''
TimeString30M = [date_obj.strftime('%H:%M:%S') for date_obj in Time30M]
print(TimeString30M)
df = pd.DataFrame(data={ "Time": TimeString30M})
df.to_csv("./VarFileH1.csv", sep=',',index=False)

VarCsv = pd.read_csv("VarFileH1.csv")
VarCsv[stringDay] = VarValues30M
VarCsv.to_csv("./VarFileH1.csv", sep=',',index=False)
'''



#Hour
DataOneDayH = list()
VarValuesH = list()
DataValuesH = list()
ErrorValH = list()
timeAbs = list()
for i in range(24):
    dataHour = TempData.loc[stringDay+str(i).zfill(2): stringDay+str(i).zfill(2)+':59']
    DataOneDayH.append(dataHour.values.mean())
    VarValuesH.append(dataHour.values.var(ddof=0))
    meanValue = dataHour.values.mean()
    errorLst.clear()
    for i in range(dataHour.values.size):
        DataValuesH.append(meanValue)
        errorLst.append(meanValue)
    if (dataHour.values.size > 0):
        ErrorValH.append(mean_squared_error(dataHour.values, errorLst) )
    else:
        ErrorValH.append(0)
TotalTime = DataOneDay.resample('H').mean()
TimeH = TotalTime.index


error5M = mean_squared_error(DataOneDay.values, DataValues5M)
error15M = mean_squared_error(DataOneDay.values, DataValues15M)
error30M = mean_squared_error(DataOneDay.values, DataValues30M)
errorH = mean_squared_error(DataOneDay.values, DataValuesH)



#Normal Data
fig1,ax1 = plt.subplots(figsize=(20, 10))
plt.xlabel("Day " + InitialHour.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel(" %RH ")
plt.plot(DataOneDay.index, DataOneDay.values, color='red',label='Humidity minuntes ')
plt.plot(Time5M, DataOneDay5M,'-.',  color='orange', label='5 Min error: %2.2f'%error5M)
plt.plot(Time15M, DataOneDay15M,'-.',  color='blue', label='15 Min error: %2.2f'%error15M)
plt.plot(Time30M, DataOneDay30M,'-.',  color='gray', label=' 30 Min error: %2.2f'%error30M)
#plt.plot(TimeH, DataOneDayH,'-.',  color='black', label='T° Hour error: %2.2f'%errorH)
plt.xlim(XminValue, XmaxValue)
plt.gcf().autofmt_xdate()
date_form = DateFormatter("%H-%M")
ax1.xaxis.set_major_formatter(date_form)
plt.legend(loc='lower right')
plt.title('Humidity Curve at Different Sampling Period')
plt.grid(True)
fig1.savefig("images/DaysH.png")
fig1.show()


fig2,ax2  = plt.subplots(figsize=(20, 10))
#Variance
plt.xlabel("Day " + InitialHour.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel("Variance %RH²")
plt.plot(Time5M, VarValues5M,  color='red',label='Variance 5 Min')
plt.plot(Time15M, VarValues15M,  color='orange',label='Variance 15 Min')
plt.plot(Time30M, VarValues30M,  color='blue',label='Variance 30 Min')
#plt.plot(TimeH, VarValuesH,  color='gray',label='Variance hour')
plt.gcf().autofmt_xdate()
ax2.xaxis.set_major_formatter(date_form)
plt.legend(loc='lower right')
plt.title('Variance curve at different Sampling period')
plt.grid(True)
fig2.savefig("images/DaysVarH.png")
fig2.show()


fig3,ax3  = plt.subplots(figsize=(20, 10))
plt.xlabel("Day " + InitialHour.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel("Absolute Error %RH")
plt.plot(DataOneDay.index, absError5M,  color='red',label='Error 5 Min')
plt.plot(DataOneDay.index, absError15M,  color='orange',label='Error 15 Min')
plt.plot(DataOneDay.index, absError30M,  color='blue',label='Error 30 Min')
#plt.plot(TimeH, ErrorValH,  color='gray',label='Error hour')
plt.gcf().autofmt_xdate()
ax3.xaxis.set_major_formatter(date_form)
plt.legend(loc='lower right')
plt.title('Abosolute Error at different Sampling period')
plt.grid(True)
fig3.savefig("images/absErrorH.png")
plt.show()






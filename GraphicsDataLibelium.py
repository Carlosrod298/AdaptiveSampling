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

print("Libelium Analysis")
df = pd.read_csv('libelium.csv')
# take a look at the dataset
print("head csv file")
print(df.head(1))
# summarize the data
print(df.shape)
print(df.describe())
# get the most importan fields
cdf = df[['fechaDato','idVariable','bateria','bateria_voltios','valor']]
timeDataSet = {}
# Convert field fechaDato to date time
timeDataSet['NewDateTime'] = pd.to_datetime(cdf['fechaDato'], unit='s')
cdf.index = timeDataSet['NewDateTime']
cdf.index = cdf.index - pd.Timedelta('05:00:00') #Set Timezone
#Position of data
#0 radiacion
#1 Temperatura ambiente
#2 Humedad Ambiente
#3 Humedad suelo
#4 presion

TempData = cdf.iloc[1::8]
HumeData = cdf.iloc[2::8]
LightData = cdf.iloc[0::8]
print("Humedad Data")
print(HumeData.head(4))

TempData = TempData.sort_index()
TempData = TempData.drop([TempData.index[0]]) # Delete first data
TempData.to_csv('Data2019.csv',float_format='%.2f',index=False) # rounded to two decimals
DataOct = TempData.loc['2019-10-22': '2019-11-16']

'''
DataOneweek  = TempData.loc['2019-11-22': '2019-12-30']
DataOneweek.to_csv('DataOneweek.csv',float_format='%.2f') # rounded to two decimals
XminValue = DataOneweek.index.min()
XmaxValue = DataOneweek.index.max()
plt.xlabel("Time")
plt.ylabel("Temperature")
plt.scatter(DataOneweek.index, DataOneweek.valor,  color='blue')
plt.xlim(XminValue, XmaxValue)
plt.show()
'''
print("Omicron Analysis")
dtf = pd.read_csv('../Clima/OmicronData.csv')
# get the most importan fields
cdtf = dtf[['fechaDato','idVariable','bateria','valor']]
timeDataSet = {}
# Convert field fechaDato to date time
timeDataSet['NewDateTime'] = pd.to_datetime(cdtf['fechaDato'], unit='s')
cdtf.index = timeDataSet['NewDateTime']
cdtf.index = cdtf.index - pd.Timedelta('05:00:00')
tempOmicron = cdtf.loc[cdtf['idVariable']==2]


daySelected = 25
stringDay = '2019-10-'+str(daySelected).zfill(2)+' '
DataOneDay  = TempData.loc[stringDay+'00': stringDay+'23:59']
DataOneDay.to_csv('DataOneDay.csv',float_format='%.2f',index=False) # rounded to two decimals
print(DataOneDay.index.max())
print(DataOneDay.index.min())
XminValue = DataOneDay.index.min()
XmaxValue = DataOneDay.index.max()



#
minutesTotal = 60 * 24
InitialTime =  pd.to_datetime(stringDay)
errorLst = list()
#5 Min
DataOneDay5M = list()
VarValues5M = list()
DataValues5M = list()
ErrorVal5M = list()

for i in range(0,minutesTotal,5):
    InitialHour = pd.to_datetime(stringDay,infer_datetime_format=True)+ pd.Timedelta('00:'+str(i).zfill(2)+':00')
    FinalHour = pd.to_datetime(stringDay,infer_datetime_format=True) + pd.Timedelta('00:'+str(i+4).zfill(2) + ':59')
    dataHour = TempData.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
    DataOneDay5M.append(dataHour.valor.mean())
    VarValues5M.append(dataHour.valor.var(ddof=0))
    meanValue = dataHour.valor.mean()
    errorLst.clear()
    for i in range(dataHour.valor.size):
        DataValues5M.append(meanValue)
        errorLst.append(meanValue)
    if(dataHour.valor.size >0):
         ErrorVal5M.append(mean_squared_error(dataHour.valor, errorLst) )
    else:
        ErrorVal5M.append(0)
TotalTime = DataOneDay.resample('300S').mean()
Time5M = TotalTime.index

#15 Min
DataOneDay15M = list()
VarValues15M = list()
DataValues15M = list()
ErrorVal15M = list()
for i in range(0,minutesTotal,15):
    InitialHour = pd.to_datetime(stringDay,infer_datetime_format=True)+ pd.Timedelta('00:'+str(i).zfill(2)+':00')
    FinalHour = pd.to_datetime(stringDay,infer_datetime_format=True) + pd.Timedelta('00:'+str(i+14).zfill(2) + ':59')
    dataHour = TempData.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
    DataOneDay15M.append(dataHour.valor.mean())
    VarValues15M.append(dataHour.valor.var(ddof=0))
    meanValue = dataHour.valor.mean()
    errorLst.clear()
    for i in range(dataHour.valor.size):
        DataValues15M.append(meanValue)
        errorLst.append(meanValue)
    if (dataHour.valor.size > 0):
        ErrorVal15M.append(mean_squared_error(dataHour.valor, errorLst) )
    else:
        ErrorVal15M.append(0)
TotalTime = DataOneDay.resample('900S').mean()
Time15M = TotalTime.index

#30 Min
DataOneDay30M = list()
VarValues30M = list()
DataValues30M = list()
ErrorVal30M = list()
for i in range(0,minutesTotal,30):
    InitialHour = pd.to_datetime(stringDay,infer_datetime_format=True)+ pd.Timedelta('00:'+str(i).zfill(2)+':00')
    FinalHour = pd.to_datetime(stringDay,infer_datetime_format=True) + pd.Timedelta('00:'+str(i+29).zfill(2) + ':59')
    dataHour = TempData.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
    DataOneDay30M.append(dataHour.valor.mean())
    VarValues30M.append(dataHour.valor.var(ddof=0))
    meanValue = dataHour.valor.mean()
    errorLst.clear()
    for i in range(dataHour.valor.size):
        DataValues30M.append(meanValue)
        errorLst.append(meanValue)
    if (dataHour.valor.size > 0):
        ErrorVal30M.append(mean_squared_error(dataHour.valor, errorLst) )
    else:
        ErrorVal30M.append(0)
TotalTime = DataOneDay.resample('1800S').mean()
Time30M = TotalTime.index


#print("data selected")
#print(Time30M)
#TimeString30M = [date_obj.strftime('%H:%M:%S') for date_obj in Time30M]
#print(TimeString30M)
#df = pd.DataFrame(data={ "Time": TimeString30M})
#df.to_csv("./VarFile.csv", sep=',',index=False)
'''
VarCsv = pd.read_csv("VarFile.csv")
VarCsv[stringDay] = VarValues30M
VarCsv.to_csv("./VarFile.csv", sep=',',index=False)
'''



#Hour
DataOneDayH = list()
VarValuesH = list()
DataValuesH = list()
ErrorValH = list()
for i in range(24):
    dataHour = TempData.loc[stringDay+str(i).zfill(2): stringDay+str(i).zfill(2)+':59']
    DataOneDayH.append(dataHour.valor.mean())
    VarValuesH.append(dataHour.valor.var(ddof=0))
    meanValue = dataHour.valor.mean()
    errorLst.clear()
    for i in range(dataHour.valor.size):
        DataValuesH.append(meanValue)
        errorLst.append(meanValue)
    if (dataHour.valor.size > 0):
        ErrorValH.append(mean_squared_error(dataHour.valor, errorLst) )
    else:
        ErrorValH.append(0)
TotalTime = DataOneDay.resample('H').mean()
TimeH = TotalTime.index


error5M = mean_squared_error(DataOneDay.valor, DataValues5M)
error15M = mean_squared_error(DataOneDay.valor, DataValues15M)
error30M = mean_squared_error(DataOneDay.valor, DataValues30M)
errorH = mean_squared_error(DataOneDay.valor, DataValuesH)

#Normal Data
fig1,ax1 = plt.subplots()
plt.xlabel("Day " + InitialHour.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel(" Temperature °c ")
plt.plot(DataOneDay.index, DataOneDay.valor, color='red',label='Temperature minuntes ')
plt.plot(Time5M, DataOneDay5M,'-.',  color='orange', label='T° 5 Min error: %2.2f'%error5M)
plt.plot(Time15M, DataOneDay15M,'-.',  color='blue', label='T° 15 Min error: %2.2f'%error15M)
plt.plot(Time30M, DataOneDay30M,'-.',  color='gray', label='T° 30 Min error: %2.2f'%error30M)
plt.plot(TimeH, DataOneDayH,'-.',  color='black', label='T° Hour error: %2.2f'%errorH)
plt.xlim(XminValue, XmaxValue)
plt.gcf().autofmt_xdate()
date_form = DateFormatter("%H-%M")
ax1.xaxis.set_major_formatter(date_form)
plt.legend(loc='upper right')
plt.title('Temperature curve at different Sampling period')
plt.grid(True)
plt.show()


fig2,ax2  = plt.subplots()
#Variance
plt.xlabel("Day " + InitialHour.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel("Variance °c²")
plt.plot(Time5M, VarValues5M,  color='red',label='Variance 5 Min')
plt.plot(Time15M, VarValues15M,  color='orange',label='Variance 15 Min')
plt.plot(Time30M, VarValues30M,  color='blue',label='Variance 30 Min')
plt.plot(TimeH, VarValuesH,  color='gray',label='Variance hour')
plt.gcf().autofmt_xdate()
ax2.xaxis.set_major_formatter(date_form)
plt.legend(loc='upper right')
plt.title('Variance curve at different Sampling period')
plt.grid(True)
plt.show()

fig3,ax3  = plt.subplots()
plt.xlabel("Day " + InitialHour.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel("Mean Squared Error °c²")
plt.plot(Time5M, ErrorVal5M,  color='red',label='Error 5 Min')
plt.plot(Time15M, ErrorVal15M,  color='orange',label='Error 15 Min')
plt.plot(Time30M, ErrorVal30M,  color='blue',label='Error 30 Min')
plt.plot(TimeH, ErrorValH,  color='gray',label='Error hour')
plt.gcf().autofmt_xdate()
ax3.xaxis.set_major_formatter(date_form)
plt.legend(loc='upper right')
plt.title('MSE at different Sampling period')
plt.grid(True)
plt.show()






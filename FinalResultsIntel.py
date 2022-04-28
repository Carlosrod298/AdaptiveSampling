#Import Data on Json intel
#Intel: http://76.74.150.54:8092/ws_iot-agro/GetIntel/?anio=2020&mes=11&dia=12
#Libelium: http://76.74.150.54:8092/ws_iot-agro/GetLibelium/?anio=2020&mes=6&dia=4
#Omicron http://76.74.150.54:8092/ws_iot-agro/GetOmicron/?anio=2020&mes=6&dia=4




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
cdf = df[['fecha','ID','TAM','HAM','LUZ','BAT']]
timeDataSet = {}
# Convert field fechaDato to date time
timeDataSet['NewDateTime'] = pd.to_datetime(cdf['fecha'], format='%Y-%m-%d %H:%M:%S')
cdf.index = timeDataSet['NewDateTime'] - pd.Timedelta('05:00:00') #Set Timezone
#cdf['Time2'] = timeDataSet['NewDateTime'] - pd.Timedelta('05:00:00')
cdf = cdf.fillna(method ='bfill')
Intel1 = cdf.loc[cdf['ID'] == 'IN_01_T_001']
Intel2 = cdf.loc[cdf['ID'] == 'IN_01_T_003']
Intel1 = Intel1.drop(columns=['ID','fecha' ])
Intel2 = Intel2.drop(columns=['ID','fecha' ])






daySelected = 14
stringDay = '2020-11-'+str(daySelected).zfill(2)+' '
daySelected2 = daySelected+1
stringDay2 = '2020-11-'+str(daySelected2).zfill(2)+' '
Intel1  = Intel1.loc[stringDay+'00:40:00': stringDay+'23:30:00']
Intel2  = Intel2.loc[stringDay+'00:00:00': stringDay2+'00:50:00']
print(Intel1.head(4))
DateBase = Intel1.index[0]


'''
fig0,ax0 = plt.subplots(figsize=(20, 10))
plt.plot(Intel1.index, Intel1.TAM, color='red', label='Temperature per minunte ')
plt.plot(Intel2.index, Intel2.TAM, color='blue', label='Adaptable Time 1')
plt.title('Humidity Curve at Different Sampling Period')
plt.grid(True)
plt.show()
'''
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


#NormalST =  pd.DataFrame(data=TimeDiffe4,columns= column_names)
#AdaptativeEmbebed = pd.DataFrame(data=TimeDiffe5,columns= column_names)
#AdaptativeGW = pd.DataFrame(data=TimeDiffe6,columns= column_names)
#print(AdaptativeEmbebed.head(5))

#Intel2.to_csv("./Intel2Normal.csv", sep=',',index=True)

from scipy.interpolate import interp1d
TimeSeconds = [time.mktime(t.timetuple()) for t in Intel2.index]
print(TimeSeconds)
TempFunction = interp1d(TimeSeconds, Intel2.TAM )
HumeFunction = interp1d(TimeSeconds, Intel2.HAM )

TimeSeconds1 = [time.mktime(t.timetuple()) for t in Intel1.index]
print(TimeSeconds1)
TempeValues = TempFunction(TimeSeconds1)
print(TempeValues)
HumeValues  = HumeFunction(TimeSeconds1)
print(HumeValues)
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


Intel1E = Intel1[['TAM','HAM']]
minutesTotal = 60 * 24
#5 Min
Values5MT = list()
Values5MH = list()
for i in range(0,minutesTotal,5):
    InitialHour = pd.to_datetime(stringDay,infer_datetime_format=True)+ pd.Timedelta('00:'+str(i).zfill(2)+':00')
    FinalHour = pd.to_datetime(stringDay,infer_datetime_format=True) + pd.Timedelta('00:'+str(i+4).zfill(2) + ':59')
    dataHour = Intel1E.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
    meanValueT = dataHour.TAM.mean()
    meanValueH = dataHour.HAM.mean()
    for i in range(dataHour.TAM.size):
        Values5MT.append(meanValueT)
        Values5MH.append(meanValueH)
errorTAM5M = mean_squared_error(Intel1E.TAM, Values5MT)
errorHAM5H = mean_squared_error(Intel1E.HAM, Values5MH)
dfm = pd.DataFrame({'tempe':Values5MT,'humi':Values5MH})
dfm.index = Intel1.index
corrTAM5M = Intel1.TAM.corr(dfm.tempe)
corrHAM5H = Intel1.HAM.corr(dfm.humi)
nseTAM5M = he.nse(Values5MT,dfm.tempe.to_numpy())
nseTAM5H = he.nse(Values5MH,dfm.humi.to_numpy())

Values15MT = list()
Values15MH = list()
for i in range(0,minutesTotal,15):
    InitialHour = pd.to_datetime(stringDay,infer_datetime_format=True)+ pd.Timedelta('00:'+str(i).zfill(2)+':00')
    FinalHour = pd.to_datetime(stringDay,infer_datetime_format=True) + pd.Timedelta('00:'+str(i+14).zfill(2) + ':59')
    dataHour = Intel1E.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
    meanValueT = dataHour.TAM.mean()
    meanValueH = dataHour.HAM.mean()
    for i in range(dataHour.TAM.size):
        Values15MT.append(meanValueT)
        Values15MH.append(meanValueH)
errorTAM15M = mean_squared_error(Intel1E.TAM, Values15MT)
errorHAM15H = mean_squared_error(Intel1E.HAM, Values15MH)
dfm = pd.DataFrame({'tempe':Values15MT,'humi':Values15MH})
dfm.index = Intel1.index
corrTAM15M = Intel1.TAM.corr(dfm.tempe)
corrHAM15H = Intel1.HAM.corr(dfm.humi)
nseTAM15M = he.nse(Values15MT,dfm.tempe.to_numpy())
nseTAM15H = he.nse(Values15MH,dfm.humi.to_numpy())

Values30MT = list()
Values30MH = list()
for i in range(0,minutesTotal,30):
    InitialHour = pd.to_datetime(stringDay,infer_datetime_format=True)+ pd.Timedelta('00:'+str(i).zfill(2)+':00')
    FinalHour = pd.to_datetime(stringDay,infer_datetime_format=True) + pd.Timedelta('00:'+str(i+29).zfill(2) + ':59')
    dataHour = Intel1E.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
    meanValueT = dataHour.TAM.mean()
    meanValueH = dataHour.HAM.mean()
    for i in range(dataHour.TAM.size):
        Values30MT.append(meanValueT)
        Values30MH.append(meanValueH)
errorTAM30M = mean_squared_error(Intel1E.TAM, Values30MT)
errorHAM30H = mean_squared_error(Intel1E.HAM, Values30MH)
dfm = pd.DataFrame({'tempe':Values30MT,'humi':Values30MH})
dfm.index = Intel1.index
corrTAM30M = Intel1.TAM.corr(dfm.tempe)
corrHAM30H = Intel1.HAM.corr(dfm.humi)
nseTAM30M = he.nse(Values30MT,dfm.tempe.to_numpy())
nseTAM30H = he.nse(Values30MH,dfm.humi.to_numpy())

# Get power comsuption
# Diff time
TimeDife = pd.to_numeric(Intel2['DiffTime'].dt.seconds, downcast='integer')
MinuteVal = [round(value/60) for value in TimeDife.values]
sumValue = 0
for x in MinuteVal:
    powerComs = CCFun.Compsuption(x) * x
    sumValue = sumValue + powerComs
AverageAT = sumValue/(sum(MinuteVal))
Temperature = [errorTAM5M, errorTAM15M,errorTAM30M,errorTAM]
Humidity = [errorHAM5H, errorHAM15H,errorTAM30M,errorHAM]
Consumption = [CCFun.Compsuption(5),CCFun.Compsuption(8),CCFun.Compsuption(9),AverageAT]
CorrTemp = [corrTAM5M,corrTAM15M,corrTAM30M,corrTAM]
CorrHumi = [corrHAM5H,corrHAM15H,corrHAM30H,corrHAM]
NseValsT = [nseTAM5M,nseTAM15M,nseTAM30M,nseTAM]
NseValsH = [nseTAM5H,nseTAM15H,nseTAM30H,nseHAM]
maresT =   [mareT,mareH,MBET,MBEH]
print("tiempo en int ")
print(sum(MinuteVal)/60)
print("Error temp  ")
print(Temperature)
print("Error Hume  ")
print(Humidity)
print("Corr temp ")
print(CorrTemp)
print("Corr Hume ")
print(CorrHumi)
print("Comsuption ")
print(Consumption)
print("NseValsT ")
print(NseValsT)
print("NseValsH ")
print(NseValsH)
print("mares ")
print(maresT)

#Consumptionvector = [(CCFun.Compsuption(x)) for x in Psampling]





#Normal Data
plt.rcParams.update({'font.size': 16})
index = ['5 min', '15 min','30 min','Adaptable']
ErrorsData = pd.DataFrame({'Temperature': Temperature,
                           'Humidity': Humidity,
                           'CorrTemp':CorrTemp,
                           'CorrHumi':CorrHumi,
                           'Current':Consumption}, index=index)
ax = ErrorsData.plot.bar(figsize=(20, 10),rot=0, subplots=True,title="MSE vs Sampling Time",
                         color=['#f39c12', '#2980b9','#27ae60'])
plt.xlabel("Sampling Times")
ax[0].set( ylabel='MSE °c²')
ax[1].set( ylabel='MSE %RH²')
ax[2].set( ylabel=' uA')
ax[0].legend(loc=2)
ax[1].legend(loc=2)
ax[2].legend(loc=2)


fig1,ax1 = plt.subplots(figsize=(20, 10))
plt.xlabel("Day  (Hours:Minutes)")
plt.ylabel(" Temperature "+r'$ \degree $'+ ' c')
plt.plot(Intel1.index, Intel1.TAM, color='red', label='Temperature per minunte ')
plt.plot(Intel2.index, Intel2.TAM, color='blue', label='Adaptable Time error: %2.2f'%errorTAM)
#plt.plot(Intel1Av.index, Intel1Av.TAM, color='black', label='media 1 minute')
#plt.plot(Intel2Av.index, Intel2Av.TAM, color='green', label='media adapt')
ax1.xaxis.set_major_locator(plt.MaxNLocator(22))
ax1.set_ylim(10, 35)
plt.gcf().autofmt_xdate()
date_form = DateFormatter("%H:%M")
ax1.xaxis.set_major_formatter(date_form)
plt.legend(loc='upper right')
plt.title('Temperature Curve ' + DateBase.strftime("%Y-%m-%d"))
plt.grid(True)
fig1.savefig("images/ResultTemp.png")
fig1.show()

#Normal Data
fig2, ax2 = plt.subplots(figsize=(20, 10))
plt.xlabel("Day  (Hours:Minutes)")
plt.ylabel("Humidity %RH")
plt.plot(Intel1.index, Intel1.HAM, color='red',     label='Humidity per minuntes ')
plt.plot(Intel1.index, HumeValues, color='blue',    label='Adaptable Time error: %2.4f'%errorHAM)
#plt.plot(Intel1.index, Values30MH, color='green',    label='30 min Time error: %2.4f'%errorHAM30H)
#plt.plot(Intel1Av.index, Intel1Av.HAM, color='black', label='media 1 minute')
#plt.plot(Intel2Av.index, Intel2Av.HAM, color='green', label='media adapt')
plt.gcf().autofmt_xdate()
ax2.xaxis.set_major_formatter(date_form)
ax2.xaxis.set_major_locator(plt.MaxNLocator(22))
ax2.set_ylim(50, 100)
plt.legend(loc='upper right')
plt.title('Humidity Curve '+ DateBase.strftime("%Y-%m-%d"))
plt.grid(True)
fig2.savefig("images/ResultHume.png")
fig2.show()

#Normal Data
fig3, ax3 = plt.subplots(figsize=(20, 10))
plt.xlabel("Day " + " (Hours)")
plt.ylabel("Sampling time (Minutes)")
#plt.plot(Intel1.index, (Intel1['DiffTime'].dt.total_seconds()) / 60, color='red',   label='One Minute')
plt.plot(Intel2.index, (Intel2['DiffTime'].dt.total_seconds()) / 60, color='blue')
ax3.xaxis.set_major_locator(plt.MaxNLocator(22))
plt.gcf().autofmt_xdate()
ax3.xaxis.set_major_formatter(date_form)
plt.title('Adaptative Time ' + DateBase.strftime("%Y-%m-%d"))
plt.grid(True)
fig3.savefig("images/AdaptableTime.png")
plt.show()


#Intel4.to_csv('Intel4.csv',float_format='%.2f',index=True) # rounded to two decimals
#Intel5.to_csv('Intel5.csv',float_format='%.2f',index=True) # rounded to two decimals
#Intel6.to_csv('Intel6.csv',float_format='%.2f',index=True) # rounded to two decimals



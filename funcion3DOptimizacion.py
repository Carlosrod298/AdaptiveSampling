#Ecuacion de intervalo de muestreo
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import pandas as pd
# Handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters

from MasterTesis import ReadDay
from sklearn.metrics import mean_squared_error



def getSampling(VarValues, Beta , Alpha):
    FSmin = 1.0 / (30 * 60)  # minimal sampling interval hz
    FSmax = 1.0 / 60  # max  sampling interval  hz
    FSampling = list()

    for variance in VarValues:
        FS = variance * Beta * FSmax + Alpha
        if (FS < FSmin):
            FS = FSmin
        if (FS > FSmax):
            FS = FSmax
        FSampling.append(FS)
    #FSamplingTime = [FSampling,]
    return FSampling



DefAdapt = 1
Def30min = 1
Def5min = 1

#Get Day
df = pd.read_json ('August12.json')
cdf = df[['fecha','ID','HAM','HSU','LUZ','BAT']]
timeDataSet = {}
# Convert field fechaDato to date time
timeDataSet['NewDateTime'] = pd.to_datetime(cdf['fecha'], format='%Y-%m-%d %H:%M:%S')
cdf.index = timeDataSet['NewDateTime']
cdf.index = cdf.index - pd.Timedelta('05:00:00') #Set Timezone

Intel4 = cdf.loc[cdf['ID']=='IN_01_T_004']
Intel4 = Intel4.drop(columns=['ID','fecha',])
print(Intel4.head(4))
DateBase = Intel4.index[0]
stringDay = DateBase.strftime("%Y-%m-%d ")  #'2019-08-'+str(12).zfill(2)+' '
Intel4  = Intel4.loc[stringDay+'00': stringDay+'23:59']
print(DateBase)

#Get Variance
stringDay = DateBase.strftime("%Y-%m-%d ")  #'2019-08-'+str(12).zfill(2)+' '
minutesTotal = 60 * 24
InitialTime =  pd.to_datetime(stringDay)
errorLst = list()
#30 Min
VarValues30M = list()
for i in range(0,minutesTotal,30):
    InitialHour = pd.to_datetime(stringDay,infer_datetime_format=True)+ pd.Timedelta('00:'+str(i).zfill(2)+':00')
    FinalHour = pd.to_datetime(stringDay,infer_datetime_format=True) + pd.Timedelta('00:'+str(i+29).zfill(2) + ':59')
    dataWindow = Intel4.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
    VarValues30M.append(dataWindow['HAM'].var(ddof=0))

#variance
print(VarValues30M)
FSampling = getSampling(VarValues30M,1,0)
Psample = [int(round(1 / (60 * x))) for x in FSampling]
#add previus Sampling time
Psampling  = [30]
for x in Psample:
    Psampling.append(x)
# Sampling selected
Psampling.pop()
print(Psampling)



#Adaptable Time
DataOneDayAM = list()
VarValuesAM = list()
DataValuesAM = list()
TimeAM = list()
minutesTotal = 30
counter = 0
errorLst = list()
ErrorValAM = list()

for adapTime in Psampling:
    baseMinutes = counter*30
    counter = counter+1
    for i in range(0,minutesTotal,adapTime):
        InitialMin = baseMinutes + i
        finMin = baseMinutes + i + adapTime - 1
        if(finMin > (baseMinutes+minutesTotal)):
            finMin = baseMinutes + minutesTotal - 1
        InitialHour = DateBase + pd.Timedelta('00:'+str(InitialMin).zfill(2)+':00')
        FinalHour = DateBase + pd.Timedelta('00:'+str(finMin).zfill(2) + ':59')
        dataWindow = Intel4.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
        if(dataWindow.index.size > 0):
            DataOneDayAM.append(dataWindow['HAM'].mean())          #average value
            TimeAM.append(dataWindow.index.mean())                #average time
            VarValuesAM.append(dataWindow['HAM'].var(ddof=0))      #Variace
            meanValue = dataWindow['HAM'].mean()
            errorLst.clear()
            for i in range(dataWindow['HAM'].size):
                DataValuesAM.append(meanValue)
                errorLst.append(meanValue)
            ErrorValAM.append(mean_squared_error(dataWindow['HAM'], errorLst) )
        else:
            #print("No data")
            DataOneDayAM.append(DataOneDayAM[-1])  # average value
            finMin = baseMinutes + i + (adapTime/2)
            TimeAM.append(TimeAM[-1] + pd.Timedelta('00:00:30') )  # average time
            VarValuesAM.append(VarValuesAM[-1])
            ErrorValAM.append(0)


AdapSample = pd.DataFrame(DataOneDayAM,index =TimeAM,columns =['Temperature'])

#5 Min
minutesTotal = 60 * 24
DataOneDay5M = list()
VarValues5M = list()
DataValues5M = list()
ErrorVal5M = list()
for i in range(0,minutesTotal,5):
    InitialHour = DateBase + pd.Timedelta('00:'+str(i).zfill(2)+':00')
    FinalHour = DateBase + pd.Timedelta('00:'+str(i+4).zfill(2) + ':59')
    dataWindow = Intel4.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
    DataOneDay5M.append(dataWindow['HAM'].mean())
    VarValues5M.append(dataWindow['HAM'].var(ddof=0))
    meanValue = dataWindow['HAM'].mean()
    errorLst.clear()
    for i in range(dataWindow['HAM'].size):
        DataValues5M.append(meanValue)
        errorLst.append(meanValue)
    if(dataWindow['HAM'].size >0):
         ErrorVal5M.append(mean_squared_error(dataWindow['HAM'], errorLst) )
    else:
        ErrorVal5M.append(0)
TotalTime = Intel4.resample('300S').mean()
Time5M = TotalTime.index


#30 Min
DataOneDay30M = list()
VarValues30M = list()
DataValues30M = list()
ErrorVal30M = list()
for i in range(0,minutesTotal,30):
    InitialHour = DateBase+ pd.Timedelta('00:'+str(i).zfill(2)+':00')
    FinalHour = DateBase + pd.Timedelta('00:'+str(i+29).zfill(2) + ':59')
    dataWindow = Intel4.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
    DataOneDay30M.append(dataWindow['HAM'].mean())
    VarValues30M.append(dataWindow['HAM'].var(ddof=0))
    meanValue = dataWindow['HAM'].mean()
    errorLst.clear()
    for i in range(dataWindow['HAM'].size):
        DataValues30M.append(meanValue)
        errorLst.append(meanValue)
    if (dataWindow['HAM'].size > 0):
        ErrorVal30M.append(mean_squared_error(dataWindow['HAM'], errorLst) )
    else:
        ErrorVal30M.append(0)
TotalTime = Intel4.resample('1800S').mean()
Time30M = TotalTime.index


errorAM = mean_squared_error(Intel4['HAM'], DataValuesAM)
error30M = mean_squared_error(Intel4['HAM'], DataValues30M)
error5M = mean_squared_error(Intel4['HAM'], DataValues5M)


fig2,ax2 = plt.subplots()
plt.xlabel("Day " + InitialHour.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel(" Temperature °c ")
plt.plot(Intel4.index, Intel4['HAM'],  color='blue',label='1 min sampling ')
if DefAdapt:
    plt.plot(AdapSample.index, AdapSample.Temperature,  color='red',label='Adaptative sampling error: %2.2f'%errorAM)
if Def30min:
    plt.plot(Time30M, DataOneDay30M,  color='green',label='30 min sampling error: %2.2f'%error30M)
if Def5min:
    plt.plot(Time5M, DataOneDay5M, color='purple', label='5 min sampling error: %2.2f'%error5M)
plt.gcf().autofmt_xdate()
date_form = DateFormatter("%H-%M")
ax2.xaxis.set_major_formatter(date_form)
plt.legend(loc='upper right')
plt.title('Temperature vs Sampling Times')
plt.grid(True)
fig2.show()


fig3, ax3 = plt.subplots()
plt.xlabel("Day " + InitialHour.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel("MSE Temperature (°c²)")
if DefAdapt:
    plt.plot(AdapSample.index, ErrorValAM,  color='blue',label='Error Adaptative sampling')
if Def30min:
    plt.plot(Time30M, ErrorVal30M,  color='red',label='Error 30 min sampling')
if Def5min:
    plt.plot(Time5M, ErrorVal5M, color='purple', label='Error 5 min sampling')
plt.gcf().autofmt_xdate()
ax3.xaxis.set_major_formatter(date_form)
plt.legend(loc='upper right')
plt.title('Mean Squared Error vs  Sampling Times')
plt.grid(True)
fig3.show()


fig4, ax4 = plt.subplots()
#Variance
plt.xlabel("Day " + InitialHour.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel("Variance")
if DefAdapt:
    plt.plot(AdapSample.index, VarValuesAM,  color='blue',label='Adaptative Variance')
if Def30min:
    plt.plot(Time30M, VarValues30M,  color='red',label='Variance 30 Min')
if Def5min:
    plt.plot(Time5M, VarValues5M,  color='purple',label='Variance 5 Min')
plt.gcf().autofmt_xdate()
ax4.xaxis.set_major_formatter(date_form)
plt.legend(loc='upper right')
plt.title('Variance vs Sampling Times')
plt.grid(True)
plt.show()






'''
#Normal Data
fig1,ax1 = plt.subplots()
plt.xlabel("Day " + InitialHour.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel(" Temperature °c ")
plt.plot(Intel4.index, Intel4['HAM'], color='red',label='Temperature minuntes ')
plt.plot(Time30M, DataOneDay30M,'-.',  color='gray', label='T° 30 Min error: %2.2f'%error30M)
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
plt.plot(Time30M, VarValues30M,  color='blue',label='Variance 30 Min')
plt.gcf().autofmt_xdate()
ax2.xaxis.set_major_formatter(date_form)
plt.legend(loc='upper right')
plt.title('Variance curve at different Sampling period')
plt.grid(True)
plt.show()

fig3,ax3  = plt.subplots()
plt.xlabel("Day " + InitialHour.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel("Mean Squared Error °c²")
plt.plot(Time30M, ErrorVal30M,  color='blue',label='Error 30 Min')
plt.gcf().autofmt_xdate()
ax3.xaxis.set_major_formatter(date_form)
plt.legend(loc='upper right')
plt.title('MSE at different Sampling period')
plt.grid(True)
plt.show()

'''


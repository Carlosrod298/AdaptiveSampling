#Ecuacion de intervalo de muestreo
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import pandas as pd
# Handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters

from MasterTesis import ReadDay
from sklearn.metrics import mean_squared_error


DefAdapt = 1
Def30min = 0
Def5min = 1

FSamplingTime = ReadDay.getSampling(1,0)
FSampling = FSamplingTime.FSampling
Psampling = [int(round(1 / (60 * x))) for x in FSampling]
print(Psampling)

# Create figure and plot space
#fig1 = plt.figure(1)
fig1, ax1 = plt.subplots()
plt.xlabel("Time (Hour) ")
plt.ylabel("Sampling Period (min)")
plt.plot(FSamplingTime.index, Psampling,  color='blue',label='Adaptative Period Sampling Selected')
plt.gcf().autofmt_xdate()
date_form = DateFormatter("%H-%M")
ax1.xaxis.set_major_formatter(date_form)
plt.legend(loc='lower right')
plt.title(' Sampling Time vs Day Hour ')
plt.grid(True)
fig1.show()


# calling functions
DataOneDay = ReadDay.SelectDay2019(10, 28)
DateBase = DataOneDay.index[0]
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
        dataHour = DataOneDay.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
        #print("Range " + InitialHour.strftime("%Y-%m-%d %H:%M:%S") +" "+ FinalHour.strftime("%Y-%m-%d %H:%M:%S"))
        if(dataHour.index.size > 0):
            DataOneDayAM.append(dataHour.valor.mean())          #average value
            TimeAM.append(dataHour.index.mean())                #average time
            VarValuesAM.append(dataHour.valor.var(ddof=0))      #Variace
            meanValue = dataHour.valor.mean()
            errorLst.clear()
            for i in range(dataHour.valor.size):
                DataValuesAM.append(meanValue)
                errorLst.append(meanValue)
            ErrorValAM.append(mean_squared_error(dataHour.valor, errorLst) )
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
    dataHour = DataOneDay.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
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


#30 Min
DataOneDay30M = list()
VarValues30M = list()
DataValues30M = list()
ErrorVal30M = list()
for i in range(0,minutesTotal,30):
    InitialHour = DateBase+ pd.Timedelta('00:'+str(i).zfill(2)+':00')
    FinalHour = DateBase + pd.Timedelta('00:'+str(i+29).zfill(2) + ':59')
    dataHour = DataOneDay.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
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


errorAM = mean_squared_error(DataOneDay.valor, DataValuesAM)
error30M = mean_squared_error(DataOneDay.valor, DataValues30M)
error5M = mean_squared_error(DataOneDay.valor, DataValues5M)

'''
ErrorCsvVal = [errorAM,error5M,error30M]
#ErrorCsv = pd.DataFrame(ErrorCsvVal, columns = [DateBase])
ErrorCsv = pd.read_csv("ErrorCsv.csv")
ErrorCsv[DateBase] = ErrorCsvVal
ErrorCsv.to_csv("./ErrorCsv.csv", sep=',',index=False)
'''

print(str(InitialHour.strftime("%Y-%m-%d")))
fig2,ax2 = plt.subplots()
plt.xlabel("Day " + InitialHour.strftime("%Y-%m-%d")+ " (Hours)")
plt.ylabel(" Temperature °c ")
plt.plot(DataOneDay.index, DataOneDay.valor,  color='blue',label='1 min sampling ')
if DefAdapt:
    plt.plot(AdapSample.index, AdapSample.Temperature,  color='red',label='Adaptative sampling error: %2.2f'%errorAM)
if Def30min:
    plt.plot(Time30M, DataOneDay30M,  color='green',label='30 min sampling error: %2.2f'%error30M)
if Def5min:
    plt.plot(Time5M, DataOneDay5M, color='purple', label='5 min sampling error: %2.2f'%error5M)
plt.gcf().autofmt_xdate()
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

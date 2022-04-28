#Ecuacion de intervalo de muestreo
import matplotlib.pyplot as plt


import pandas as pd
import numpy as np
from numpy import savetxt
# Handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters

from MasterTesis import CCFun
from sklearn.metrics import mean_squared_error



def getSampling(VarValues, AlphaV , BetaV):
    FSmin = 1.0 / (30 * 60)  # minimal sampling interval hz
    FSmax = 1.0 / 60  # max  sampling interval  hz
    FSampling = list()

    for variance in VarValues:
        FS = variance * AlphaV  + BetaV
        if (FS < FSmin):
            FS = FSmin
        if (FS > FSmax):
            FS = FSmax
        FSampling.append(FS)
    return FSampling

def ErrorOnAdapt(Psample,DateBaseDay,IntelData):
    # Error on Adaptable Time
    DataValuesAM = list()
    minutesTotal = 30
    counter = 0
    for adapTime in Psample:
        baseMinutes = counter * 30
        counter = counter + 1
        for i in range(0, minutesTotal, adapTime):
            InitialMin = baseMinutes + i
            finMin = baseMinutes + i + adapTime - 1
            if (finMin > (baseMinutes + minutesTotal)):
                finMin = baseMinutes + minutesTotal - 1
            InitialHour = DateBaseDay + pd.Timedelta('00:' + str(InitialMin).zfill(2) + ':00')
            FinalHour = DateBaseDay + pd.Timedelta('00:' + str(finMin).zfill(2) + ':59')
            dataWindow = IntelData.loc[InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
            if (dataWindow.index.size > 0):
                meanValue = dataWindow['HSU'].mean()
                for i in range(dataWindow['HSU'].size):
                    DataValuesAM.append(meanValue)

    return float(mean_squared_error(Intel4['HSU'], DataValuesAM))



df = pd.read_json ('../MasterTesis1/AllIntel.json')
cdf = df[['fecha','ID','HSU','LUZ','BAT','TAM']]
timeDataSet = {}
# Convert field fechaDato to date time
timeDataSet['NewDateTime'] = pd.to_datetime(cdf['fecha'], format='%Y-%m-%d %H:%M:%S')
cdf.index = timeDataSet['NewDateTime']
cdf.index = cdf.index - pd.Timedelta('05:00:00') #Set Timezone
Intel4 = cdf.loc[cdf['ID']=='IN_01_T_004']
Intel4 = Intel4.drop(columns=['ID','fecha',])
daySelected = 17
stringDay = '2020-08-'+str(daySelected).zfill(2)+' '
Intel4 = Intel4.loc[Intel4.index >= pd.to_datetime(stringDay+'00:00:00',format='%Y-%m-%d %H:%M:%S')]
Intel4 = Intel4.loc[Intel4.index <= pd.to_datetime(stringDay+'23:59:59',format='%Y-%m-%d %H:%M:%S')]

print(Intel4.head(4))
DateBase = Intel4.index[0]
stringDay = DateBase.strftime("%Y-%m-%d ")
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
    VarValues30M.append(dataWindow['HSU'].var(ddof=0))

#variance
print(VarValues30M)
print(min(VarValues30M))
print(max(VarValues30M))
print( 1.0 / (30 * 60))  # minimal sampling interval hz
print( 1.0 / 60)  # max  sampling interval  hz

MaxError = 0.3
MaxCurrent = CCFun.MaxCompsuption()
print("MaxCurrent %f"%MaxCurrent)

# Make data.
Alpha = np.arange(0, 0.1, 1e-3)
lenVectorA = len(Alpha)
ListErrro = list()
ListCurre = list()
for i in range(lenVectorA):
    FSampling = getSampling(VarValues30M,Alpha[i],0.0)
    Psample = [int(round(1 / (60 * x))) for x in FSampling]
    #add previus Sampling time
    Psampling  = [30]
    for x in Psample:
        Psampling.append(x)
    Psampling.pop()# Delete last sample
    Errorvector = (ErrorOnAdapt(Psampling,DateBase,Intel4))*1.0
    Consumptionvector = [(CCFun.Compsuption(x)) for x in Psampling]
    meanConsumption  =((np.array(Consumptionvector)).mean())*1.0
    ListErrro.append(Errorvector)
    ListCurre.append(meanConsumption)
    print(Alpha[i])

print(ListErrro)
print(ListCurre)

fig2,ax2 = plt.subplots()
plt.xlabel(" Aplha ")
plt.ylabel(" Error ")
plt.plot(Alpha, ListErrro ,color='blue',label='1 min sampling ')
plt.plot(Alpha, ListCurre ,color='red',label='1 min sampling ')
plt.gcf().autofmt_xdate()
plt.legend(loc='upper right')
plt.title('Error vs alpha')
plt.grid(True)
plt.show()




'''
df = pd.DataFrame(data={stringDay: ListErrro})
df.to_csv("./AlphaErrorFileH1.csv", sep=',', index=False)
df = pd.DataFrame(data={stringDay: ListCurre})
df.to_csv("./AlphaCurrentFileH1.csv", sep=',', index=False)

VarCsv = pd.read_csv("AlphaErrorFileH1.csv")
VarCsv[stringDay] = ListErrro
VarCsv.to_csv("./AlphaErrorFileH1.csv", sep=',', index=False)
VarCsv = pd.read_csv("AlphaCurrentFileH1.csv")
VarCsv[stringDay] = ListCurre
VarCsv.to_csv("./AlphaCurrentFileH1.csv", sep=',', index=False)
print(stringDay)
'''










'''


CurrFunVal = [0.0]*lenVectorA
ErrFunVal = [0.0]*lenVectorA
print(CurrFunVal)
print(lenVectorA)


GeneralValues = np.vstack((Alpha,CurrFunVal,ErrFunVal))
savetxt('GeneralFunctionV6G3.csv', GeneralValues, delimiter=',')

fig2,ax2 = plt.subplots()
plt.xlabel(" Aplha ")
plt.ylabel(" Error ")
plt.plot(Alpha, CurrFunVal ,color='blue',label='1 min sampling ')
plt.plot(Alpha, ErrFunVal ,color='blue',label='1 min sampling ')
plt.gcf().autofmt_xdate()
plt.legend(loc='upper right')
plt.title('Error vs alpha')
plt.grid(True)
plt.show()
'''





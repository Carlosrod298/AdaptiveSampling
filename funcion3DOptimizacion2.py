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
                meanValue = dataWindow['HAM'].mean()
                for i in range(dataWindow['HAM'].size):
                    DataValuesAM.append(meanValue)

    return float(mean_squared_error(Intel4['HAM'], DataValuesAM))




DefAdapt = 1
Def30min = 1
Def5min = 1

#Get Day
df = pd.read_json ('August6.json')
cdf = df[['fecha','ID','HAM','HSU']]
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
print(min(VarValues30M))
print(max(VarValues30M))
print( 1.0 / (30 * 60))  # minimal sampling interval hz
print( 1.0 / 60)  # max  sampling interval  hz

MaxError = 0.3
MaxCurrent = CCFun.MaxCompsuption()
print("MaxCurrent %f"%MaxCurrent)



'''
GenFunVal = [[0.0]*lenVectorA]*lenVectorB
for i in range(lenVectorA):
    for ii in range(lenVectorB):
        FSampling = getSampling(VarValues30M,Alpha[i],Beta[ii])
        Psample = [int(round(1 / (60 * x))) for x in FSampling]
        #add previus Sampling time
        Psampling  = [30]
        for x in Psample:
            Psampling.append(x)
        Psampling.pop()# Delete last sample
        Errorvector = (ErrorOnAdapt(Psampling,DateBase,Intel4))*1.0
        Consumptionvector = 0#[(CCFun.Compsuption(x)) for x in Psampling]
        meanConsumption  =0#((np.array(Consumptionvector)).mean())*1.0
        #print("Current %f Error %f" %(meanConsumption,Errorvector))
        GenFunVal[ii][i] =  (Errorvector) #(meanConsumption/MaxCurrent) +
        print("Alpha %f Beta %f Current %f Error %f  Gen %f " % (Alpha[i],Beta[ii],meanConsumption/MaxCurrent, Errorvector,GenFunVal[ii][i]))
    print(Alpha[i])
savetxt('GeneralFunctionV5E.csv', GenFunVal, delimiter=',')
'''
# Make data.
Alpha = np.arange(0, 0.3, 1e-3)
Beta =  np.arange(0,  7e-3,  0.1e-3)
lenVectorA = len(Alpha)
lenVectorB = len(Beta)

CurrFunVal = [0.0]*lenVectorA
ErrFunVal = [0.0]*lenVectorA
print(CurrFunVal)
print(lenVectorA)
for i in range(lenVectorA):
    FSampling = getSampling(VarValues30M,Alpha[i],0.4e-3)
    Psample = [int(round(1 / (60 * x))) for x in FSampling]
    #add previus Sampling time
    Psampling  = [30]
    for x in Psample:
        Psampling.append(x)
    Psampling.pop()# Delete last sample
    Errorvector = (ErrorOnAdapt(Psampling,DateBase,Intel4))
    Consumptionvector = [(CCFun.Compsuption(x)) for x in Psampling]
    meanConsumption  =((np.array(Consumptionvector)).mean())*1.0
    print("Current Alpha %f Current %f Error %f" %(Alpha[i],meanConsumption,Errorvector))
    CurrFunVal[i] =   (meanConsumption/MaxCurrent) #+(Errorvector)
    ErrFunVal[i]  = Errorvector

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
print(GenFunVal)
Alphax,Betay = np.meshgrid(Alpha,Beta)
GenArray = np.array(GenFunVal)
fig = plt.figure()
ax = fig.gca(projection='3d')
# Plot the surface.
surf = ax.plot_surface(Alpha, Beta, GenArray, cmap=cm.coolwarm,linewidth=0, antialiased=False)
# Customize the z axis.
ax.set_xlabel('Alpha')
ax.set_ylabel('Beta')
ax.set_zlabel('Function')
#ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()
'''



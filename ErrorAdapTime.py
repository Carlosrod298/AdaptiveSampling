# ReadDay.py>
import pandas as pd
from sklearn.metrics import mean_squared_error

def Error(pSampling, dataDay):
    # Adaptable Time
    DateBase = dataDay.index[0]
    DataValuesAM = list()
    minutesTotal = 30
    counter = 0
    errorLst = list()
    for adapTime in pSampling:
        baseMinutes = counter * 30
        counter = counter + 1
        for i in range(0, minutesTotal, adapTime):
            InitialMin = baseMinutes + i
            finMin = baseMinutes + i + adapTime - 1
            if (finMin > (baseMinutes + minutesTotal)):
                finMin = baseMinutes + minutesTotal - 1
            InitialHour = DateBase + pd.Timedelta('00:' + str(InitialMin).zfill(2) + ':00')
            FinalHour = DateBase + pd.Timedelta('00:' + str(finMin).zfill(2) + ':59')
            dataHour = dataDay.loc[
                       InitialHour.strftime("%Y-%m-%d %H:%M:%S"): FinalHour.strftime("%Y-%m-%d %H:%M:%S")]
            # print("Range " + InitialHour.strftime("%Y-%m-%d %H:%M:%S") +" "+ FinalHour.strftime("%Y-%m-%d %H:%M:%S"))
            if (dataHour.index.size > 0):
                meanValue = dataHour.valor.mean()
                errorLst.clear()
                for i in range(dataHour.valor.size):
                    DataValuesAM.append(meanValue)
    return mean_squared_error(dataDay.valor, DataValuesAM) * 100

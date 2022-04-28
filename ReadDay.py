# ReadDay.py>
import pandas as pd


# function
def SelectDay2019(month, day):
    TempData = pd.read_csv("Data2019.csv")
    timeDataSet = {}
    timeDataSet['NewDateTime'] = pd.to_datetime(TempData['fechaDato'], unit='s')
    TempData.index = timeDataSet['NewDateTime']
    TempData.index = TempData.index - pd.Timedelta('05:00:00')  # Set Timezone
    TempData.drop(columns=['fechaDato'])
    stringDay = '2019-'+str(month).zfill(2)+'-'+ str(day).zfill(2) + ' '
    DataOneDay = TempData.loc[stringDay + '00': stringDay + '23:59']
    if(DataOneDay.index.size >0):
        return DataOneDay
        #DataOneDay.to_csv('DataOneDay.csv', float_format='%.2f', index=False)  # rounded to two decimals
    else:
        print("Error importing data")
        return "Error"



def getSampling(Beta,Alpha):
    def NormalizedValue(hour, minute):
        if (minute < 30):
            minutemin = str(hour).zfill(2) + ":00:00"
            minutemax = str(hour).zfill(2) + ":29:59"
        else:
            minutemin = str(hour).zfill(2) + ":30:00"
            minutemax = str(hour).zfill(2) + ":59:59"
        #  Get the sampling interval in variance file
        dataH = df.loc[DateBase + minutemin: DateBase + minutemax]
        return dataH.iat[0, 0]
    # Read results from AnalsysVar
    df = pd.read_csv("VarNormalFile.csv")
    timeDataSet = {}
    # Convert field fechaDato to date time
    timeDataSet['NewDateTime'] = pd.to_datetime(df['Time'])
    df.index = timeDataSet['NewDateTime']
    df = df.drop(columns=['Time'])
    DateBase = df.index[0].strftime("%Y-%m-%d ")
    FSmin = 1.0 / (30 * 60)  # minimal sampling interval hz
    FSmax = 1.0 / 60  # max  sampling interval  hz
    #print("min: " + str(FSmin) + " max: " + str(FSmax) + " intervalos de muestro en HZ")
    #print("min: " + str(1 / FSmax) + " max: " + str(1 / FSmin) + " intervalos de muestreo en segundos")
    minutesTotal = 60 * 24
    VectorVar = list()  # Variance Vector
    # create vector dates over 24 hours
    for i in range(0, minutesTotal, 30):
        InitialHour = pd.to_datetime(DateBase, infer_datetime_format=True) + pd.Timedelta(
            '00:' + str(i).zfill(2) + ':00')
        VectorVar.append(NormalizedValue(InitialHour.hour, InitialHour.minute))
    FSampling = list()

    for variance in VectorVar:
        FS = variance * Beta * FSmax + Alpha
        if (FS < FSmin):
            FS = FSmin
        FSampling.append(FS)
    #FSamplingTime = [FSampling,]
    return pd.DataFrame(FSampling,index =df.index,columns =['FSampling'])
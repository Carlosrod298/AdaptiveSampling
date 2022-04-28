from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import pandas as pd
import csv



from sklearn.metrics import mean_squared_error

print("Analysis Variance")
df  = pd.read_csv("VarFile.csv")
# take a look at the dataset
print("head csv file")
print(df.head(3))
# summarize the data
print(df.shape)
print(df.describe())

timeDataSet = {}
# Convert field fechaDato to date time
timeDataSet['NewDateTime'] = pd.to_datetime(df['Time'])
#print(timeDataSet)
df.index = timeDataSet['NewDateTime']

Day1 = df[df.columns[1]]
Day2 = df[df.columns[2]]
Day3 = df[df.columns[3]]
Day4 = df[df.columns[4]]
Day5 = df[df.columns[5]]
Day6 = df[df.columns[6]]


sumVar = df.drop(columns=['Time'])
print ("Max Value on Day %2.3f"%Day1.max())
sumVar = sumVar.sum(axis = 1, skipna = True)
NormalizedVar= sumVar.div(sumVar.max())
NormalizedVar.to_csv("./VarNormalFile.csv", sep=',',index=True)


fig1 = plt.figure(1)
#Variance
plt.xlabel("Time")
plt.ylabel("Variance")
plt.plot(df.index, Day1.values,  color='red',    label='2019-10-25')
plt.plot(df.index, Day2.values,  color='orange', label='2019-10-28')
plt.plot(df.index, Day3.values,  color='yellow', label='2019-10-30')
plt.plot(df.index, Day4.values,  color='blue',   label='2019-10-31')
plt.plot(df.index, Day5.values,  color='yellow', label='2019-11-04')
plt.plot(df.index, Day6.values,  color='blue',   label='2019-11-08')
plt.plot(df.index, sumVar.values,  color='pink',   label='Sum Values')
#plt.xlim(XminValue, XmaxValue)
plt.gcf().autofmt_xdate()
plt.legend(loc='upper right')
plt.grid(True)
fig1.show()

fig2 = plt.figure(2)
plt.xlabel("Time")
plt.ylabel("normalized Variance")
plt.plot(NormalizedVar.index, NormalizedVar.values,  color='black',label='Sum Variance')
plt.gcf().autofmt_xdate()
plt.legend(loc='upper right')
plt.grid(True)
plt.show()
plt.show()




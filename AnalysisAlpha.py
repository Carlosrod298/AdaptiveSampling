from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statistics import mean
import csv



from sklearn.metrics import mean_squared_error

color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                  '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                  '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                  '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5',
                  '#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                  '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5']


print("Analysis Variance")
dfError  = pd.read_csv("AlphaErrorFileH1.csv")
dfCurr  = pd.read_csv("AlphaCurrentFileH1.csv")
# take a look at the dataset
print("head csv file")

# Convert field fechaDato to date time
Alpha = np.arange(0, 0.1, 1e-3)
Dates = list()
minValues = list()

print(dfError.columns.size)


plt.rcParams.update({'font.size': 16})
dayError = (dfError[dfError.columns[0]])/3.4
dayCurrent = (dfCurr[dfCurr.columns[0]])/42
sumFun = dayError + dayCurrent
minElement = min(sumFun)#np.amin(sumFun)
print("Minimal Value: ")
print(minElement)
index_min = np.where(sumFun == minElement)
AlphaSel = Alpha[index_min[0][0]]
fig0,ax0 = plt.subplots(figsize=(20, 10))
plt.xlabel("Alpha")
plt.ylabel(" Normalized Data")
plt.plot(Alpha, dayError, color='blue',label='MSE')
plt.plot(Alpha, dayCurrent, color='red',label='Current Comsuption')
plt.plot(Alpha, sumFun, color='green',label='MSE + Current')
plt.vlines(AlphaSel, 0, 1.75, colors='k', linestyles='solid',label='Alpha Selected  %2.4f'%AlphaSel)
plt.gcf().autofmt_xdate()
plt.legend(loc='upper right')
plt.title(' Analysis Alpha For One Day ')
plt.grid(True)
#fig0.savefig("images/OneDayAlpha.png")
fig0.show()




#Variance
fig1,ax1 = plt.subplots(figsize=(20, 10))
plt.xlabel("Alpha")
plt.ylabel(" %RH²")
for x in range(dfError.columns.size):
    print(x)
    dayS = dfError[dfError.columns[x]]
    #print(dayS.values)
    plt.plot(Alpha, dayS.values, color=color_sequence[x])
#plt.xlim(XminValue, XmaxValue)
plt.gcf().autofmt_xdate()
plt.title(' Alpha vs Mean Squared Error for day ')
#plt.legend(loc='upper right')
plt.grid(True)
fig1.show()


#Variance
fig2,ax2 = plt.subplots(figsize=(20, 10))
plt.xlabel("Alpha")
plt.ylabel("uA")
for x in range(dfCurr.columns.size):
    print(x)
    dayS = dfCurr[dfCurr.columns[x]]
    #print(dayS.values)
    plt.plot(Alpha, dayS.values, color=color_sequence[x])
plt.title(' Alpha vs Current For Day ')
plt.gcf().autofmt_xdate()
plt.grid(True)
fig2.show()

print("Dates")
Dates = dfCurr.columns
print(Dates)
XminPos = list()
minCurrL = list()
minErroL = list()
fig4,ax4 = plt.subplots(figsize=(20, 10))
plt.xlabel("Alpha")
plt.ylabel("Error + Current Normalized")
for x in range(dfCurr.columns.size):
    #normalized values
    #print(dfError[dfError.columns[x]])
    Error2D =   ((dfError[dfError.columns[x]]).to_numpy())/3.301547877175522
    Current2D = ((dfCurr[dfCurr.columns[x]]).to_numpy())/41.46694453703704
    # sum arrays
    sumFun = Error2D + Current2D
    minElement = min(sumFun)#np.amin(sumFun)
    print("Minimal Value: ")
    print(minElement)
    index_min = np.where(sumFun == minElement)
    AlphaSel = Alpha[index_min[0][0]]
    XminPos.append(AlphaSel)
    minCurrL.append(Current2D[index_min[0][0]])
    minErroL.append(Error2D[index_min[0][0]])
    plt.plot(Alpha, sumFun, color=color_sequence[x])
    plt.vlines(AlphaSel, 0, 1.75, colors='k', linestyles='solid')
plt.gcf().autofmt_xdate()
plt.title(' Alpha vs General Function For Day ')
plt.grid(True)
fig4.show()

xminMean = mean(XminPos)
print(xminMean)

fig3,ax3 = plt.subplots(figsize=(20, 10))
plt.xlabel("Time (Days)")
plt.ylabel("Alpha")
plt.scatter(Dates,XminPos,color='blue' )
plt.hlines(xminMean,Dates[0],Dates[-1],color='red' ,label=' Mean Alpha %2.4f'%xminMean)
plt.title(' Best Alpha Selected for day ')
plt.legend(loc='lower right')
plt.gcf().autofmt_xdate()
plt.grid(True)
plt.show()



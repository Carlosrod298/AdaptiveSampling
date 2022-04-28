from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statistics import mean
from matplotlib.dates import DateFormatter
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
plt.xlabel(r'$ \alpha $')
plt.ylabel(" Normalized Data")
plt.plot(Alpha, dayError, color='blue',label='MSE')
plt.plot(Alpha, dayCurrent, color='red',label='Current Comsuption')
plt.plot(Alpha, sumFun, color='green',label='MSE + Current')
plt.vlines(AlphaSel, 0, 1.75, colors='k', linestyles='solid',label='Alpha Selected  %2.4f'%AlphaSel)
plt.gcf().autofmt_xdate()
plt.legend(loc='upper right')
plt.title(' Analysis '+r'$ \alpha $'+' For One Day ')
plt.grid(True)
#fig0.savefig("images/OneDayAlpha.png")
fig0.show()




#Variance
fig1,ax1 = plt.subplots(2,figsize=(20, 10))
plt.xlabel(r'$ \alpha $')
ax1[0].set( ylabel='MSE %RH²')
for x in range(dfError.columns.size):
    print(x)
    dayS = dfError[dfError.columns[x]]
    #print(dayS.values)
    ax1[0].plot(Alpha, dayS.values, color=color_sequence[x])
#plt.xlim(XminValue, XmaxValue)
ax1[0].grid(True)
fig1.suptitle(r'$ \alpha $'+' vs Mean Squared Error for day ')
#plt.legend(loc='upper right')

plt.xlabel(r'$ \alpha $'+' in 20 days selected')
ax1[1].set( ylabel='Current uA')
for x in range(dfCurr.columns.size):
    print(x)
    dayS = dfCurr[dfCurr.columns[x]]
    #print(dayS.values)
    ax1[1].plot(Alpha, dayS.values, color=color_sequence[x])
plt.title(r'$ \alpha $'+' vs Current For Day ')
plt.gcf().autofmt_xdate()
ax1[1].grid(True)
fig1.savefig("images/AlphaCurrentError.png")
fig1.show()


print("Dates")
Dates = dfCurr.columns
print(Dates)
XminPos = list()
minCurrL = list()
minErroL = list()


fig4,ax4 = plt.subplots(2,figsize=(20, 10))
plt.xlabel(r'$ \alpha $')
ax4[0].set(ylabel="Error + Current Normalized")
for x in range(dfCurr.columns.size):
    #normalized values
    #print(dfError[dfError.columns[x]])
    Error2D =   ((dfError[dfError.columns[x]]).to_numpy())/3.301547877175522
    Current2D = ((dfCurr[dfCurr.columns[x]]).to_numpy())/41.46694453703704
    # sum arrays
    sumFun = Error2D + Current2D
    minElement = min(sumFun)#np.amin(sumFun)
    #print("Minimal Value: ")
    #print(minElement)
    index_min = np.where(sumFun == minElement)
    AlphaSel = Alpha[index_min[0][0]]
    XminPos.append(AlphaSel)
    minCurrL.append(Current2D[index_min[0][0]])
    minErroL.append(Error2D[index_min[0][0]])
    ax4[0].plot(Alpha, sumFun, color=color_sequence[x])
    ax4[0].vlines(AlphaSel, 0, 1.75, colors='k', linestyles='solid')
plt.gcf().autofmt_xdate()
fig4.suptitle(r'$ \alpha $'+' vs General Function For Day ')
ax4[0].grid(True)

xminMean = mean(XminPos)
print(xminMean)
plt.xlabel("Time (Days)")
ax4[1].set(ylabel=r'$ \alpha $')
ax4[1].scatter(Dates,XminPos,color='blue' )
ax4[1].hlines(xminMean,Dates[0],Dates[-1],color='red' ,label=' Mean Alpha %2.4f'%xminMean)
plt.title(' Best '+r'$ \alpha $'+' Selected for day ')
ax4[1].legend(loc='upper right')
plt.gcf().autofmt_xdate()
date_form = DateFormatter(" %d")
ax4[1].xaxis.set_major_formatter(date_form)
ax4[1].grid(True)
#fig4.savefig("images/AlphaSelect.png")
plt.show()


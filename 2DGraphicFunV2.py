import pandas as pd
import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plt
from numpy import loadtxt
from mpl_toolkits import mplot3d




print("Intel Analysis")
df = pd.read_csv('GeneralCurrentFileH1.csv')
df1 = pd.read_csv('GeneralErrorFileH1.csv')


#Version 6
Alpha = np.arange(0, 0.1, 1e-3)
Beta =  np.arange(0,  10e-3,  0.1e-3)
GenFunCurrent = df
GenFunError = df1
GenFunCurrent  = GenFunCurrent/41.46694453703704
GenFunError = GenFunError/3.301547877175522
GenFunT = GenFunCurrent + GenFunError
print(GenFunT.shape)

#df[df.columns[1]]
Error2D = (GenFunError.iloc[0]).to_numpy()
Current2D = (GenFunCurrent.iloc[0]).to_numpy()
sumFun = Error2D + Current2D
minElement = np.amin(sumFun)
print(min(sumFun))
print(minElement)
index_min = np.where(sumFun == minElement)
print(index_min)
XminPos = Alpha[index_min[0]]
minCurr  = Current2D[index_min]
minError = Error2D[index_min]

print("Alpha Value %f index min %d"%(XminPos,index_min[0]))

plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(20, 10))
#plt.subplots()
plt.xlabel(" Alpha ")
plt.ylabel(" Normalized Value ")
plt.plot(Alpha,Current2D, color='red',label=' Current normalized ')
plt.plot(Alpha,Error2D, color='blue',label=' Error  normalized')
plt.plot(Alpha,sumFun, color='green',label=' Sum of variables ')
plt.vlines(XminPos, 0, 1.75, colors='k', linestyles='solid', label='Alpha %f Error %f Current %f'%(XminPos,minError,minCurr))
plt.legend(loc='upper right')
plt.title('Alpha Analysis 12 August')
plt.grid(True)
#plt.tight_layout()
plt.show()
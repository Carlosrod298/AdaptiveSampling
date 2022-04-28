import pandas as pd
import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plt
from numpy import loadtxt


GenFun  = loadtxt('GeneralFunctionV6G.csv', delimiter = ",")

Alpha      = GenFun[0,:]
CurrFun    = GenFun[1,:]
ErrorFun   = GenFun[2,:]
sumFun = CurrFun+ErrorFun
minElement = np.amin(sumFun)
print(min(sumFun))
print(minElement)
print(sumFun)
index_min = np.where(sumFun == minElement)
print(index_min)
XminPos = Alpha[index_min[0]]
minCurr  = CurrFun[index_min]
minError = ErrorFun[index_min]
ErrrMax = np.max(ErrorFun)
ErrorFun = ErrorFun/ErrrMax
print("Alpha Value %f index min %d"%(XminPos,index_min[0]))

fig2 = plt.subplots()
plt.xlabel(" Alpha ")
plt.ylabel(" Normalized Value ")
plt.plot(Alpha,CurrFun, color='red',label=' Current normalized ')
plt.plot(Alpha,ErrorFun, color='blue',label=' Error  normalized')
plt.plot(Alpha,sumFun, color='green',label=' Sum of variables ')
plt.vlines(XminPos, 0, 1.75, colors='k', linestyles='solid', label='Alpha %f Error %f Current %f'%(XminPos,minError,minCurr))
plt.legend(loc='upper right')
plt.title('Alpha Analysis 12 August')
plt.grid(True)
#plt.tight_layout()
plt.show()



GenFun  = loadtxt('GeneralFunctionV6G1.csv', delimiter = ",")
Alpha      = GenFun[0,:]
CurrFun    = GenFun[1,:]
ErrorFun   = GenFun[2,:]
sumFun = CurrFun+ErrorFun
index_min = np.argmin(sumFun)
XminPos = Alpha[index_min]
minCurr  = CurrFun[index_min]
minError = ErrorFun[index_min]
ErrrMax = np.max(ErrorFun)
ErrorFun = ErrorFun/ErrrMax
print("Alpha Value %f index min %f"%(XminPos,index_min))

fig3,ax3 = plt.subplots()
plt.xlabel(" Alpha ")
plt.ylabel(" Normalized Value ")
plt.plot(Alpha,CurrFun, color='red',label=' Current normalized ')
plt.plot(Alpha,ErrorFun, color='blue',label=' Error  normalized')
plt.plot(Alpha,sumFun, color='green',label=' Sum of variables ')
plt.vlines(XminPos, 0, 1.75, colors='k', linestyles='solid', label='Alpha %f Error %f Current %f'%(XminPos,minError,minCurr))
plt.legend(loc='upper right')
plt.title('Alpha Analysis 20 August')
plt.grid(True)
plt.tight_layout()
fig3.show()


GenFun  = loadtxt('GeneralFunctionV6G2.csv', delimiter = ",")
Alpha      = GenFun[0,:]
CurrFun    = GenFun[1,:]
ErrorFun   = GenFun[2,:]
sumFun = CurrFun+ErrorFun
index_min = np.argmin(sumFun)
XminPos = Alpha[index_min]
minCurr  = CurrFun[index_min]
minError = ErrorFun[index_min]
ErrrMax = np.max(ErrorFun)
ErrorFun = ErrorFun/ErrrMax
print("Alpha Value %f index min %f"%(XminPos,index_min))

fig4,ax4 = plt.subplots()
plt.xlabel(" Alpha ")
plt.ylabel(" Normalized Value ")
plt.plot(Alpha,CurrFun, color='red',label=' Current normalized ')
plt.plot(Alpha,ErrorFun, color='blue',label=' Error  normalized')
plt.plot(Alpha,sumFun, color='green',label=' Sum of variables ')
plt.vlines(XminPos, 0, 1.75, colors='k', linestyles='solid', label='Alpha %f Error %f Current %f'%(XminPos,minError,minCurr))
plt.legend(loc='upper right')
plt.title('Alpha Analysis 11 August')
plt.grid(True)
plt.tight_layout()
fig4.show()


GenFun  = loadtxt('GeneralFunctionV6G3.csv', delimiter = ",")
Alpha      = GenFun[0,:]
CurrFun    = GenFun[1,:]
ErrorFun   = GenFun[2,:]
sumFun = CurrFun+ErrorFun
index_min = np.argmin(sumFun)
XminPos = Alpha[index_min]
minCurr  = CurrFun[index_min]
minError = ErrorFun[index_min]
ErrrMax = np.max(ErrorFun)
ErrorFun = ErrorFun/ErrrMax
print("Alpha Value %f index min %f"%(XminPos,index_min))

fig5,ax5 = plt.subplots()
plt.xlabel(" Alpha ")
plt.ylabel(" Normalized Value ")
plt.plot(Alpha,CurrFun, color='red',label=' Current normalized ')
plt.plot(Alpha,ErrorFun, color='blue',label=' Error  normalized')
plt.plot(Alpha,sumFun, color='green',label=' Sum of variables ')
plt.vlines(XminPos, 0, 1.75, colors='k', linestyles='solid', label='Alpha %f Error %f Current %f'%(XminPos,minError,minCurr))
plt.legend(loc='upper right')
plt.title('Alpha Analysis 6 August')
plt.grid(True)
plt.tight_layout()
plt.show()
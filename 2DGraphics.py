import pandas as pd
import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plt
from numpy import loadtxt

from mpl_toolkits import mplot3d



GenFun  = loadtxt('GeneralFunctionV4E.csv', delimiter = ",")
GenFun1 = loadtxt('GeneralFunctionV4C.csv', delimiter = ",")

ErrorFun    = GenFun[0,:]
CurrentFun  = GenFun1[0,:]

ErrrMax = np.max(ErrorFun)
ErrorFun = ErrorFun/ErrrMax
print()

#Version 4  alpha and  Beta data
Alpha = np.arange(0, 3, 10e-3)
Beta =  np.arange(0,  7e-3,  0.1e-3)

fun2 = (8.0 * ErrorFun)


print(fun2[0:3])
fig2,ax2 = plt.subplots()
plt.xlabel(" Beta ")
plt.ylabel(" Error ")
plt.plot(Alpha,ErrorFun, color='red',label=' Error ')
plt.plot(Alpha,CurrentFun, color='blue',label=' Error ')
plt.plot(Alpha,fun2, color='green',label=' Error ')
#ax2.ylim(0, 1.5)
plt.title('Optimization')
plt.grid(True)
fig2.show()




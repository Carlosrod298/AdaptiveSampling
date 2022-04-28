import pandas as pd
import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plt
from numpy import loadtxt

from mpl_toolkits import mplot3d



GenFun  = loadtxt('GeneralFunctionV4E.csv', delimiter = ",")
GenFun1 = loadtxt('GeneralFunctionV4C.csv', delimiter = ",")
#GenFun2 = loadtxt('GeneralFunctionV1C.csv', delimiter = ",")

GenFun2 = GenFun*1000
# Hasta la version 3
#Alpha = np.arange(0, 400e-3, 10e-3)
#Beta =  np.arange(0,  32e-3,  0.5e-3)

#Version 4
Alpha = np.arange(0, 3, 10e-3)
Beta =  np.arange(0,  7e-3,  0.1e-3)

#Alpha = np.arange(0, 200e-3, 10e-3)
#Beta =  np.arange(0,  16e-3,  1e-3)
Alphax,Betay = np.meshgrid(Alpha,Beta)
print(GenFun.shape)
print(Alphax.shape)
print(Betay.shape)


fig1 = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(Alphax, Betay, GenFun,cmap='viridis', edgecolor='none')
ax.set_xlabel('Alpha')
ax.set_ylabel('Beta')
ax.set_zlabel('Function')
ax.set_title('Error Function')
fig1.show()




fig2 = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(Alphax, Betay, GenFun1,cmap='viridis', edgecolor='none')
ax.set_xlabel('Alpha')
ax.set_ylabel('Beta')
ax.set_zlabel('Function')
ax.set_title('Current Function')
plt.show()

#Normal Data
'''
fig2,ax2 = plt.subplots()
plt.xlabel("Day " +" (Hours)")
plt.ylabel(" Temperature °c ")
plt.plot(DataOneDay.index, DataOneDay.valor, color='red',label='Temperature minuntes ')
plt.plot(Time5M, DataOneDay5M,'-.',  color='orange', label='T° 5 Min error: %2.2f'%error5M)
plt.plot(Time15M, DataOneDay15M,'-.',  color='blue', label='T° 15 Min error: %2.2f'%error15M)
plt.plot(Time30M, DataOneDay30M,'-.',  color='gray', label='T° 30 Min error: %2.2f'%error30M)
plt.plot(TimeH, DataOneDayH,'-.',  color='black', label='T° Hour error: %2.2f'%errorH)
plt.gcf().autofmt_xdate()
plt.legend(loc='upper right')
plt.title('Temperature curve at different Sampling period')
plt.grid(True)
plt.show()
'''




'''
fig2 = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(Alphax, Betay, GenFun1,cmap='viridis', edgecolor='none')
ax.set_xlabel('Alpha')
ax.set_ylabel('Beta')
ax.set_zlabel('Function')
ax.set_title('General Function')
fig2.show()

fig3 = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(Alphax, Betay, GenFun2,cmap='viridis', edgecolor='none')
ax.set_xlabel('Alpha')
ax.set_ylabel('Beta')
ax.set_zlabel('Function')
ax.set_title('General Function')
plt.show()
'''



'''
fig = plt.figure(figsize=(6, 3.2))
ax = fig.add_subplot(111)
ax.set_title('colorMap')
plt.imshow(GenFun)
ax.set_aspect('equal')
plt.colorbar(orientation='vertical')
plt.show()
'''
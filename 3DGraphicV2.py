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
Alphax,Betay = np.meshgrid(Alpha,Beta)
GenFunCurrent = df
GenFunError = df1
GenFunCurrent  = GenFunCurrent/41.46694453703704
GenFunError = GenFunError/3.301547877175522
GenFunT = GenFunCurrent + GenFunError
print(GenFunT.shape)
print(Alphax.shape)
print(Betay.shape)





plt.rcParams.update({'font.size': 16})
fig1 = plt.figure(figsize=(20, 10))
ax = fig1.add_subplot(111, projection='3d')
ax.plot_surface(Alphax, Betay, GenFunCurrent,cmap='viridis',rstride=4, cstride=4)
ax.set_xlabel(r'$ \alpha $')
ax.set_ylabel(r'$ \beta $')
ax.set_zlabel('Current Normalized')
ax.set_title('Current Function')
#fig1.savefig("images/CurrentVar3D.png")
fig1.show()

fig2 = plt.figure(figsize=(30, 10))
ax = fig2.add_subplot(111, projection='3d')
ax.plot_surface(Alphax, Betay, GenFunError,cmap='viridis',rstride=4, cstride=4)
ax.set_xlabel(r'$ \alpha $')
ax.set_ylabel(r'$ \beta $')
ax.set_zlabel('MSE Normalized ')
ax.set_title('MSE Normalized Function')
#fig2.savefig("images/ErrorGraph3D.png")
fig2.show()

fig3 = plt.figure(figsize=(20, 10))
ax = fig3.add_subplot(111, projection='3d')
ax.plot_surface(Alphax, Betay, GenFunT,cmap='viridis',rstride=4, cstride=4)
ax.set_xlabel(r'$ \alpha $')
ax.set_ylabel(r'$ \beta $')
ax.set_zlabel('Function')
ax.set_title('Sum  Function')
plt.show()


#//////////////////////////////////////
#
# Script to graphics from csv files
# Intel Tags
#
# Carlos David Rodriguez
#

#Import Data on Json intel
#Intel: http://76.74.150.54:8092/ws_iot-agro/GetIntel/?anio=2020&mes=2&dia=1
#Libelium: http://76.74.150.54:8092/ws_iot-agro/GetLibelium/?anio=2020&mes=6&dia=1
#Omicron http://76.74.150.54:8092/ws_iot-agro/GetOmicron/?anio=2020&mes=6&dia=4

from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import pandas as pd
import pylab as pl
import numpy as np
#%matplotlib inline
import time
import datetime

print("Intel Analysis")
print("Reading csv files")
df = pd.read_csv('IN_01_T_006-Junio2020.csv')
# take a look at the dataset
print("head csv file")
print(df.head(1))
# summarize the data
print(df.shape)
print(df.describe())
#Lets select some features to explore more.
cdf = df[['fechaDato','idVariable','bateria','bateria_voltios','valor']]
print(cdf.head(4))
# get only temperature, humidity and light
#HumeData = cdf.iloc[2::4]
HumeData = cdf.iloc[2::4]
TempData = cdf.iloc[1::4]
LightData = cdf.iloc[0::4]

TemperatureVal = TempData[['fechaDato', 'bateria_voltios', 'valor', 'bateria']]
timeDataSet = {}
timeDataSet['NewDateTime'] = pd.to_datetime(TemperatureVal['fechaDato'], unit='s')
TemperatureVal.index = timeDataSet['NewDateTime']
print(TemperatureVal.shape)
df_p = TemperatureVal.resample('H').mean()
print(df_p.shape)
print(df_p.head(10))

host = host_subplot(111, axes_class=AA.Axes)
plt.subplots_adjust(right=0.75)
par1 = host.twinx()
par2 = host.twinx()
offset = 60
new_fixed_axis = par2.get_grid_helper().new_fixed_axis
par2.axis["right"] = new_fixed_axis(loc="right", axes=par2,
                                       offset=(offset, 0))
offset = 10
new_fixed_axis = par1.get_grid_helper().new_fixed_axis
par1.axis["right"] = new_fixed_axis(loc="right", axes=par1,
                                       offset=(offset, 0))
par2.axis["right"].toggle(all=True)
host.set_ylim(0, 100)
host.set_xlabel("Time")
host.set_ylabel("Battery")
par1.set_ylabel("Temperature")
par2.set_ylabel("Volts")
p1, = host.plot(df_p.index, df_p.bateria, label="Battery Level")
p2, = par1.plot(df_p.index, df_p.valor, label="Temperature")
p3, = par2.plot(df_p.index, df_p.bateria_voltios, label="Battery Volts")
par1.set_ylim(0, 40)
par2.set_ylim(2.5, 3.1)
host.legend()
host.axis["left"].label.set_color(p1.get_color())
par1.axis["right"].label.set_color(p2.get_color())
par2.axis["right"].label.set_color(p3.get_color())
plt.draw()
plt.show()
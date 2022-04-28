from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import pandas as pd
import pylab as pl
import numpy as np
from matplotlib.dates import DateFormatter
#%matplotlib inline
import time
import datetime



# Ble
sampling = np.arange(1,31)
print(sampling)
# Zigbee
Ism = 21000     #uA State machine
Isn = 17000     #uA read sensors
It  = 22000     #uA transmision
Ir  = 24000     #uA reception
Igs = 17000     #uA go to sleep
Isl = 20        #uA Sleep Mode
#  times
smT = 7     #ms state machine time
snT = 5     #ms read sensors
txT = 12    #ms tx time
rxT = 20  #ms rx time
gsT = 2     #ms go to sleep time
TimesUpdate = 2
slT = ((60000-(TimesUpdate * smT)-snT)*sampling) - (txT +rxT+gsT)

CurrentAvg = ((TimesUpdate*smT*Ism*sampling)+(Isn*snT*sampling)+(It*txT)+(Ir*rxT*sampling)+(Isl*slT)+(Igs*gsT))/(60000*sampling)

print(CurrentAvg)

plt.rcParams.update({'font.size': 16})
fig1, ax1 = plt.subplots()
plt.scatter(sampling, CurrentAvg, color='red')
ax1.xaxis.set_major_locator(plt.MaxNLocator(32))
#plt.gcf().autofmt_xdate()
#date_form = DateFormatter("%M-%S")
#ax1.xaxis.set_major_formatter(date_form)
plt.title('Current Consumption Analysis')
plt.xlabel('Sampling time (Minutes)')
plt.ylabel('Device Current Consumption (uA)')
plt.grid(True)
fig1.show()

cr2434 = ((320/(CurrentAvg/1000))*0.7)/24
cr2450 = ((620/(CurrentAvg/1000))*0.7)/24
AAA = ((1200/(CurrentAvg/1000))*0.7)/24

fig2, ax2 = plt.subplots()
plt.plot(sampling, cr2434, color='red',label='CR2434 Battery ')
plt.plot(sampling, cr2450, color='blue',label='CR2450 Battery ')
plt.plot(sampling, AAA, color='green',label='AAA Battery ')
ax2.xaxis.set_major_locator(plt.MaxNLocator(32))
#plt.gcf().autofmt_xdate()
#date_form = DateFormatter("%M-%S")
#ax1.xaxis.set_major_formatter(date_form)
plt.title('Estimated Life of The Device')
plt.xlabel('Sampling time (Minutes)')
plt.ylabel('Device life (days)')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()


from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.dates import DateFormatter
import csv



from sklearn.metrics import mean_squared_error

print("Analysis Variance")
df  = pd.read_csv("VarFileH1.csv")
# take a look at the dataset
print("head csv file")
print(df.head(3))
# summarize the data
print(df.shape)
print(df.describe())


# Convert field fechaDato to date time
df.index = pd.to_datetime(df['Time'])
hours  = np.arange(0, 24, 0.5)
print(hours)
Day1 = df[df.columns[1]]
Day2 = df[df.columns[2]]
Day3 = df[df.columns[3]]
Day4 = df[df.columns[4]]
Day5 = df[df.columns[5]]
Day6 = df[df.columns[6]]

print(df.columns.size)


plt.rcParams.update({'font.size': 12})
fig1,ax1 = plt.subplots(figsize=(20, 10))
plt.xlabel("Time (hours)")
plt.ylabel(" %RH²")
for x in range(1,df.columns.size):
    print(x)
    dayS = df[df.columns[x]]
    print(dayS.values)
    plt.scatter(df['Time'],dayS.values,color='blue' )
#plt.legend(loc='lower right')
plt.gcf().autofmt_xdate()
ax1.xaxis.set_major_locator(plt.MaxNLocator(24))
plt.title('Variance distribution for selected days')
plt.grid(True)
#fig1.savefig("images/ScattVar.png")
plt.show()



'''
plt.plot(df.index, Day1.values,  color='red',    label='2019-08-05')
plt.plot(df.index, Day2.values,  color='orange', label='2019-08-06')
plt.plot(df.index, Day3.values,  color='yellow', label='2019-08-07')
plt.plot(df.index, Day4.values,  color='blue',   label='2019-08-08')
plt.plot(df.index, Day5.values,  color='yellow', label='2019-08-09')
plt.plot(df.index, Day6.values,  color='blue',   label='2019-08-10')
'''


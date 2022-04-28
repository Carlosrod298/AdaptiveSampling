
import matplotlib.pyplot as plt
import numpy as np
import ReadDay
import ErrorAdapTime


BetaValues  = np.arange(0.1,2,0.1)
errorBeta = list()
Comsuption = list()
ModelComsuption = [-8.88320120e-41,  1.25194234e-36, -7.98659985e-33,  3.04992176e-29
                   -7.76952077e-26,  1.39274592e-22, -1.80597252e-19,  1.71489854e-16
                   -1.19386793e-13,  6.04167398e-11, -2.18151681e-08,  5.44985166e-06
                   -8.98245742e-04,  9.07840326e-02, -5.00439449e+00,  1.81722760e+02]
Predic = np.poly1d(ModelComsuption)

for x in BetaValues :
    # calling functions
    FSamplingTime = ReadDay.getSampling(x)
    FSampling = FSamplingTime.FSampling
    Psampling = [int(round(1 / (60 * x))) for x in FSampling]
    print("Sampling: " ,Psampling)
    PredicValues = Predic(Psampling*60)
    print("Current: ",np.average(PredicValues))
    Comsuption.append(np.average(PredicValues))
    DataOneDay = ReadDay.SelectDay2019(10, 25)
    ErrorAdTime = ErrorAdapTime.Error(Psampling,DataOneDay)
    errorBeta.append(ErrorAdTime)

#Variance
fig1 = plt.figure(1)
plt.subplot(211)
plt.xlabel("Beta Values")
plt.ylabel("Error")
plt.plot(BetaValues, errorBeta,  color='purple',label='Beta Vs Error')
plt.gcf().autofmt_xdate()
plt.legend(loc='upper right')
plt.grid(True)
#
plt.subplot(212)
plt.xlabel("Time")
plt.ylabel("s")
plt.plot(BetaValues, Comsuption,  color='green',label='Beta Vs Current')
plt.gcf().autofmt_xdate()
plt.legend(loc='lower right')
plt.grid(True)
plt.show()
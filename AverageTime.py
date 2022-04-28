
import datetime as dt
import numpy as np

def calc_hravg(X):
    """Calculates hourly average from input data"""
    X_hr = []
    minX = X[:,0].min()
    hr = dt.datetime(*minX.timetuple()[0:4])
    while hr <= dt.datetime(*X[-1,0].timetuple()[0:4]):
        nhr = hr + dt.timedelta(hours=1)
        ind = np.where( (X[:,0] > hr) & (X[:,0] < nhr) )
        vals = X[ind,1][0].T
        try:
            #hr_avg = np.sum(vals) / len(vals)
            hr_avg = np.average(vals)
        except:
            hr_avg = np.nan
            X_hr.append([hr,hr_avg])
            hr = hr + dt.timedelta(hours=1)
    return np.array(X_hr)
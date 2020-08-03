import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#2. Import the datetime library and use 'datetime' function:
from datetime import datetime
# Now, we will load the data set and look at some initial rows and data types of the columns:
plt.figure(figsize=(20,10))
# The data contains a particular month and number of passengers travelling in that month. In order to read the data as a time series, we have to pass special arguments to the read_csv command:
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
data = pd.read_csv('ML Future.csv', parse_dates=['Month'], index_col='Month',date_parser=dateparse)
ts = data['Jobs']
ts_log = np.log(ts)
from statsmodels.tsa.arima_model import ARIMA
model = ARIMA(ts_log, order=(2, 1, 2))
results_ARIMA = model.fit(disp=-1)
results_ARIMA.plot_predict(1,216).savefig("mlfuture")
x=results_ARIMA.forecast(steps=65)
y=np.exp(x[0])
arrcount=[]
arrcount.append(int(sum(y[5:17])))
arrcount.append(int(sum(y[17:29])))
arrcount.append(int(sum(y[29:41])))
arrcount.append(int(sum(y[41:53])))
arrcount.append(int(sum(y[53:65])))
print(arrcount)
plt.show()



import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np


df = pd.read_csv("01_01_2020_00_00-25_11_2020_00_00-5m.csv", index_col=None, sep=";")



df['Number'] = np.arange(1000)+1

print(df)

x = df[:].H
y = df[:].L
slope, intercept, r_value, p_value, std_err = linregress(x, y)
print("slope: %f, intercept: %f" % (slope, intercept))
print("R-squared: %f" % r_value**2)

  
plt.figure(figsize=(15, 5))
plt.plot(x, y, 'o', label='original data')
plt.plot(x, intercept + slope*x, 'r', label='fitted line')
plt.legend()
plt.grid()
plt.show()
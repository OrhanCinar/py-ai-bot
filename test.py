import numpy as np
from sklearn import preprocessing
from gym.envs.registration import register, make
import gym
import random
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data\\test_scaled.csv", index_col=None, sep=";")
myData = df["C_Scaled"].values
shapedData = myData.reshape(1, -1)

# print(shapedData)
# scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
# scaled = scaler.fit_transform(shapedData)

scaled = preprocessing.scale(myData)
#df["C_Scaled"] = scaled

#df.to_csv("test_scaled.csv", index=False, sep=";")

print('scaled', scaled.shape)
# print("normalized", scaler.transform(scaled.reshape(1, -1)))

#pd.plotting.scatter_matrix(df, diagonal='kde', figsize=(10, 10))

plt.plot(scaled)
plt.show()

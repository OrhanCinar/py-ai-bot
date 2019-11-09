import numpy as np
from sklearn import preprocessing
from gym.envs.registration import register, make
import gym
import random
import matplotlib.pyplot as plt
import pandas as pd


def createBins():
    bins = np.zeros((5, 10))
    lineSpace = np.linspace(-4, 4, 10)
    # digit = np.digitize(1.34, lineSpace) // example
    return (bins, lineSpace)


def loadcsv():
    df = pd.read_csv("data\\small_batch.csv", index_col=None, sep=";")
    return df


def dropColumns(df):
    df.drop(["O", "H", "C", "L", "V", "VWap", "EMA5", "EMA10", "EMA20", "EMA50",
             "EMA100", "EMA200", "trend_ichimoku_a", "trend_ichimoku_b", "momentum_rsi",
             "momentum_mfi", "volatility_bbh", "volatility_bbl", "volatility_bbm", "volatility_bbhi", "volatility_bbli"], axis=1, inplace=True)
    return df


def getState(df, columnLength=25):
    state_line = df.iloc[1]
    state = np.append(state_line.to_numpy(), 1,
                      axis=None).reshape(1, columnLength)
    # print(state_line)
    # print(state)
    return state


def printColumnsMinMax(df):
    for c in df.columns:
        print(c, ' Min : ', df[c].min(), ' Max : ', df[c].max())


def scaleData(df, colName):
    #colName = "V_Scaled"

    myData = df[colName].values
    scaled = myData.reshape(1, -1)
    return scaled


def minMaxScale(scaledData):
    # print(shapedData)
    scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(scaledData)
    return scaled


def scaleData(df, data, colName):
    scaled = preprocessing.scale(data)
    df[f"{colName}_Scaled"] = scaled
    return df


def saveCsv(df):
    df.to_csv("data\\small_batch.csv", index=False, sep=";")
    return df


def plotData(data):
    # print(scaled.shape)
    plt.plot(data)
    plt.show()

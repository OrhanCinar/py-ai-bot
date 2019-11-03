import requests
import json
import pprint
import bitmex as b
import time
from datetime import datetime
from datetime import timedelta
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np
from time import sleep

PAIR_NAME = "XBTUSD"
BUCKET_URL = "https://www.bitmex.com/api/v1/trade/bucketed?"
BIN_SIZE = "1m"
START_DATE = datetime(2019, 10, 20)

# Set Column Names


# Get Data from Bitmex
def getData(count, startTime, endTime):
    df = pd.DataFrame(columns=["T", "TF", "O", "H", "C", "L", "V", "VWAP"])
    url = f"{BUCKET_URL}binSize={BIN_SIZE}&partial=false&symbol={PAIR_NAME}&reverse=true&startTime={startTime}&endTime={endTime}&count={count}"
    print(url)

    try:
        response = requests.get(url).json()

    except:
        return df

    if response is None:
        return df

    for i in range(len(response)):
        try:
            value = response[i]
            openprice = value["open"]
            closeprice = value["close"]
            highprice = value["high"]
            lowprice = value["low"]
            time = value["timestamp"]
            volume = value["volume"]
            vwap = value["vwap"]

            df = df.append({"T": time, "TF": BIN_SIZE,
                            "O": openprice,
                            "H": highprice,
                            "C": closeprice,
                            "L": lowprice,
                            "V": volume,
                            "VWAP": vwap
                            }, ignore_index=True)
        # print(f"{time} >> {openprice:.2f} | {closeprice:.2f} | {highprice:.2f} | {lowprice:.2f} | {vwap:.2f} | {volume:.2f}")
        except:
            pass

    return df


def startRequest(minutes=500):

    endTime = datetime.utcnow()
    startTime = datetime.utcnow() - timedelta(minutes=minutes)
    df = pd.DataFrame(columns=["T", "TF", "O", "H", "C", "L", "V", "VWAP"])
    while startTime > START_DATE:
        # print(startTime)
        # print(endTime)
        dd = getData(minutes, startTime, endTime)
        df = pd.concat([df, dd], axis=0, sort=False)
        endTime = startTime
        startTime -= timedelta(minutes=minutes)
        sleep(2)
        # print(dd.head())
    df.sort_values("T", axis=0, ascending=True, inplace=True)
    df.drop_duplicates(subset='T', keep=False, inplace=True)
    df.to_csv("test.csv", index=False, sep=";")


def readCsv():

    df = pd.read_csv("test.csv", index_col=None, sep=";")
    print(df.count())
    pearsoncorr = df.corr(method='pearson')

    plt.figure(figsize=(10, 5))
    sb.heatmap(pearsoncorr,
               cmap='RdBu_r',
               annot=True,
               linewidth=0.5)
    sb.set(font_scale=2)

    plt.show()


# print(df.corr())

# readCsv()
startRequest()

# print(df.count())
# print(df.head())
# print(df.corr())
# print(df.all())

# getData(500, startTime, endTime)
# print(df.head())

import pandas as pd
from utility.coi_indicators import (create_Ema_FromJson, create_Cloud )
import numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import decimal

def getKLines(coinId, timeFrameId):
    K_LINE_URL = "http://local.coi.com/api/binance/GetKLines"

    response = requests.get(K_LINE_URL, params={
        "coinId": coinId,
        "size": 1000,
        "timeFrameId": timeFrameId

    })
    json = response.json()
    # print(json['data'])
    return json

def drange(self, x, y, jump): 
        while x < y:
            yield float(x)
            x += decimal.Decimal(jump)

def create_Cloud(df):

    #ichimoku = ta.trend.IchimokuIndicator(df['H'], df['L'], 20, 60, 120, visual=False,fillna=False)    
    high_prices = df['H']
    low_prices = df['L']
    close_prices = df['C']

    # # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2))
    # period9_high = high_prices.rolling(window=20).max()
    # period9_low = low_prices.rolling(window=20).min()
    # tenkan_sen = (period9_high + period9_low) / 2

    # # Kijun-sen (Base Line): (26-period high + 26-period low)/2))
    # period26_high = high_prices.rolling( window=60).max()
    # period26_low = low_prices.rolling(window=60).min()
    # kijun_sen = (period26_high + period26_low) / 2

    # # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2))
    # senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(30)

    # # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2))
    # period52_high = high_prices.rolling(window=120).max()
    # period52_low = low_prices.rolling(window=120).min()
    # senkou_span_b = ((period52_high + period52_low) / 2).shift(30)

    # # The most current closing price plotted 22 time periods behind (optional)
    # chikou_span = close_prices.shift(-30) # 22 according to investopedia

    tenkan_window = 20
    kijun_window = 60
    senkou_span_b_window = 120
    cloud_displacement = 30
    chikou_shift = -30
  
    # Dates are floats in mdates like 736740.0
    # the period is the difference of last two dates
    # last_date = df["T"].iloc[-1]
    # period = 500

    # # Add rows for N periods shift (cloud_displacement)
    # ext_beginning = decimal.Decimal(last_date+period)
    # ext_end = decimal.Decimal(last_date + ((period*cloud_displacement)+period))
    # dates_ext = list(drange(ext_beginning, ext_end, str(period)))
    # dates_ext_df = pd.DataFrame({"OpenDateTime": dates_ext})
    # dates_ext_df.index = dates_ext # T update the df index
    # df = df.append(dates_ext_df)

    # Tenkan - Conv
    tenkan_sen_high = high_prices.rolling( window=tenkan_window ).max()
    tenkan_sen_low = low_prices.rolling( window=tenkan_window ).min()
    df['ichimoku_conversion_line'] = (tenkan_sen_high + tenkan_sen_low) /2
    # Kijun - Base
    kijun_sen_high = high_prices.rolling( window=kijun_window ).max()
    kijun_sen_low = low_prices.rolling( window=kijun_window ).min()
    df['ichimoku_base_line'] = (kijun_sen_high + kijun_sen_low) / 2
    # Senkou Span A 
    df['ichimoku_a'] = ((df['ichimoku_conversion_line'] + df['ichimoku_base_line']) / 2).shift(cloud_displacement)
    # Senkou Span B 
    senkou_span_b_high = high_prices.rolling( window=senkou_span_b_window ).max()
    senkou_span_b_low = low_prices.rolling( window=senkou_span_b_window ).min()
    df['ichimoku_b'] = ((senkou_span_b_high + senkou_span_b_low) / 2).shift(cloud_displacement)
    # Chikou
    df['chikou_span'] = close_prices.shift(chikou_shift)



    # df['ichimoku_a'] = senkou_span_a
    # df['ichimoku_b'] = senkou_span_b
    # df['ichimoku_base_line'] = kijun_sen
    # df['ichimoku_conversion_line'] = tenkan_sen
    # df['chikou_span'] = chikou_span
    return df
    


def plotChart(df, sr):
    fig = plt.figure(figsize=(15, 5))
    plt.plot(df['C'], 'y', label='Close')
  
    plt.plot(df['ichimoku_a'], label="ichimoku_a", color='g')
    plt.plot(df['ichimoku_b'],  label="ichimoku_b", color='r')
    plt.plot(df['ichimoku_base_line'],  label="ichimoku_base_line",color='b')
    plt.plot(df['ichimoku_conversion_line'], label="ichimoku_conversion_line", color='k')
    #plt.plot(df['chikou_span'], label="chikou_span", color='k')

    plt.legend()
    plt.grid()
    plt.show()


def singleCoin(timeFrameId):
    coinId = 385
    coinName = 'YFIUSDT'
    json = getKLines(coinId, timeFrameId)
    df = create_Ema_FromJson(json)
        
    df = create_Cloud(df)
    plotChart(df, coinName)
  


singleCoin(5)
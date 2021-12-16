import sys
import pandas as pd
from utility.coi_indicators import (
    create_AO, create_Ema_FromJson, create_MACD, create_Cloud_new, create_ATR, create_OBV, json_To_DF)
import numpy as np
import sys
import matplotlib.pyplot as plt
import requests
from datetime import datetime
from utility.support_resistance import (supres)
import matplotlib.lines as lines

drop_column_name = {"Name", "CoinId", "T", "TimeFrameId",
                    "OpenTime", "CloseTime", "CheckKeyDate", "Id", "CheckKey"}
normalize_columns = {"O", "H", "C", "L", "V", "ichimoku_a",
                     "ichimoku_b", "ichimoku_base_line", "ichimoku_conversion_line", "EMA20", "EMA50", "EMA200", "MACD", "MACD_Signal", "MACD_Diff"}


def drop_columns(df):
    for item in drop_column_name:
        df = drop_column(df, item)
    return df


def normalize_data(df):
    for item in normalize_columns:
        if not item in df.columns:
            continue

        df = normalize_column(df, item)
    df.dropna(inplace=True)
    return df


def normalize_column(df, column_name):
    df[column_name] = df[column_name].astype(np.float32).apply(
        lambda x: x / divider)
    return df


def drop_column(df, column_name):
    return df.drop([column_name], axis=1)


def getCoins():
    COINS_URL = "http://local.coi.com/api/coin/getcoins"
    response = requests.get(COINS_URL)
    json = response.json()
    return json


def deleteOldData(timeFrameId):
    DELETE_URL = "http://local.coi.com/api/BinanceIndicator/deleteolddata"
    requests.get(DELETE_URL,
     params={             
        "timeFrameId": timeFrameId
    })


def getKLines(coinId, timeFrameId):
    K_LINE_URL = "http://local.coi.com/api/binance/GetKLines"

    response = requests.get(K_LINE_URL, params={
        "coinId": coinId,
        "size": 500,
        "timeFrameId": timeFrameId

    })
    json = response.json()
    
    return json

def getKLines2(timeFrameId):
    K_LINE_URL = "http://local.coi.com/api/binance/GetKLines"

    response = requests.get(K_LINE_URL, params={       
        "size": 100000,
        "timeFrameId": timeFrameId

    })
    json = response.json()
    
    return json

def singleCoin(timeFrameId):
    coinId = 3
    coinName = 'BNBUSDT'
    json = getKLines(coinId, timeFrameId)
    df = json_To_DF(json)
    df = create_Ema_FromJson(df)
    df = create_MACD(df)
    df = create_AO(df)
    df["ATR"] = 0
    #df = create_ATR(df)
    #df = create_OBV(df)
    df = create_Cloud_new(df)    
    #df['price_ichimoku_diff_a_IsUp'] = (df['price_ichimoku_diff_a'].diff() > 0).astype(bool)
    #df['price_ichimoku_diff_b_IsUp'] = (df['price_ichimoku_diff_b'].diff() > 0).astype(bool)
    #print('Single Coin', df['price_ichimoku_diff_a'] ,df['price_ichimoku_diff_a_IsUp'])    
    #plotChart(df, coinName)
    print(df["AO_IsUp"])
    #df.to_csv("11test.csv")
    # plotMacdChart(df)
    #sendIndicator(coinId, coinName, df, timeFrameId)


def test():
    coinId = 385
    coinName = 'ALICEUSDT'
    json = getKLines(coinId)
    df = create_Ema_FromJson(json)
    
    # df["V"] = (df["V"] / ).astype(np.float32)

    supp, res = supres(df['C'], 100)

    df = create_Cloud(df)
    df = create_MACD(df)

    df = drop_columns(df)
    normalize_data(df)

    df.to_csv(coinName+".csv", index=False, sep=";")

  
    supp.extend(x for x in res if x not in res)
    plotChart(df, supp)


divider = 100_000


def plotMacdChart(df):
    fig = plt.figure(figsize=(15, 3))
    plt.plot(df['MACD'], 'b', label='MACD')
    plt.plot(df['MACD_Signal'], 'g', label='MACD_Signal')
    plt.plot(df['MACD_Diff'], 'y', label='MACD_Diff')
    plt.legend()
    plt.grid()
    plt.show()


def plotChart(df, sr):
    fig = plt.figure(figsize=(15, 5))
    plt.plot(df['C'], 'y', label='Close')
    # plt.plot(df['EMA20'], 'b', label='EMA20')
    # plt.plot(df['EMA50'], 'g', label='EMA50')
    # plt.plot(df['EMA200'], 'y', label='EMA200')

    plt.plot(df['ichimoku_a'], label="ichimoku_a", color='g')
    plt.plot(df['ichimoku_b'],  label="ichimoku_b", color='r')
    #plt.plot(df['ichimoku_base_line'],  label="ichimoku_base_line",color='b')
    #plt.plot(df['ichimoku_conversion_line'], label="ichimoku_conversion_line", color='k')

    #for i in sr:
     #   plt.axhline(y=i/divider, color='g', linestyle='--')

    plt.legend()
    plt.grid()
    plt.show()


def calculateIndicators(timeFrameId):
    coins = getCoins()
    print('Start : ', datetime.now())
    deleteOldData(timeFrameId)

    for coin in coins['data']:
        try:
            coinId = coin['CoinId']
            coinName = coin['CoinName']
            json = getKLines(coinId, timeFrameId)           
            df = json_To_DF(json)

            if df.shape[0] < 200:
                continue


            df = create_Ema_FromJson(df)
            df = create_MACD(df)
            df = create_ATR(df)
            df = create_Cloud_new(df)                    
            if not df.empty:
                sendIndicator(coinId, coinName, df, timeFrameId)
              
        except Exception as e:
            print(coinId, e)
    #sendMail()
    print('End : ', datetime.now())


def calculateIndicators2(timeFrameId):    
    print('Start : ', datetime.now())
    coins = getCoins()
  
    kLines = getKLines2(timeFrameId)
   
    jsonList = list(kLines['data'])
    dfJson = pd.DataFrame(jsonList)

    if dfJson.empty:
        return dfJson

    requestList = None
    deleteOldData(timeFrameId)

    for coin in coins['data']:
        try:
            coinId = coin['CoinId']
            coinName = coin['CoinName']               
            coinKLines = dfJson[dfJson.CoinId == coinId]
            #print('Df Count : CoinId  : ' , coinId , ' ' , coinKLines.shape[0])
            #print(coinKLines.head())        
            if coinKLines.shape[0] < 200:
                continue

            df = create_Ema_FromJson(coinKLines)                    
            df = create_MACD(df)
            #df = create_ATR(df)
            df = create_AO(df)
            df["ATR"] = 0
            df = create_Cloud_new(df)                    
            #lastRow = df.iloc[[-1]]
            #requestList = pd.concat( [requestList, lastRow])
            if not df.empty:
               sendIndicator(coinId, coinName, df, timeFrameId)
              
        except Exception as e:
            print('CoinId ', coinId, e)
    
    #print('requestList :' , requestList.shape[0], requestList.tail())
    sendMail()

  

    print('End : ', datetime.now())

def sendIndicator(coinId, coinName, df, timeFrameId):
    INDICATOR_URL = "http://local.coi.com/api/BinanceIndicator/AddIndicator"
    lastRow = df.iloc[[-1]]
   
    data = {
        'CoinId': coinId,
        'CoinName': coinName,
        
        'Ema20' : lastRow['EMA20'],
        'Ema50': lastRow['EMA50'],
        'Ema200': lastRow['EMA200'],
        
        'ClosePrice': lastRow['C'],
        'TimeFrameId': timeFrameId,
        'CreateDateTime': datetime.now(),
        'OpenTime': lastRow['OpenTime'],
        'CloseTime': lastRow['CloseTime'],
        'V': lastRow['V'],
        'QuoteVolume': lastRow['QuoteVolume'],
        
        'Ema20IsUp': lastRow['EMA20_Up'],
        'Ema50IsUp': lastRow['EMA50_Up'],
        'Ema200IsUp': lastRow['EMA200_Up'],


        'PriceOverEma20': lastRow['PriceOverEMA20'],
        'PriceOverEma50': lastRow['PriceOverEMA50'],
        'PriceOverEma200': lastRow['PriceOverEMA200'],
        
        'Ema20OverEma50': lastRow['EMA20OverEma50'],
        'Ema20OverEma200': lastRow['EMA20OverEma200'],
        
        'EMA50OverEma200': lastRow['EMA50OverEma200'],
        
        'EmaCross': lastRow['EMACross'],
        'PriceChange1H': lastRow['PriceChange1H'],

        'PriceEma20Cross': lastRow['PriceEma20Cross'],
        'PriceEma50Cross': lastRow['PriceEma50Cross'],
        'PriceEma200Cross': lastRow['PriceEma200Cross'],
        
        'Macd': lastRow['MACD'],
        'MacdSignal': lastRow['MACD_Signal'],
        'MacdDiff': lastRow['MACD_Diff'],
        'MacdCross': lastRow['MACD_Cross'],
        'MacdIsUp': lastRow["MACD_Up"],
        'MacdSignalIsUp': lastRow["MACD_Signal_Up"],
        'MacdDiffIsUp': lastRow["MACD_Diff_Up"],
        'ATR': lastRow["ATR"],
        'IchimokuA':	lastRow['ichimoku_a'],
        'IchimokuB': lastRow['ichimoku_b'],
        'IchimokuBaseLine': lastRow['ichimoku_base_line'],
        'IchimokuConvLine': lastRow['ichimoku_conversion_line'],
        'IchimokuAIsUp': lastRow['ichimoku_a_Up'],
        'IchimokuBIsUp': lastRow['ichimoku_b_Up'],
        'IchimokuBaseLineIsUp': lastRow['ichimoku_base_line_Up'],
        'IchimokuConvLineIsUp': lastRow['ichimoku_conversion_line_Up'],
        'PriceOverIchimokuA': lastRow['price_over_ichimoku_a'],
        'PriceOverIchimokuB': lastRow['price_over_ichimoku_b'],
        'PriceOverIchimokuBaseLine': lastRow['price_over_ichimoku_base_line'],
        'PriceOverIchimokuConvLine': lastRow['price_over_ichimoku_conversion_line'],
        'IchimokuAOverB': lastRow['ichimoku_a_over_b'],
        'IchimokuAOverBaseLine': lastRow['ichimoku_a_over_base'],
        'IchimokuAOverConvLine': lastRow['ichimoku_a_over_conv'],
        'IchimokBOverA': lastRow['ichimoku_b_over_a'],
        'IchimokBOverBaseLine': lastRow['ichimoku_b_over_base'],
        'IchimokBOverConvLine': lastRow['ichimoku_b_over_conv'],
        'IchimokuBaseLineOverConvLine': lastRow['ichimoku_base_over_conv'],
        'IchimokuConvLineOverBaseLine': lastRow['ichimoku_conv_over_base'],

        'IchimokuChikou': lastRow['ichimoku_chikou_span'],
        'PriceInCloud': lastRow['priceInCloud'],
        'PricePrevInCloud': lastRow['pricePrevInCloud'],

        'PriceIchimokuDiffA' :lastRow['price_ichimoku_diff_a']  ,
        'PriceIchimokuDiffAIsUp':lastRow['price_ichimoku_diff_a_IsUp'],

        'PriceIchimokuDiffB' :lastRow['price_ichimoku_diff_b']  ,
        'PriceIchimokuDiffBIsUp':lastRow['price_ichimoku_diff_b_IsUp']
    }
    requests.post(INDICATOR_URL, data)


def sendIndicator2(df):
    INDICATOR_URL = "http://local.coi.com/api/BinanceIndicator/AddIndicators"
    
    list = []

    for index, row in df.iterrows():   
        lastRow = row
        data = {
            'CoinId': lastRow['CoinId'],
            'CoinName': lastRow['CoinName'],
            
            'Ema20' : lastRow['EMA20'],
            'Ema50': lastRow['EMA50'],
            'Ema200': lastRow['EMA200'],
            
            'ClosePrice': lastRow['C'],
            'TimeFrameId': lastRow['TimeFrameId'],
            'CreateDateTime': datetime.now(),
            'OpenTime': lastRow['OpenTime'],
            'CloseTime': lastRow['CloseTime'],
            'V': lastRow['V'],
            'QuoteVolume': lastRow['QuoteVolume'],
            
            'Ema20IsUp': lastRow['EMA20_Up'],
            'Ema50IsUp': lastRow['EMA50_Up'],
            'Ema200IsUp': lastRow['EMA200_Up'],


            'PriceOverEma20': lastRow['PriceOverEMA20'],
            'PriceOverEma50': lastRow['PriceOverEMA50'],
            'PriceOverEma200': lastRow['PriceOverEMA200'],
            
            'Ema20OverEma50': lastRow['EMA20OverEma50'],
            'Ema20OverEma200': lastRow['EMA20OverEma200'],
            
            'EMA50OverEma200': lastRow['EMA50OverEma200'],
            
            'EmaCross': lastRow['EMACross'],
            'PriceChange1H': lastRow['PriceChange1H'],

            'PriceEma20Cross': lastRow['PriceEma20Cross'],
            'PriceEma50Cross': lastRow['PriceEma50Cross'],
            'PriceEma200Cross': lastRow['PriceEma200Cross'],
            
            'Macd': lastRow['MACD'],
            'MacdSignal': lastRow['MACD_Signal'],
            'MacdDiff': lastRow['MACD_Diff'],
            'MacdCross': lastRow['MACD_Cross'],
            'MacdIsUp': lastRow["MACD_Up"],
            'MacdSignalIsUp': lastRow["MACD_Signal_Up"],
            'MacdDiffIsUp': lastRow["MACD_Diff_Up"],
            'ATR': lastRow["ATR"],
            'IchimokuA':	lastRow['ichimoku_a'],
            'IchimokuB': lastRow['ichimoku_b'],
            'IchimokuBaseLine': lastRow['ichimoku_base_line'],
            'IchimokuConvLine': lastRow['ichimoku_conversion_line'],
            'IchimokuAIsUp': lastRow['ichimoku_a_Up'],
            'IchimokuBIsUp': lastRow['ichimoku_b_Up'],
            'IchimokuBaseLineIsUp': lastRow['ichimoku_base_line_Up'],
            'IchimokuConvLineIsUp': lastRow['ichimoku_conversion_line_Up'],
            'PriceOverIchimokuA': lastRow['price_over_ichimoku_a'],
            'PriceOverIchimokuB': lastRow['price_over_ichimoku_b'],
            'PriceOverIchimokuBaseLine': lastRow['price_over_ichimoku_base_line'],
            'PriceOverIchimokuConvLine': lastRow['price_over_ichimoku_conversion_line'],
            'IchimokuAOverB': lastRow['ichimoku_a_over_b'],
            'IchimokuAOverBaseLine': lastRow['ichimoku_a_over_base'],
            'IchimokuAOverConvLine': lastRow['ichimoku_a_over_conv'],
            'IchimokBOverA': lastRow['ichimoku_b_over_a'],
            'IchimokBOverBaseLine': lastRow['ichimoku_b_over_base'],
            'IchimokBOverConvLine': lastRow['ichimoku_b_over_conv'],
            'IchimokuBaseLineOverConvLine': lastRow['ichimoku_base_over_conv'],
            'IchimokuConvLineOverBaseLine': lastRow['ichimoku_conv_over_base'],

            'IchimokuChikou': lastRow['ichimoku_chikou_span'],
            'PriceInCloud': lastRow['priceInCloud'],
            'PricePrevInCloud': lastRow['pricePrevInCloud'],

            'PriceIchimokuDiffA' :lastRow['price_ichimoku_diff_a']  ,
            'PriceIchimokuDiffAIsUp':lastRow['price_ichimoku_diff_a_IsUp'],

            'PriceIchimokuDiffB' :lastRow['price_ichimoku_diff_b']  ,
            'PriceIchimokuDiffBIsUp':lastRow['price_ichimoku_diff_b_IsUp'],
            'AO' : lastRow["AO"],
            'AO_IsUp' : lastRow["AO_IsUp"]
        }
    requests.post(INDICATOR_URL, data)


def sendMail():
     URL = "http://local.coi.com/api/mail/SendIchimokuSignals"
     requests.get(URL)

def sendMailHourly():
     URL = "http://local.coi.com/api/mail/SendIchimokuSignalsHourly"
     requests.get(URL)

if __name__ == "__main__":
    param = int(sys.argv[1])
    
    if param == 5:
        calculateIndicators2(5)
    elif param == 60:
        calculateIndicators2(60)
        sendMailHourly()
    elif param == 999:
        singleCoin(5)        
    elif param == 666:    
        calculateIndicators2(5)
#singleCoin(60)

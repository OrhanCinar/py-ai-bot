import pandas as pd
import ta
import matplotlib.pyplot as plt
import numpy as np
pd.options.mode.chained_assignment = None 

divider = 100_000


def json_To_DF(json):
    jsonList = list(json['data'])
    df = pd.DataFrame(jsonList)
    return df


def create_Ema_FromJson(df):
   
    df["EMA20"] = (ta.trend.ema_indicator(df["C"], 20)).astype(np.float32)
    df["EMA50"] = (ta.trend.ema_indicator(df["C"], 50)).astype(np.float32)
    df["EMA200"] = (ta.trend.ema_indicator(df["C"], 200)).astype(np.float32)

    # df["EMA20"] = (ta.trend.ema_indicator(df["C"], 20))
    # df["EMA50"] = (ta.trend.ema_indicator(df["C"], 50))
    # df["EMA200"] = (ta.trend.ema_indicator(df["C"], 200))

    df['EMA20_Up'] = (df['EMA20'].diff() > 0).astype(bool)
    df['EMA50_Up'] = (df['EMA50'].diff() > 0).astype(bool)
    df['EMA200_Up'] = (df['EMA200'].diff() > 0).astype(bool)

    df["PriceOverEMA20"] = (df["C"] > df["EMA20"]).astype(bool)
    df["PriceOverEMA50"] = (df["C"] > df["EMA50"]).astype(bool)
    df["PriceOverEMA200"] = (df["C"] > df["EMA200"]).astype(bool)

    df["EMA20OverEma50"] = (df["EMA20"] > df["EMA50"]).astype(bool)
    df["EMA20OverEma200"] = (df["EMA20"] > df["EMA200"]).astype(bool)

    df["EMA50OverEma200"] = (df["EMA50"] > df["EMA200"]).astype(bool)

    df["EMACross"] = ((df["EMA50"] > df["EMA200"]) & (
        df["EMA50"].shift() <= df["EMA200"].shift())).astype(bool)

    df["PriceEma20Cross"] = ((df["C"] > df["EMA20"]) & (
        df["C"].shift() <= df["EMA20"].shift())).astype(bool)
    df["PriceEma50Cross"] = ((df["C"] > df["EMA50"]) & (
        df["C"].shift() <= df["EMA50"].shift())).astype(bool)
    df["PriceEma200Cross"] = ((df["C"] > df["EMA200"]) & (
        df["C"].shift() <= df["EMA200"].shift())).astype(bool)

    df['PriceChange1H'] = (df['C'] - df['C'].shift(12)) / df['C'] * 100
    
    return df


def create_MACD(df):
    close_price = df["C"]
    macd = ta.trend.macd(close_price)  # macd
    macd_Signal = ta.trend.macd_signal(close_price)  # macd signal
    macd_diff = ta.trend.macd_diff(close_price)  # histogram
    df["MACD"] = macd
    df["MACD_Signal"] = macd_Signal
    df["MACD_Diff"] = macd_diff
    df["MACD_Cross"] = ((macd > macd_Signal) & (
        df["MACD"].shift() <= df["MACD_Signal"].shift())).astype(bool)
    df["MACD_Up"] = (df["MACD"].diff() > 0).astype(bool)
    df["MACD_Signal_Up"] = (df["MACD_Signal"].diff() > 0).astype(bool)
    df["MACD_Diff_Up"] = (df["MACD_Diff"].diff() > 0).astype(bool)
    return df

def create_AO(df):
    high_price = df["H"]
    low_price = df["L"]    
    ao = ta.momentum.awesome_oscillator(high_price, low_price, 5, 34)
    df["AO"]  = ao
    df["AO_IsUp"] = (df["AO"].diff() > 0).astype(bool)
    return df

def create_ATR(df):
    high_price = df["H"]
    low_price = df["L"]
    close_price = df["C"]
    atr = ta.volatility.average_true_range(high_price, low_price, close_price)

    df["ATR"] = atr
    return df


def create_OBV(df):
    volume = df["V"]
    close_price = df["C"]
    obv = ta.volume.on_balance_volume(close_price, volume)

    df["OBV"] = obv
    return df


def create_Cloud(df):

    ichimoku = ta.trend.IchimokuIndicator(
        df['H'], df['L'], 20, 60, 120, visual=False, fillna=False)

    df['ichimoku_a'] = ichimoku.ichimoku_a()
    df['ichimoku_b'] = ichimoku.ichimoku_b()
    df['ichimoku_base_line'] = ichimoku.ichimoku_base_line()
    df['ichimoku_conversion_line'] = ichimoku.ichimoku_conversion_line()

    close_price = df['C']

    df['ichimoku_a_Up'] = (df['ichimoku_a'].diff() > 0).astype(bool)
    df['ichimoku_b_Up'] = (df['ichimoku_b'].diff() > 0).astype(bool)
    df['ichimoku_base_line_Up'] = (
        df['ichimoku_base_line'].diff() > 0).astype(bool)
    df['ichimoku_conversion_line_Up'] = (
        df['ichimoku_conversion_line'].diff() > 0).astype(bool)

    df['price_over_ichimoku_a'] = (
        close_price > df['ichimoku_a']).astype(bool)
    df['price_over_ichimoku_b'] = (
        close_price > df['ichimoku_b']).astype(bool)
    df['price_over_ichimoku_base_line'] = (
        close_price > df['ichimoku_base_line']).astype(bool)
    df['price_over_ichimoku_conversion_line'] = (
        close_price > df['ichimoku_conversion_line']).astype(bool)

    df['ichimoku_a_over_b'] = (
        df['ichimoku_a'] > df['ichimoku_b']).astype(bool)
    df['ichimoku_a_over_base'] = (df['ichimoku_a'] > df['ichimoku_base_line']).astype(
        bool)
    df['ichimoku_a_over_conv'] = (df['ichimoku_a'] > df['ichimoku_conversion_line']).astype(
        bool)

    df['ichimoku_b_over_a'] = (
        df['ichimoku_b'] > df['ichimoku_a']).astype(bool)
    df['ichimoku_b_over_base'] = (df['ichimoku_b'] > df['ichimoku_base_line']).astype(
        bool)
    df['ichimoku_b_over_conv'] = (df['ichimoku_b'] > df['ichimoku_conversion_line']).astype(
        bool)

    df['ichimoku_base_over_conv'] = (df['ichimoku_base_line'] > df['ichimoku_conversion_line']).astype(
        bool)
    df['ichimoku_conv_over_base'] = (df['ichimoku_conversion_line'] > df['ichimoku_base_line']).astype(
        bool)
    # df.dropna(inplace=True)

    return df


def create_Cloud_new(df):

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
    tenkan_sen_high = high_prices.rolling(window=tenkan_window).max()
    tenkan_sen_low = low_prices.rolling(window=tenkan_window).min()
    df['ichimoku_conversion_line'] = (tenkan_sen_high + tenkan_sen_low) / 2
    # Kijun - Base
    kijun_sen_high = high_prices.rolling(window=kijun_window).max()
    kijun_sen_low = low_prices.rolling(window=kijun_window).min()
    df['ichimoku_base_line'] = (kijun_sen_high + kijun_sen_low) / 2
    # Senkou Span A
    df['ichimoku_a'] = ((df['ichimoku_conversion_line'] +
                        df['ichimoku_base_line']) / 2).shift(cloud_displacement)
    # Senkou Span B
    senkou_span_b_high = high_prices.rolling(window=senkou_span_b_window).max()
    senkou_span_b_low = low_prices.rolling(window=senkou_span_b_window).min()
    df['ichimoku_b'] = (
        (senkou_span_b_high + senkou_span_b_low) / 2).shift(cloud_displacement)
    # Chikou
    df['ichimoku_chikou_span'] = close_prices.shift(chikou_shift)

    df['priceInCloud'] = (close_prices < df['ichimoku_a']) & (
        close_prices > df['ichimoku_b'])
    df['pricePrevInCloud'] = (close_prices < df['ichimoku_a'].shift(-1)
                              ) & (close_prices > df['ichimoku_b'].shift(-1))

    df['ichimoku_a_Up'] = (df['ichimoku_a'].diff() > 0).astype(bool)
    df['ichimoku_b_Up'] = (df['ichimoku_b'].diff() > 0).astype(bool)
    df['ichimoku_base_line_Up'] = (
        df['ichimoku_base_line'].diff() > 0).astype(bool)
    df['ichimoku_conversion_line_Up'] = (
        df['ichimoku_conversion_line'].diff() > 0).astype(bool)

    df['price_over_ichimoku_a'] = (
        close_prices > df['ichimoku_a']).astype(bool)
    df['price_over_ichimoku_b'] = (
        close_prices > df['ichimoku_b']).astype(bool)
    df['price_over_ichimoku_base_line'] = (
        close_prices > df['ichimoku_base_line']).astype(bool)
    df['price_over_ichimoku_conversion_line'] = (
        close_prices > df['ichimoku_conversion_line']).astype(bool)

    df['ichimoku_a_over_b'] = (
        df['ichimoku_a'] > df['ichimoku_b']).astype(bool)
    df['ichimoku_a_over_base'] = (df['ichimoku_a'] > df['ichimoku_base_line']).astype(
        bool)
    df['ichimoku_a_over_conv'] = (df['ichimoku_a'] > df['ichimoku_conversion_line']).astype(
        bool)

    df['ichimoku_b_over_a'] = (
        df['ichimoku_b'] > df['ichimoku_a']).astype(bool)
    df['ichimoku_b_over_base'] = (df['ichimoku_b'] > df['ichimoku_base_line']).astype(
        bool)
    df['ichimoku_b_over_conv'] = (df['ichimoku_b'] > df['ichimoku_conversion_line']).astype(
        bool)

    df['ichimoku_base_over_conv'] = (df['ichimoku_base_line'] > df['ichimoku_conversion_line']).astype(
        bool)
    df['ichimoku_conv_over_base'] = (df['ichimoku_conversion_line'] > df['ichimoku_base_line']).astype(
        bool)    
    df['price_ichimoku_diff_a'] = getPercDiff2(df['ichimoku_a'], df['C'])
    df['price_ichimoku_diff_b'] = getPercDiff2(df['ichimoku_b'], df['C'])
    df['price_ichimoku_diff_a_IsUp'] = (df['price_ichimoku_diff_a'].diff() > 0).astype(bool)
    df['price_ichimoku_diff_b_IsUp'] = (df['price_ichimoku_diff_b'].diff() > 0).astype(bool)
    return df


def calculateIchimokuDiff(df):
    df['price_ichimoku_diff'] = getPercDiff(df)
    df['price_ichimoku_diffIsUp'] = (df['price_ichimoku_diff'] > df['price_ichimoku_diff'].shift(-1)).astype(
        bool)
    return df    

def getPercDiff(df):
    diff = 0
    lastRow = df.iloc[[-1]]   
    v2 = lastRow['C']
    v1 = 0    
    if (lastRow['ichimoku_a'] > lastRow['ichimoku_b']).bool():
        v1 = lastRow['ichimoku_a']
    else :     
        v1 = lastRow['ichimoku_b']

    diff = ((v2 - v1) / v1) * 100

    return diff

def getPercDiff2(v1, v2):   
    diff = ((v2 - v1) / v1) * 100

    return diff

def normalize_column(df, column_name):
    df[column_name] = df[column_name].astype(np.float32).apply(
        lambda x: x / divider)
    return df


def drop_column(df, column_name):
    return df.drop([column_name], axis=1)

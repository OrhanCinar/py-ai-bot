import pandas as pd
import ta
import matplotlib.pyplot as plt
import os.path
import numpy as np
from ta.volatility import BollingerBands

divider = 100_000


def create_Cloud(file_name):
    if not os.path.exists(file_name):
        print("no file")
        return

    df = pd.read_csv(file_name, index_col=None, sep=";", nrows=200)
    #df = add_all_ta_features(df, "O", "H", "L", "C", "V", fillna=True)

    # df["IchimokuA"] = ichimoku_a(df["H"], df["L"], 20, 60, visual=True)
    # df["IchimokuB"] = ichimoku_b(df["H"], df["L"], 20, 60, visual=True)
    # print(df)
    # df = df[-120:]
    ax = plt.plot(df.C, label="Close", color="black")
    # ax = plt.plot(df.H, label="H")
    # ax = plt.plot(df.L, label="L")
    # ax.set_xlabel("T")

    plt.plot(df["ichimoku_a"], label='Ichimoku a', color='blue')
    plt.plot(df["ichimoku_b"], label='Ichimoku b', color='red')
    plt.plot(df["ichimoku_base_line"], label='Ichimoku base')
    plt.plot(df["ichimoku_conversion_line"], label='Ichimoku C')
    #plt.plot(df.momentum_kama, label='Kama')
    #plt.plot(df.C, label='C')

    plt.title('Ichimoku Kinko Hyo')
    plt.legend()
    plt.grid("True")

    plt.show()


def create_EMA(file_name):
    if not os.path.exists(file_name):
        print("file not exists")
        return

    df = pd.read_csv(file_name, index_col=None, sep=";")
    df["EMA5"] = (ta.trend.ema_indicator(
        df["C"], 5) / divider).astype(np.float32)
    df["EMA10"] = (ta.trend.ema_indicator(
        df["C"], 10) / divider).astype(np.float32)
    df["EMA20"] = (ta.trend.ema_indicator(
        df["C"], 20) / divider).astype(np.float32)
    df["EMA50"] = (ta.trend.ema_indicator(
        df["C"], 50) / divider).astype(np.float32)
    df["EMA100"] = (ta.trend.ema_indicator(
        df["C"], 100) / divider).astype(np.float32)
    df["EMA200"] = (ta.trend.ema_indicator(
        df["C"], 200) / divider).astype(np.float32)
    return df


def create_volatile_indicators(df):
    df["ichimoku_a"] = ta.trend.ichimoku_a(
        df["H"], df["L"], 20, 60, visual=True).astype(np.float32)
    df["ichimoku_b"] = ta.trend.ichimoku_b(
        df["H"], df["L"], 20, 60, visual=True).astype(np.float32)
    df["ichimoku_base_line"] = ta.trend.ichimoku_base_line(
        df["H"], df["L"], 20, 60, visual=True).astype(np.float32)
    df["ichimoku_conversion_line"] = ta.trend.ichimoku_conversion_line(
        df["H"], df["L"], 20, 60, visual=True).astype(np.float32)

    # df["momentum_rsi"] = ta.momentum.rsi(df["C"])
    # df["momentum_mfi"] = ta.volume.money_flow_index(
    #     df["H"], df["L"], df["C"], df["V"])

    # indicator_bb = BollingerBands(close=df["C"])
    # df["volatility_bbh"] = indicator_bb.bollinger_hband()
    # df["volatility_bbl"] = indicator_bb.bollinger_lband()
    # df["volatility_bbm"] = indicator_bb.bollinger_mavg()

    # df["volatility_bbhi"] = indicator_bb.bollinger_hband_indicator()
    # df["volatility_bbli"] = indicator_bb.bollinger_lband_indicator()
    return df


def normalize_column(df, column_name):
    df[column_name] = df[column_name].astype(np.float32).apply(
        lambda x: x / divider)
    return df


def drop_column(df, column_name):
    return df.drop([column_name], axis=1)


def plotEma(df):
    plt.plot(df.C, label="Close")
    plt.plot(df.EMA5, label='EMA5')
    plt.plot(df.EMA10, label='EMA10')
    plt.plot(df.EMA20, label='EMA20')
    plt.plot(df.EMA50, label='EMA50')
    plt.plot(df.EMA100, label='EMA100')
    plt.plot(df.EMA200, label='EMA200')
    plt.title('EMA')
    plt.legend()
    plt.show()


def export_indicators(from_file, to_file):
    if not os.path.exists(from_file):
        return
    df = pd.read_csv(from_file, index_col=None, sep=";")
    # df = add_all_ta_features(df, "O", "H", "L", "C", "V", fillna=True)
    df["EMA5"] = ema_indicator(df["C"], 5)
    df["EMA10"] = ema_indicator(df["C"], 10)
    df["EMA20"] = ema_indicator(df["C"], 20)
    df["EMA50"] = ema_indicator(df["C"], 50)
    df["EMA100"] = ema_indicator(df["C"], 100)
    df["EMA200"] = ema_indicator(df["C"], 200)
    df["trend_ichimoku_a"] = ichimoku_a(
        df["H"], df["L"], 20, 60, visual=True)
    df["trend_ichimoku_b"] = ichimoku_b(
        df["H"], df["L"], 20, 60, visual=True)

    df["momentum_rsi"] = rsi(df["C"])
    df["momentum_mfi"] = money_flow_index(
        df["H"], df["L"], df["C"], df["V"])
    df["volatility_bbh"] = bollinger_hband(df["C"])
    df["volatility_bbl"] = bollinger_lband(df["C"])
    df["volatility_bbm"] = bollinger_mavg(df["C"])
    df["volatility_bbhi"] = bollinger_hband_indicator(df["C"])
    df["volatility_bbli"] = bollinger_lband_indicator(df["C"])

    df.to_csv(to_file, index=False, sep=";")

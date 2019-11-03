import pandas as pd
from ta import *
import matplotlib.pyplot as plt


def createCloud():
    df = pd.read_csv("test.csv", index_col=None, sep=";")
    df = add_all_ta_features(df, "O", "H", "L", "C", "V", fillna=True)

    # df["IchimokuA"] = ichimoku_a(df["H"], df["L"], 20, 60, visual=True)
    # df["IchimokuB"] = ichimoku_b(df["H"], df["L"], 20, 60, visual=True)
    # print(df)
    # df = df[-120:]
    ax = plt.plot(df.C, label="Close", linestyle='dashed',
                  linewidth=2, markersize=10)
    # ax.set_xlabel("T")

    plt.plot(df.trend_ichimoku_a, label='Ichimoku a', color='blue')
    plt.plot(df.trend_ichimoku_b, label='Ichimoku b', color='red')
    plt.plot(df.momentum_kama, label='Kama')
    plt.plot(df.trend_ema_slow, label='EMA')

    plt.title('Ichimoku Kinko Hyo')
    plt.legend()
    plt.grid("True")

    plt.show()
    return 0


def creatEMA():
    df = pd.read_csv("data/alldata.csv", index_col=None, sep=";")
    df["EMA5"] = ema_indicator(df["C"], 5)
    df["EMA10"] = ema_indicator(df["C"], 10)
    df["EMA20"] = ema_indicator(df["C"], 20)
    df["EMA50"] = ema_indicator(df["C"], 50)
    df["EMA100"] = ema_indicator(df["C"], 100)
    df["EMA200"] = ema_indicator(df["C"], 200)

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
    return 0


def exportIndicators():
    df = pd.read_csv("data\\alldata.csv", index_col=None, sep=";")
    #df = add_all_ta_features(df, "O", "H", "L", "C", "V", fillna=True)
    df["EMA5"] = ema_indicator(df["C"], 5)
    df["EMA10"] = ema_indicator(df["C"], 10)
    df["EMA20"] = ema_indicator(df["C"], 20)
    df["EMA50"] = ema_indicator(df["C"], 50)
    df["EMA100"] = ema_indicator(df["C"], 100)
    df["EMA200"] = ema_indicator(df["C"], 200)
    df["trend_ichimoku_a"] = ichimoku_a(df["H"], df["L"], 20, 60, visual=True)
    df["trend_ichimoku_b"] = ichimoku_b(df["H"], df["L"], 20, 60, visual=True)

    df["momentum_rsi"] = rsi(df["C"])
    df["momentum_mfi"] = money_flow_index(df["H"], df["L"], df["C"], df["V"])
    df["volatility_bbh"] = bollinger_hband(df["C"])
    df["volatility_bbl"] = bollinger_lband(df["C"])
    df["volatility_bbm"] = bollinger_mavg(df["C"])
    df["volatility_bbhi"] = bollinger_hband_indicator(df["C"])
    df["volatility_bbli"] = bollinger_lband_indicator(df["C"])

    df.to_csv("data\\indicators_light.csv", index=False, sep=";")
    return 0


exportIndicators()

# createCloud()

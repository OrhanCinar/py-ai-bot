import pandas as pd
import ta
import matplotlib.pyplot as plt
import os.path


def create_Cloud(file_name):
    if not os.path.exists(file_name):
        return
    df = pd.read_csv(file_name, index_col=None, sep=";")
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


def create_EMA(file_name):
    if not os.path.exists(file_name):
        print("file not exists")
        return

    df = pd.read_csv(file_name, index_col=None, sep=";")
    df["EMA5"] = ta.trend.ema_indicator(df["C"], 5)
    df["EMA10"] = ta.trend.ema_indicator(df["C"], 10)
    df["EMA20"] = ta.trend.ema_indicator(df["C"], 20)
    df["EMA50"] = ta.trend.ema_indicator(df["C"], 50)
    df["EMA100"] = ta.trend.ema_indicator(df["C"], 100)
    df["EMA200"] = ta.trend.ema_indicator(df["C"], 200)
    return df


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

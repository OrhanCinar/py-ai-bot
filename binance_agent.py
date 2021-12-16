import pandas as pd
import Binance.binance_data
from utility.indicators import create_EMA, drop_column, normalize_column, create_volatile_indicators, create_Cloud
import Binance.binanceEnvironment as b
import numpy as np
import sys
import matplotlib.pyplot as plt

env = b.BinanceEnvironment()

# state = np.reshape(state, [1, -1])
# print(state)
# env.init("data\\test.csv", total_budget=100.0,
#          budget_per_trade=5.0, render=True)
# state = env.get_state()
# # print(env.get_data_frame())
# # print(env.get_actions())

# for i in range(10):
#     ##print(env.get_state()[8], "-", env.get_state()[3])
#     action = np.random.choice(env.get_actions())
#     next_state, reward, done, _ = env.step(action)
#     # sys.stdout.flush()
# print(env.get_rewards_sum())

# plt.plot(env.get_rewards(), label="Rewards")
# plt.show()

# df = pd.read_csv("data\\test.csv", delimiter=";")
# x = df.iloc[5].values
# print(type(x))


# print(df.head())
drop_column_name = {"TF", "OpenDT", "CloseDT"}
normalize_columns = {"O", "H", "C", "L", "ichimoku_a",
                     "ichimoku_b", "ichimoku_base_line", "ichimoku_conversion_line"}
divider = 100_000


def add_emas():
    df = create_EMA("Binance\\data\\01_01_2020_00_00-06_12_2020_00_00-1h.csv")
    return df


def add_volatile(df):
    df = create_volatile_indicators(df)
    return df


def drop_columns(df):
    for item in drop_column_name:
        df = drop_column(df, item)
    return df


def normalize_data(df):
    for item in normalize_columns:
        df = normalize_column(df, item)
    df.dropna(inplace=True)
    return df


def order_columns(df):
    df = df[['OT', 'CT', 'O', 'H', 'C', 'L', 'EMA5',
             'EMA10', 'EMA20', 'EMA50', 'EMA100', 'EMA200']]
    return df


def calculate_indicators(df):
    # for index, row in df.iterrows():
    #     df["PriceUp"] = df["C"] > df["C"].shift(-1)
    #df = df[[10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8]]
    close_price = df['C']
    close_price_diff = df['C'].diff()

    df['Price_Up'] = (close_price_diff > 0).astype(int)
    df['Perc_Change'] = round(df['C'].pct_change(
        periods=1).astype(np.float32), 8)

    df['ichimoku_a_Up'] = (df['ichimoku_a'].diff() > 0).astype(int)
    df['ichimoku_b_Up'] = (df['ichimoku_b'].diff() > 0).astype(int)
    df['ichimoku_base_line_Up'] = (
        df['ichimoku_base_line'].diff() > 0).astype(int)
    df['ichimoku_conversion_line_Up'] = (
        df['ichimoku_conversion_line'].diff() > 0).astype(int)

    df['price_over_ichimoku_a'] = (
        close_price > df['ichimoku_a']).astype(int)
    df['price_over_ichimoku_b'] = (
        close_price > df['ichimoku_b']).astype(int)
    df['price_over_ichimoku_base_line'] = (
        close_price > df['ichimoku_base_line']).astype(int)
    df['price_over_ichimoku_conversion_line'] = (
        close_price > df['ichimoku_conversion_line']).astype(int)

    df['ichimoku_a_over_b'] = df['ichimoku_a'] > df['ichimoku_b'].astype(int)
    df['ichimoku_a_over_base'] = df['ichimoku_a'] > df['ichimoku_base_line'].astype(
        int)
    df['ichimoku_a_over_conv'] = df['ichimoku_a'] > df['ichimoku_conversion_line'].astype(
        int)

    df['ichimoku_b_over_a'] = df['ichimoku_b'] > df['ichimoku_a'].astype(int)
    df['ichimoku_b_over_base'] = df['ichimoku_b'] > df['ichimoku_base_line'].astype(
        int)
    df['ichimoku_b_over_conv'] = df['ichimoku_b'] > df['ichimoku_conversion_line'].astype(
        int)

    df['ichimoku_base_over_conv'] = df['ichimoku_base_line'] > df['ichimoku_conversion_line'].astype(
        int)
    df['ichimoku_conv_over_base'] = df['ichimoku_conversion_line'] > df['ichimoku_base_line'].astype(
        int)
    # .fillna(0)

   
    df.dropna(inplace=True)

    #df = df.rename(columns={10: 'OT', 11: 'CT',0: 'O', 1: 'H', 2: 'C', 3: 'L'})
    return df


def export_csv(df):
    df.to_csv("data\\test_17122020.csv", index=False, sep=";")


#df = add_emas()
# df = pd.read_csv(
#     "Binance\\data\\01_01_2020_00_00-06_12_2020_00_00-1h.csv", index_col=None, sep=";")
# df = add_volatile(df)
# df = drop_columns(df)
# df = normalize_data(df)
# df = calculate_indicators(df)
# export_csv(df)
# print(df.head())


create_Cloud("data\\test_17122020.csv")

# df.drop([0, 1], inplace=True)

# df["O"] = df["O"].astype(np.float32)
# df["H"] = df["O"].astype(np.float32)
# df["C"] = df["C"].astype(np.float32)
# df["L"] = df["L"].astype(np.float32)
# df["EMA5"] = df["EMA5"].astype(np.float32)
# df["EMA10"] = df["EMA10"].astype(np.float32)
# df["EMA20"] = df["EMA20"].astype(np.float32)
# df["EMA50"] = df["EMA50"].astype(np.float32)
# df["EMA100"] = df["EMA100"].astype(np.float32)
# df["EMA200"] = df["EMA200"].astype(np.float32)

#df["OT"] = df["OpenDT"]
#df["CT"] = df["CloseDT"]
#df.drop(columns=["OpenDT", "CloseDT"], inplace=True)
# print(df.dtypes)

# print(df.to_numpy())

# state_line = df.iloc[1][:-2]
# print("state_line", state_line)
# state = np.append(state_line.to_numpy(), 0, axis=None).reshape(1, -1)

# print("State", state)


# print(df.head(10))
#df.to_csv("data\\test.csv", index=False, sep=";")

# print(startTime)
# print(endTime)
# print(repr(KLines.ONE_HOUR.value))
# agent = BinanceDataAgent()
# startTime = datetime(2020, 1, 1)
# endTime = startTime + timedelta(days=10)
# agent.get_data("BTCUSDT", KLines.ONE_HOUR.value, startTime, endTime)
# data = agent.get_data_frame()
# trans = data.iloc[0].to_numpy().reshape(1, data.iloc[0].count())
# print(trans)

# STEP_SIZE = 80
# INTERVAL = KLines.THREE_DAY.value

# startTime = datetime(2020, 1, 1)
# fileNameStart = startTime
# # startTime = agent.hour_rounder(startTime)
# endTime = startTime + timedelta(days=STEP_SIZE)
# df = pd.DataFrame(
#     columns=["OT", "CT", "TF", "O", "H", "C", "L", "V", "OpenDT", "CloseDT"])
# while endTime < (datetime(2021, 6, 1)):
#     data = agent.get_data("BTCUSDT", INTERVAL, startTime, endTime)
#     print(startTime, endTime)
#     if (agent.r.status_code == 200):
#         dtTemp = agent.get_data_frame()
#         df = pd.concat([df, dtTemp], axis=0, sort=False)
#         startTime += timedelta(days=STEP_SIZE)
#         endTime = startTime + timedelta(days=STEP_SIZE)
#         # sleep(2)
#         # print(df.head())

# file_name = fileNameStart.strftime("%d_%m_%Y_%H_%M") + "-" + endTime.strftime(
#     "%d_%m_%Y_%H_%M") + "-" + INTERVAL
# agent.save_csv(df, file_name)

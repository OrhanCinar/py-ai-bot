import requests
import pandas as pd
from enum import Enum
from datetime import datetime, timedelta
from time import sleep

# https://api.binance.com/api/v1/klines?symbol=BTCUSDT&interval=1h&startTime=
# https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#klinecandlestick-data

K_LINE_URL = "https://api.binance.com/api/v1/klines"
# ?symbol=BTCUSDT&interval=5m


class KLines(Enum):
    ONE_MINUTE = "1m"
    THREE_MINUTE = "3m"
    FIVE_MINUTE = "5m"
    FIFTEEN_MINUTE = "15m"
    THIRTY_MINUTE = "30m"
    ONE_HOUR = "1h"
    TWO_HOUR = "2h"
    FOUR_HOUR = "4h"
    SIX_HOUR = "6h"
    EIGHT_HOUR = "8h"
    TWELVE_HOUR = "12h"
    ONE_DAY = "1d"
    THREE_DAY = "3d"
    ONE_WEEK = "1w"
    ONE_MONTH = "1M"


class BinanceDataAgent:

    def get_data(self, symbol, interval, startTime, endTime):
        self.interval = interval
        ts_start = int(datetime.timestamp(startTime))
        ts_end = int(datetime.timestamp(endTime))

        payload = {'symbol': symbol,
                   'interval': interval,
                   'startTime': f'{ts_start*1000}',  # millisecond
                   'endTime': f'{ts_end*1000}'}
        self.r = requests.get(f"{K_LINE_URL}", params=payload)

    def hour_rounder(self, t):

        return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
                + timedelta(hours=t.minute//30))

    def get_data_frame(self):
        # df = pd.read_json(self.r.text)
        # df.columns = ["OT_" + self.interval, "O_" + self.interval, "H_" + self.interval, "L_" + self.interval, "C_" + self.interval, "V_" + self.interval, "CT_" + self.interval, "V_" + self.interval,
        #               "Trades_" + self.interval, "TakerBaseVol_" + self.interval, "TakerQuoteVol_" + self.interval, "Ignore_" + self.interval]
        # df["OpenDateTime_" + self.interval] = pd.to_datetime(
        #     (df["OT_" + self.interval]/1000), unit='s')  # millisecond
        # df["CloseDateTime_" + self.interval] = pd.to_datetime(
        #     (df["CT_" + self.interval]/1000), unit='s')  # millisecond
        # return df
        jsonResponse = self.r.json()

        df = pd.DataFrame(
            columns=["OT", "CT", "TF", "O", "H", "C", "L", "V", "OpenDT", "CloseDT"])
        for i in range(len(jsonResponse)):
            try:
                value = jsonResponse[i]
                opentime = value[0]
                openprice = value[1]
                highprice = value[2]
                lowprice = value[3]
                closeprice = value[4]
                volume = value[5]
                closetime = value[6]
                openDT = pd.to_datetime(opentime/1000, unit='s')
                closeDT = pd.to_datetime(closetime/1000, unit='s')

                df = df.append({"OT": opentime,
                                "CT": closetime,
                                "TF": self.interval,
                                "O": openprice,
                                "H": highprice,
                                "C": closeprice,
                                "L": lowprice,
                                "V": volume,
                                "OpenDT": openDT,
                                "CloseDT": closeDT

                                }, ignore_index=True)
            except Exception as e:
                print(e)

        return df

    def save_csv(self, df,  file_name):
        df.to_csv("data\\" + file_name+".csv", index=False, sep=";")

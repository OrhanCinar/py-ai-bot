from __future__ import print_function
import json
import gate_api
from gate_api.exceptions import ApiException, GateApiException
import pandas as pd

configuration = gate_api.Configuration(
    host="https://api.gateio.ws/api/v4"
)


api_client = gate_api.ApiClient(configuration)

api_instance = gate_api.SpotApi(api_client)

try:
   
    api_response = api_instance.list_currency_pairs()
    api_response = [p for p in api_response if p.quote == 'USDT' and
                    p.trade_status == 'tradable'
                    and '3S' not in p.id
                    and '3L' not in p.id
                    and '5S' not in p.id
                    and '5L' not in p.id]
    #print(len(api_response))
    for count, pair in enumerate(api_response):
        try:
            klines = api_instance.list_candlesticks(pair.id, limit=500, interval='1h')
            print(count, pair.id)
        except GateApiException as ex:
            print("Gate api exception, label: %s, message: %s\n" %
                  (ex.label, ex.message))
except GateApiException as ex:
    print("Gate api exception, label: %s, message: %s\n" %
          (ex.label, ex.message))
except ApiException as e:
    print("Exception when calling DeliveryApi->list_delivery_contracts: %s\n" % e)

def getTickers():
    tickers = api_instance.list_tickers()
    #tickers.sort(key=lambda x: x.quote_volume, reverse=True)    
    df = pd.DataFrame.from_records([s.to_dict() for s in  tickers])
    df = df[df['currency_pair'].str.contains('_USDT')]
    df = df.astype({'change_percentage': 'float32', 'quote_volume' : 'float32'})
    
    df.sort_values(by=['quote_volume'], inplace=True, ascending=False)
    
    print(df.head(20))   
#oanda
import oandapyV20
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import json
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
import oandapyV20.endpoints.pricing as pricing
import pandas as pd

accountID= str(input("Please enter your account ID:"))
api_key = str(input("Plese enter your api key:"))
api= API(environment="practice", access_token=api_key)

#get histrical data and make DataFrame
#instrumentは通貨 ex)USD_JPY,EUR_USD
#paramsは
params={
  "count": 5,
  "granularity": "M5"
}
def make_dataframe(instrument,params):
    r=instruments.InstrumentsCandles(instrument=instrument,params=params)
    api.request(r)
    df=pd.DataFrame(r.response["candles"])
    return df

#order

#timeInForce
#GTC（Good unTil Cancelled – キャンセルされるまで有効）
#GTD（Good unTil Date – 指定した日付まで有効）
#GFD（Good For Day – 同日のNY時間5PMまで有効）
#FOK（Filled Or Killed – 注文を即時実行または削除）
#IOC（Immediately filled or Cancelled – 即時実行またはキャンセル）
data={
  "order": {
    "price": "120",
    "stopLossOnFill": {
      "timeInForce": "GTC",
      "price": "200"
    },
    "timeInForce": "GTC",
    "instrument": "USD_JPY",
    "units": "+100",
    "type": "LIMIT",
    "positionFill": "DEFAULT"
  }
}
def order_create(data):
    r= orders.OrderCreate(accountID, data=data)
    api.request(r)
    print("注文詳細:",r.response)

#cancellation orders
def cancel_order(target_id):
    r = orders.OrderCancel(accountID= accountID, orderID=target_id)
    api.request(r)
    print("キャンセル結果:",r.response)

#current rate
params={
          "instruments": "USD_JPY"
        }
def current_rate(params):
    r = pricing.PricingInfo(accountID=accountID, params=params)
    rv=api.request(r)
    rv=rv["prices"][0]["bids"][0]["price"]
    return rv

import sys
sys.path.append(r"C:\Python37\Scripts")
import config_acc_testnet as config_acc
from binance.client import Client
from binance.enums import *
import time, ta
import math,btalib
import datetime
import numpy as np
import pandas as pd

#conexion API binance
client = Client()

#Datos de la crypto
symbol = "SHIBBUSD"                                             #CRYPTO/BUSD
candles, candlet = 15, "m"                                      #VELAS tiempo 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
minutesa = candles*300                                          #Cuantas velas atras quieres analizar
candle = str(candles) + candlet                                 #Entrada get_historical_klines 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
minutes = str(minutesa) + " min ago UTC"                        #Entrada get_historical_klines cuanto tiempo atras
bars = client.get_historical_klines(symbol,candle,minutes)      #Regresa las velas

for line in bars:
    del line[5:]


btc_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])
btc_df.set_index('date', inplace=True)
btc_df.index = pd.to_datetime(btc_df.index, unit='ms')
btc_df.index = btc_df.index.tz_localize('UTC').tz_convert('America/Mexico_City')    #Cambio de zona horaria
btc_df = btc_df.astype(float)
print(btc_df.head())

#btc_df['sma'] = btalib.sma(btc_df.close, period=20).df
#print(btc_df.tail())
#rsi = btalib.rsi(btc_df, period=14).mean()
macd = btalib.macd(btc_df.close, pfast=12, pslow=26, psignal=9)
btc_df = btc_df.join([macd.df])
#print(btc_df.tail())

#Indicadores
#btc_df["rsi_ta"] = ta.momentum.rsi(btc_df.close, window = 14)
#btc_df['20sma'] = btc_df.close.rolling(20).mean()
print(btc_df.tail(10))

#Activa señal del MACD, si obtiene mas de cinco velas rojas se activa, TIEMPO REAL!
ALERTA_MACD = False
MACD_COUNT = 0
for i in range(-10,-1,1): #ultimas 8 velas + valor actual 
    btc_df.iloc[i]["histogram"]
    if btc_df.iloc[i]["histogram"] < 0:
        MACD_COUNT += 1
        if MACD_COUNT > 6:
            ALERTA_MACD = True
    else:# btc_df.iloc[i]["histogram"] > 0:
        MACD_COUNT = 0

#BACK TESTING DE ALERTA MACD
#Activa señal del MACD, si obtiene mas de cinco velas rojas se activa, BACKTESTING
ALERTA_MACD = False
MACD_COUNT = 0
btc_df['MACDC_ALERT'] = "NaN"
for i in range(0, len(btc_df)):
    #btc_df.iloc[i]["histogram"]
    if btc_df.iloc[i]["histogram"] < 0:
        MACD_COUNT += 1
        btc_df.iat[i,7] = "Possible"
        if MACD_COUNT > 6:
            ALERTA_MACD = True
            btc_df.iat[i,7] = "TRUE"
    else:# btc_df.iloc[i]["histogram"] > 0:
        MACD_COUNT = 0

#print("DEBUG")
#print(btc_df[btc_df["MACDC_ALERT"] == "TRUE"])
pd.set_option('display.max_column', 6)              #Para ver la tabla completa
pd.set_option('display.max_rows', None)             #Para ver la tabla completa
print(btc_df)
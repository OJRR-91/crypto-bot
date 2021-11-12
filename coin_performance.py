import sys
sys.path.append(r"C:\Python37\Scripts")
import config_acc_testnet as config_acc
from binance.client import Client
from binance.enums import *
import time, ta
import math
import datetime
import numpy as np
import pandas as pd
from tqdm import tqdm
from playsound import playsound

candles = 1
minutesa = candles*24*30
candle = str(candles)+"m"
minutes = str(minutesa) + " min ago UTC"
candle,minutes


def better_coins(candles, minutesa):
    candle = str(candles)+"h"
    minutes = str(minutesa) + " hours ago UTC"
    client = Client()
    info = client.get_exchange_info()
    symbols = [x["symbol"] for x in info["symbols"]]
    exclude = ["UP","DOWN","BEAR","BULL"]
    non_lev = [symbol for symbol in  symbols if all (excludes not in symbol for excludes in exclude)]
    relevant = [symbol for symbol in non_lev if symbol.endswith("BUSD")]
    klines = {}
    for symbol in tqdm(relevant):
        klines[symbol] = client.get_historical_klines(symbol,candle,minutes)
        
    returns, symbols = [],[]
    for symbol in relevant:
        if len(klines[symbol]) > 0:
            cumret = (pd.DataFrame(klines[symbol])[4].astype(float).pct_change() + 1).prod() - 1
            returns.append(cumret)
            symbols.append(symbol)
            
    retdf = pd.DataFrame(returns, index = symbols, columns = ["ret"])
    #playsound('C:\\Windows\\Media\\notify.wav')
    return(retdf)
    


coins = better_coins(candles, minutesa)
playsound('C:\\Windows\\Media\\notify.wav')
coins.ret.nlargest(20)
coins.ret.nsmallest(20)
import sys, btalib, time, math
sys.path.append(r"C:\Python37\Scripts")
from binance.client import Client
from binance.enums import *
import pandas as pd

#########################################################################################
#########################################################################################

#Conexion API binance
client = Client()

#Indicadores
def obtener_velas():
    #Datos de la crypto
    symbol = "SHIBBUSD"                                             #CRYPTO/BUSD
    candles, candlet = 15, "m"                                      #VELAS tiempo 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    minutesa = candles*100                                       #Cuantas velas atras quieres analizar
    candle = str(candles) + candlet                                 #Entrada get_historical_klines 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    minutes = str(minutesa) + " min ago UTC"                        #Entrada get_historical_klines cuanto tiempo atras
    bars = client.get_historical_klines(symbol,candle,minutes)      #Regresa las velas
    for line in bars:
        del line[5:]                                                #Borrar datos para nada mas obtener ['date', 'open', 'high', 'low', 'close']
    btc_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])       #Countruir data frame(tabla), declara nombre de columnas
    btc_df.set_index('date', inplace=True)                                              #Seleccionar columna "date" como index
    btc_df.index = pd.to_datetime(btc_df.index, unit='ms')                              #Cambio de UTC a horario normal HH:MM:SS
    btc_df.index = btc_df.index.tz_localize('UTC').tz_convert('America/Mexico_City')    #Cambio de zona horaria
    btc_df = btc_df.astype(float)
    btc_df = añadir_indicadores(btc_df)
    return btc_df


#########################################################################################
#########################################################################################

#Indicadores
def añadir_indicadores(btc_df):
    #MACD
    macd = btalib.macd(btc_df.close, pfast=12, pslow=26, psignal=9)
    btc_df = btc_df.join([macd.df])
    #Banda bollinger
    bollinger = btalib.BBANDS(btc_df.close, period = 21)
    btc_df = btc_df.join([bollinger.df])
    return btc_df

#########################################################################################
#########################################################################################

#Activa señal del MACD, si obtiene mas de cinco velas rojas se activa, TIEMPO REAL!
def macd_alerta(btc_df):
    ALERTA_MACD = False
    MACD_COUNT = 0
    for i in range(-10,-1,1):                   #ultimas 8 velas + valor actual 
        btc_df.iloc[i]["histogram"]
        if btc_df.iloc[i]["histogram"] < 0:
            MACD_COUNT += 1
            if MACD_COUNT > 6:
                ALERTA_MACD = True
        else:                                   # btc_df.iloc[i]["histogram"] > 0:
            MACD_COUNT = 0
            ALERTA_MACD = False
    return ALERTA_MACD


#########################################################################################
#########################################################################################

#Main loop
def main():
    print(time.ctime(time.time()))
    btc_df = obtener_velas()
    print(btc_df)
    #print(time.ctime(time.time()))
    compra_activa=False         #Agregamos Flag de compra
    cron = True
    while(cron):
        #Realizar chequeo de alertas para comprar
        #print(time.ctime(time.time()))
        #print("cont loop")
        btc_df = obtener_velas()
        #btc_price = client.get_symbol_ticker(symbol = "SHIBBUSD")   #Verificar cada segundo el precio
        #print(btc_df.iloc[-1]["bot"]*0.996 , float(btc_price["price"]))
        if not compra_activa:           #Compra
            if macd_alerta(btc_df):
                #print("MACD -> Bollinger")
                #btc_df = obtener_velas()
                btc_price = client.get_symbol_ticker(symbol = "SHIBBUSD")
                precio_actual = float(btc_price["price"])
                precio_compra = round_down(btc_df.iloc[-1]["bot"]*0.996,8)
                if (precio_compra > precio_actual):
                    print("MACD -> Bollinger -> Compra")          #Falta crear metodo de compra 
                    print(f"{time.ctime(time.time())}\nPrecio actual: {precio_actual}\nPrecio a comprar: {precio_compra}\n")
                    compra_activa = True
                else:
                    print("MACD -> Bollinger") 
                    print(f"{time.ctime(time.time())}\nPrecio actual: {precio_actual}\nPrecio a comprar: {precio_compra}\n")
                    continue
            else:
                print("MACD (Velas verdes)")
                btc_price = client.get_symbol_ticker(symbol = "SHIBBUSD")
                precio_actual = float(btc_price["price"])
                print(f"{time.ctime(time.time())}\nPrecio actual: {precio_actual}\n")
                time.sleep(60)              #esperar 60 segundos
                continue
        elif compra_activa:             #Venta
            print("MACD -> Bollinger -> Compra -> Venta")              #Falta crear metodo de venta
            btc_price = client.get_symbol_ticker(symbol = "SHIBBUSD")
            precio_actual = float(btc_price["price"])
            precio_venta = precio_compra * 1.01             #Ganancia del 1%
            print(f"{time.ctime(time.time())}\nPrecio actual: {precio_actual}\nPrecio a vender: {precio_venta}\n")
            if (precio_venta < precio_actual):
                print("Venta completada") 
                print(f"{time.ctime(time.time())}\nPrecio actual: {precio_actual}\nPrecio de venta: {precio_venta}\n")
        else:
            print("Nothing")
            continue



def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

main()


#########################################################################################
#########################################################################################


#Debug

#print(btc_df.head())
#btc_df['sma'] = btalib.sma(btc_df.close, period=20).df
#print(btc_df.tail())
#rsi = btalib.rsi(btc_df, period=14).mean()
#print(btc_df.tail())

#Indicadores
#btc_df["rsi_ta"] = ta.momentum.rsi(btc_df.close, window = 14)
#btc_df['20sma'] = btc_df.close.rolling(20).mean()
#print(btc_df.tail(10))

#########################################################################################
#########################################################################################

#Activa señal del MACD, si obtiene mas de cinco velas rojas se activa, TIEMPO REAL!

# ALERTA_MACD = False
# MACD_COUNT = 0
# for i in range(-10,-1,1): #ultimas 8 velas + valor actual 
#     btc_df.iloc[i]["histogram"]
#     if btc_df.iloc[i]["histogram"] < 0:
#         MACD_COUNT += 1
#         if MACD_COUNT > 6:
#             ALERTA_MACD = True
#     else:# btc_df.iloc[i]["histogram"] > 0:
#         MACD_COUNT = 0

#BACK TESTING DE ALERTA MACD
#Activa señal del MACD, si obtiene mas de cinco velas rojas se activa, BACKTESTING
# ALERTA_MACD = False
# MACD_COUNT = 0
# btc_df['MACD_ALERT'] = "NaN"
# for i in range(0, len(btc_df)):
#     #btc_df.iloc[i]["histogram"]
#     if btc_df.iloc[i]["histogram"] < 0:
#         MACD_COUNT += 1
#         btc_df.iat[i,10] = "Possible"                   #[i,10]MACD_ALERT
#         if MACD_COUNT > 6:
#             ALERTA_MACD = True
#             btc_df.iat[i,10] = "TRUE"                   #[i,10]MACD_ALERT
#     else:# btc_df.iloc[i]["histogram"] > 0:
#         MACD_COUNT = 0

#########################################################################################
#########################################################################################

#Alerta Bollinger

#BACK TESTING DE ALERTA Bollinger
#Activa señal del Bollinger, se activa al bajar el precio mas del 0.4% por debajo de la banda low , BACKTESTING
#ALERTA_BB = False
def bbands_alert(btc_df, btc_price):
    #btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
    btc_df['BB_ALERT'] = "NaN"
    for i in range(0, len(btc_df)):
        if btc_df.iloc[i]["bot"]*0.996 > float(btc_price["price"]):     #Debajo de 0.4% Activa la señal
            btc_df.iat[i,11] = "TRUE"                       #[i,10]BB_ALERT







#########################################################################################
#########################################################################################

#Alerta Bollinger

#BACK TESTING DE ALERTA Bollinger
#Activa señal del Bollinger, se activa al bajar el precio mas del 0.4% por debajo de la banda low , BACKTESTING
#ALERTA_BB = False

# btc_df['BB_ALERT'] = "NaN"
# btc_df['COMPRAS'] = "NaN"
# btc_df['VENTAS'] = "NaN"
# compra_active = False
# compra = 0
# for i in range(0, len(btc_df)):
#     if not compra_active:
#         if btc_df.iloc[i]["MACD_ALERT"] == "TRUE":
#             if btc_df.iloc[i]["bot"]*0.996 > btc_df.iloc[i]["low"]:     #Debajo de 0.4% Activa la señal y compra
#                 btc_df.iat[i,11] = "TRUE"                       #[i,11]BB_ALERT
#                 btc_df.iat[i,12] = "TRUE"                       #[i,12]COMPRAS
#                 compra = btc_df.iloc[i]["bot"]*0.996
#                 compra_active = True
#                 continue
#     if compra_active:
#         venta = compra*1.01 
#         if (btc_df.iloc[i]["close"] > venta) or (btc_df.iloc[i]["open"] > venta) or (btc_df.iloc[i]["low"] > venta) or (btc_df.iloc[i]["high"] > venta):
#             compra_active = False
#             btc_df.iat[i,13] = "TRUE"
#             print (compra,venta)
        
#########################################################################################
#########################################################################################

#DEBUG

#print("DEBUG")
#print(btc_df[btc_df["MACD_ALERT"] == "TRUE"])
# 

# btc_df[btc_df["BB_ALERT"] == "TRUE"]
#pd.set_option('display.max_column', 6)              #Para ver la tabla completa
#pd.set_option('display.max_rows', None)             #Para ver la tabla completa
#print(btc_df)
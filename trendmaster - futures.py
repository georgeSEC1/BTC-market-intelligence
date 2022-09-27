#copyright - george wagenknecht - Trendmaster - 2022 - all rights reserved
#Poloniex trading bot
# Account Keys
API_KEY = "6322c494eedcca00073eb05a"
SECRET = "9275fd55-0883-4ed8-b501-67197db39715"
API_PASS = input("Please enter account password: ")
modB = 1.0001
modS = 1.0001
taker = 3
import requests
import os
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import tensorflow as tf
from numpy import loadtxt
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import os
from polofutures import RestClient
import traceback

rest_client = RestClient(API_KEY, SECRET, API_PASS)
SYMBOL = 'BTCUSDTPERP'
# Trade Functions
trade = rest_client.trade_api()
var = 8
tRounds = 5
waitTime = 60
print("Trendmaster - 2022")

recordPrev = 2
stat = 0
def download_resource(proc,url,mode):
    try:
        valY = trade.get_position_details("BTCUSDTPERP")['markPrice']
        rx = requests.get(url)
        array = json.loads(rx.content.decode('utf-8'))
        go = 1
        for item in array:
            val1 = item[0]
            val2 = item[1]
            valA = item[2]
            valB = item[3]
            val3 = item[4]
            val4 = item[5]
            val5 = item[6]
            val6 = item[7]
            val7 = item[8]
            #open/close is valA/valB
            if float(valA) < float(valB) and mode == 0:
                recordPrev = 1
                if go == 1:
                    totalPAIR.append(proc)
                go = 0
                xxx.write(str(val1) +","+ str(val2)  +","+str(float(valB))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",1\n")#todo, add more variables
            if float(valA) > float(valB) and mode == 0:
                recordPrev = 0
                if go == 1:
                    totalPAIR.append(proc)
                go = 0
                xxx.write(str(val1) +","+ str(val2)  +","+str(float(valB))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",0\n")#todo, add more variables
            xxx.flush()
            if mode == 1:
                xxxx = open("realtime.csv", "w", encoding="utf8")
                xxxx.write(str(val1) +","+ str(val2)  +","+str(float(valY))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",1\n")#todo, add more variables
                xxxx.write(str(val1) +","+ str(val2)  +","+str(float(valY))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",1\n")#todo, add more variables
                xxxx.flush()
        return rx.status_code
    except requests.exceptions.RequestException as e:
       return e
while(True):
    xxx = open("test.csv", "w", encoding="utf8")
    TotalCheck = []
    totalPAIR = []
    print()
    print("Loading...")
    url_list = []
    r = requests.get("https://poloniex.com/public?command=return24hVolume")#proc.conf
    string = r.text
    TotalCheck = []
    totalPAIR = []
    for line in string.split(","):
        if line.find("_") > -1 and line.find("BTC") > -1:     
            proc = line.split("\"")[1]
            url_list.append("https://api.poloniex.com/markets/"+proc+"/candles?interval=HOUR_1")
            TotalCheck.append(proc)
    threads = []
    with ThreadPoolExecutor(max_workers=200) as executor:
        i = 0
        for url in url_list:
            if i < len(TotalCheck):
                threads.append(executor.submit(download_resource,TotalCheck[i], url,0))
            i+=1
    dataset = loadtxt('test.csv', delimiter=',')
    X = dataset[:,0:var]
    y = dataset[:,var]
    model = Sequential()
    model.add(Dense(120, input_shape=(X.shape[-1],), activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X, y, epochs=150, batch_size=10, verbose=0)
    model.save('my_model')
    cancel_all = trade.cancel_all_limit_orders(SYMBOL)
    time.sleep(1)
    #for PAIR in totalPAIR:
    PAIR = "BTC_USDT"
    url = "https://api.poloniex.com/markets/"+PAIR+"/candles?interval=MONTH_1"
    download_resource(PAIR,url,1)
    dataset = loadtxt('realtime.csv', delimiter=',')
    X = dataset[:,0:var]
    y = dataset[:,var]
    varX = float(X[0][2])
    model = keras.models.load_model('my_model')
    predictions = (model.predict(X) > 0.5).astype(int)
    print ("Price category & movement indicator for:", PAIR)
    print('%s => %d' % (X[0].tolist(), predictions[0]))
    if predictions[0][0] == 0:#TODO: adjust values, fix "invalid price", adjust scaling 
        if varX < 1:
            varZ = "%.8f" % varX
            take = varZ.split('.')[1][-taker:]
            i = 0
            mag = "0."
            while(i+len(str(take)) < len(str(varX))-2):
                mag+="0"
                i+=1
            varI = "%.8f" % (varX+float(mag+str(take)))
            print("Trendmaster could SELL @",varI)
        if varX > 1:
            varI = varX/modS
            varI = "%.2f" % varI
            print("Trendmaster could SELL @",varI)
        try:
            if varX > 1:
                order_id = trade.create_limit_order(SYMBOL, 'sell', '100', '5', str(round(float(varI))))#symbol,side,leverage,quantity,price
                print("SELL @",varI)
        except:
            traceback.print_exc()
    if predictions[0][0] == 1:#TODO: adjust values, fix "invalid price", adjust scaling 
        testVar = 1
        if varX < 1:
            varZ = "%.8f" % varX
            take = varZ.split('.')[1][-3:]
            i = 0
            mag = "0."
            while(i+len(str(taker)) < len(str(varX))-2):
                mag+="0"
                i+=1
            varI = "%.8f" % (varX+float(mag+str(take)))
            print("Trendmaster could BUY @",varI)
        if varX > 1:
            varI = varX*modS
            varI = "%.2f" % varI
            print("Trendmaster could BUY @",varI)
        try:
            if varX > 1:
                order_id = trade.create_limit_order(SYMBOL, 'buy', '100', '5', str(round(float(varI))))#symbol,side,leverage,quantity,price
                print("BUY @",varI)
        except:
            traceback.print_exc()
    if recordPrev == predictions[0][0] and recordPrev != 2:
        stat += 1
        recordPrev = predictions[0][0]
    if recordPrev != predictions[0][0] and recordPrev != 2:
        stat -= 1
        recordPrev = predictions[0][0]
    if recordPrev == 2:
        recordPrev = 0
    print("Theoretical success balance(from 0):" , stat)
    
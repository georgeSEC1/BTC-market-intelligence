#copyright - george wagenknecht - Trendmaster - 2022 - all rights reserved
#Poloniex trading bot
# Account Keys
API_KEY = "633f5806eedcca00073eb6ce"
SECRET = "234d9db3-390a-4339-b732-8b5cd4683bd3"
API_PASS = input("Please enter account password: ")
safetyThreshold = 5#stop trading if balance is under safetyThreshold
modB = 1.0004#Buy multiplier
modS = 1.0004#Sell multiplier
risk = 1#maximum position quantity
taker = 3#dev only
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
market = rest_client.market_api()
user = rest_client.user_api()
var = 8
print("Trendmaster - 2022")
stat = 0
index = 0
instance = 1
def download_resource(proc,url,mode):
    try:
        valY = index 
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
                if go == 1:
                    totalPAIR.append(proc)
                go = 0
                xxx.write(str(val1) +","+ str(val2)  +","+str(float(valA))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",1\n")#todo, add more variables
            if float(valA) > float(valB) and mode == 0:
                if go == 1:
                    totalPAIR.append(proc)
                go = 0
                xxx.write(str(val1) +","+ str(val2)  +","+str(float(valA))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",0\n")#todo, add more variables
            xxx.flush()
            if mode == 1 and url.find("BTC_USDT") > -1:
                xxxx = open("realtime.csv", "w", encoding="utf8")
                xxxx.write(str(val1) +","+ str(val2)  +","+str(float(valY))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",1\n")#todo, add more variables
                xxxx.write(str(val1) +","+ str(val2)  +","+str(float(valY))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",1\n")#todo, add more variables
                xxxx.flush()
        return rx.status_code
    except requests.exceptions.RequestException as e:
       return e
tradeVar = "test"
counter = 0
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
            url_list.append("https://api.poloniex.com/markets/"+proc+"/candles?interval=MINUTE_1")
            TotalCheck.append(proc)
    threads = []
    index = round(float(market.get_ticker("BTCUSDTPERP")['price']))
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
    #for PAIR in totalPAIR:
    PAIR = "BTC_USDT"
    url = "https://api.poloniex.com/markets/"+PAIR+"/candles?interval=MINUTE_1"
    download_resource(PAIR,url,1)
    dataset = loadtxt('realtime.csv', delimiter=',')
    X = dataset[:,0:var]
    y = dataset[:,var]
    varX = float(X[0][2])
    model = keras.models.load_model('my_model')
    predictions = (model.predict(X) > 0.5).astype(int)
    print ("Price category & movement indicator for:", PAIR)
    print('%s => %d' % (X[0].tolist(), predictions[0]))
    checkPos = trade.get_position_details("BTCUSDTPERP")['currentQty']
    availBalance = user.get_account_overview()['availableBalance']
    if counter >= 5:
        trade.cancel_all_stop_orders("BTCUSDTPERP")
        print("Cancelling stale orders")
        counter = 0
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
            if varX > 1 and checkPos > -1 and checkPos < risk:
                order_id = trade.create_limit_order(SYMBOL, 'sell', '100', '1', str(round(float(varI))))#symbol,side,leverage,quantity,price
                print("SELL @",varI)
                counter+=1
                time.sleep(instance)
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
            if varX > 1 and checkPos < 1 and checkPos < risk :
                order_id = trade.create_limit_order(SYMBOL, 'buy', '100', '1', str(round(float(varI))))
                print("BUY @",varI)
                counter+=1
                time.sleep(instance)
        except:
            traceback.print_exc()
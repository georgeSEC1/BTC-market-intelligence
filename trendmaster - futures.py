#copyright - george wagenknecht - Trendmaster - 2022 - all rights reserved
#Poloniex trading bot
print()
print("==================================================================================================")
print()
print("Trendmaster - 2022")
print()
print("==================================================================================================")
print()
#Account Keys
API_KEY = ""
SECRET = ""
API_PASS = input("Please enter account password: ")
safetyThreshold = 1#stop trading if balance is under safetyThreshold
modB = 1.0004#Buy multiplier
modS = 1.0004#Sell multiplier
modG = 2#generic multiplier
leverage = 100
amount = 1
profitLever = 0.01/leverage#Pct
expectanceMultiplier = 10
load = 1
refreshLimit = 50
from playsound import playsound
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
taker = 3#dev only
stat = 0
index = 0
instance = 1
def download_resource(proc,url,mode):#multithreading capable downloader, NN multimode
    try:
        valY = index 
        rx = requests.get(url)#download URL
        array = json.loads(rx.content.decode('utf-8'))
        go = 1
        for item in array:#iterate array
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
                xxx.flush()#flush training data
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
                xxxx.flush()#flush NN ready data, duplicated due to bug
        return rx.status_code
    except requests.exceptions.RequestException as e:#added exception to avoid completely stopping
       return e
counter = 0
refresh = 1
while(True):
    print()
    print("==================================================================================================")
    print()
    index = round(float(market.get_ticker("BTCUSDTPERP")['price']))#Get index price
    if refresh == 1:
        xxx = open("test.csv", "w", encoding="utf8")#prepare file save logic
        TotalCheck = []
        totalPAIR = []
        print()
        print("==================================================================================================")
        print()
        print("Loading...")
        print()
        print("==================================================================================================")
        print()
        url_list = []
        r = requests.get("https://poloniex.com/public?command=return24hVolume")#get volume
        string = r.text
        TotalCheck = []
        totalPAIR = []
        for line in string.split(","):
            if line.find("_") > -1 and line.find("BTC") > -1:     
                proc = line.split("\"")[1]
                url_list.append("https://api.poloniex.com/markets/"+proc+"/candles?interval=MINUTE_1")#get candle data iterator
                TotalCheck.append(proc)
        threads = []
        with ThreadPoolExecutor(max_workers=200) as executor:#multithreading
            i = 0
            for url in url_list:
                if i < len(TotalCheck):
                    threads.append(executor.submit(download_resource,TotalCheck[i], url,0))
                i+=1
        #Neural network training code
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
        #Neural network training code
        refresh = 0
        print()
        print("==================================================================================================")
        print()
    #for PAIR in totalPAIR:
    #Neural network prediction code
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
    #Neural network prediction code
    checkPos = trade.get_position_details("BTCUSDTPERP")['currentQty']#position information
    checkPosX = trade.get_position_details("BTCUSDTPERP")['unrealisedPnl']#position information
    checkPosY = trade.get_position_details("BTCUSDTPERP")['realisedPnl']#position information
    availBalance = user.get_account_overview()['availableBalance']#balance information
    cancel_all = trade.cancel_all_limit_orders("BTCUSDTPERP")
    print(checkPosX)
    if predictions[0][0] == 0:#TODO: adjust values, fix "invalid price", adjust scaling 
        if varX < 1:#alt coin processing
            varZ = "%.8f" % varX
            take = varZ.split('.')[1][-taker:]
            i = 0
            mag = "0."
            while(i+len(str(take)) < len(str(varX))-2):
                mag+="0"
                i+=1
            varI = "%.8f" % (varX+float(mag+str(take)))
            print("Trendmaster could SELL @",varI)
            counter+=1
        if varX > 1:#large coin processing
            varI = varX/modS#adjust price
            varI = "%.2f" % varI
            print("Trendmaster could SELL @",varI)
            counter+=1
        try:
            if varX > 1 and checkPos > load-(load+load) and checkPosX < profitLever and availBalance > safetyThreshold :
                order_id = trade.create_limit_order(SYMBOL, 'sell', leverage, amount, str(round(float(varI))))#symbol,side,leverage,quantity,price
                print("SELL @",varI)
                counter+=1
                time.sleep(instance)
        except:
            traceback.print_exc()#added exception to avoid completely stopping
        print(checkPosX+0.1, (abs(checkPosY)+0.1)*modG)
        if checkPos < load and checkPosX+0.1 > (abs(checkPosY)*modG)+0.1:
            playsound('profit.mp3')
            order_id = trade.create_limit_order(SYMBOL, 'buy', leverage, amount, index)#symbol,side,leverage,quantity,price
            print("Profit made!")
            counter+=1
            time.sleep(instance)
    if predictions[0][0] == 1:#TODO: adjust values, fix "invalid price", adjust scaling 
        testVar = 1
        if varX < 1:#alt coin processing
            varZ = "%.8f" % varX
            take = varZ.split('.')[1][-3:]
            i = 0
            mag = "0."
            while(i+len(str(taker)) < len(str(varX))-2):
                mag+="0"
                i+=1
            varI = "%.8f" % (varX+float(mag+str(take)))
            print("Trendmaster could BUY @",varI)
            counter+=1
        if varX > 1:#large coin processing
            varI = varX*modS#adjust price
            varI = "%.2f" % varI
            print("Trendmaster could BUY @",varI)
            counter+=1
        try:
            if varX > 1 and checkPos < load and checkPosX < profitLever and availBalance > safetyThreshold :
                order_id = trade.create_limit_order(SYMBOL, 'buy', leverage, amount, index)
                print("BUY @",varI)
                counter+=1
                time.sleep(instance)
        except:
            traceback.print_exc()#added exception to avoid completely stopping
        print(checkPosX+0.1, (abs(checkPosY)+0.1)*modG)    
        if checkPos > load-(load+load) and checkPosX+0.1 > (abs(checkPosY)*modG)+0.1:
            playsound('profit.mp3')
            order_id = trade.create_limit_order(SYMBOL, 'sell', leverage, amount, index)#symbol,side,leverage,quantity,price
            print("Profit made!")
            counter+=1
            time.sleep(instance)
    #and checkPosX >= profitLever*expectanceMultiplier #greed function
    if counter >= refreshLimit:
        time.sleep(instance)
        print()
        print("==================================================================================================")
        print()
        print("Refreshing Trendmaster")
        print()
        print("==================================================================================================")
        print()
        refresh = 1
        counter = 0
# -*- coding:utf-8 -*-
#copyright - george wagenknecht - Trendmaster - 2022 - all rights reserved
#Poloniex trading bot
access_key = ""#enter API key
secret_key = ""#enter API secret  
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
import hashlib
import urllib
import urllib.parse
import urllib.request
import requests
import time
import hmac
import base64
import json
class SDK:
    def __init__(self, access_key, secret_key):
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__time = int(time.time() * 1000)
    def __create_sign(self, params, method, path):
        timestamp = self.__time
        if method.upper() == "GET":
            params.update({"signTimestamp": timestamp})
            sorted_params = sorted(params.items(), key=lambda d: d[0], reverse=False)
            encode_params = urllib.parse.urlencode(sorted_params)
            del params["signTimestamp"]
        else:
            requestBody = json.dumps(params)
            encode_params = "requestBody={}&signTimestamp={}".format(
                requestBody, timestamp
            )
        sign_params_first = [method.upper(), path, encode_params]
        sign_params_second = "\n".join(sign_params_first)
        sign_params = sign_params_second.encode(encoding="UTF8")
        secret_key = self.__secret_key.encode(encoding="UTF8")
        digest = hmac.new(secret_key, sign_params, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature
    def sign_req(self, host, path, method, params, headers):
        sign = self.__create_sign(params=params, method=method, path=path)
        headers.update(
            {
                "key": self.__access_key,
                "signTimestamp": str(self.__time),
                "signature": sign,
            }
        )
        if method.upper() == "POST":
            host = "{host}{path}".format(host=host, path=path)
            response = requests.post(host, data=json.dumps(params), headers=headers)
            return response.json()
        if method.upper() == "GET":
            params = urllib.parse.urlencode(params)
            if params == "":
                host = "{host}{path}".format(host=host, path=path)
            else:
                host = "{host}{path}?{params}".format(host=host, path=path, params=params)
            response = requests.get(host, params={}, headers=headers)
            return response.json()
        if method.upper() == "PUT":
            host = "{host}{path}".format(host=host, path=path)
            response = requests.put(host, data=json.dumps(params), headers=headers)
            return response.json()
        if method.upper() == "DELETE":
            host = "{host}{path}".format(host=host, path=path)
            response = requests.delete(host, data=json.dumps(params), headers=headers)
            return response.json()
var = 8
tRounds = 5
waitTime = 60
print("Trendmaster - 2022")
xxx = open("test.csv", "w", encoding="utf8")
TotalCheck = []
totalPAIR = []
def download_resource(proc,url,mode):
    try:
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
            if float(valA) < float(valB) and mode == 0:
                if go == 1:
                    totalPAIR.append(proc)
                go = 0
                xxx.write(str(val1) +","+ str(val2)  +","+str(float(valB))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",1\n")#todo, add more variables
            if float(valA) > float(valB) and mode == 0:
                if go == 1:
                    totalPAIR.append(proc)
                go = 0
                xxx.write(str(val1) +","+ str(val2)  +","+str(float(valA))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",0\n")#todo, add more variables
            xxx.flush()
            if float(valA) < float(valB) and mode == 1:
                xxxx = open("realtime.csv", "w", encoding="utf8")
                xxxx.write(str(val1) +","+ str(val2)  +","+str(float(valB))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",1\n")#todo, add more variables
                xxxx.write(str(val1) +","+ str(val2)  +","+str(float(valB))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",1\n")#todo, add more variables
                xxxx.flush()
            if float(valA) > float(valB) and mode == 1:
                xxxx = open("realtime.csv", "w", encoding="utf8")
                xxxx.write(str(val1) +","+ str(val2)  +","+str(float(valA))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",0\n")#todo, add more variables
                xxxx.write(str(val1) +","+ str(val2)  +","+str(float(valA))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",0\n")#todo, add more variables
                xxxx.flush()
            if float(valA) == float(valB) and mode == 1:
                xxxx = open("realtime.csv", "w", encoding="utf8")
                xxxx.write(str(val1) +","+ str(val2)  +","+str(float(valA))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",0\n")#todo, add more variables
                xxxx.write(str(val1) +","+ str(val2)  +","+str(float(valA))+ ","+str(val3) +","+ str(val4) +","+ str(val5) +","+ str(val6) +","+ str(val7)+ ",0\n")#todo, add more variables
                xxxx.flush()
        return rx.status_code
    except requests.exceptions.RequestException as e:
       return e
while(True):
    headers = {"Content-Type": "application/json"}
    host = "https://api.poloniex.com"
    service = SDK(access_key, secret_key)
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
    print("Crypto pairs:",totalPAIR)
    for PAIR in totalPAIR:
        url = "https://api.poloniex.com/markets/"+PAIR+"/candles?interval=MINUTE_1"
        download_resource(PAIR,url,1)
        dataset = loadtxt('realtime.csv', delimiter=',')
        X = dataset[:,0:var]
        y = dataset[:,var]
        model = keras.models.load_model('my_model')
        predictions = (model.predict(X) > 0.5).astype(int)
        i = 0
        print ("Price category & movement indicator for:", PAIR)
        print('%s => %d' % (X[0].tolist(), predictions[0]))
        try:
            if predictions[0][0] == 0:#TODO: adjust values   
                path_req = "/orders"    
                method_req = "post"    
                params_req = {
                    "symbol": PAIR,
                    "accountType": "spot",
                    "type": "limit",
                    "side": "sell",
                    "timeInForce": "GTC",
                    "price": "1000",
                    "amount": "1",
                    "quantity": "10",
                    "clientOrderId": "",
                }
                res = service.sign_req(
                    host,
                    path_req,
                    method_req,
                    params_req,
                    headers)
                print(res)
            if predictions[0][0] == 1:#TODO: adjust values       
                path_req = "/orders"    
                method_req = "post"    
                params_req = {
                    "symbol": PAIR,
                    "accountType": "spot",
                    "type": "limit",
                    "side": "buy",
                    "timeInForce": "GTC",
                    "price": "1000",
                    "amount": "1",
                    "quantity": "10",
                    "clientOrderId": "",
                }
                res = service.sign_req(
                    host,
                    path_req,
                    method_req,
                    params_req,
                    headers)
                print(res)
        except:
            print("FAILED!")
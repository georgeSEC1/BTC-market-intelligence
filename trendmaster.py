#copyright - george wagenknecht - 2022 - all rights reserved
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
var = 1
tRounds = 5
waitTime = 60
print("Trendmaster - 2022")
xxx = open("test.csv", "w", encoding="utf8")
def download_resource(url):
    try:
        rx = requests.get(url)
        array = json.loads(rx.content.decode('utf-8'))
        for item in array:
            valA = item[2]
            valB = item[3]
            if float(valA) < float(valB):
                xxx.write(str(float(valB)) + ",1\n")#todo, add more variables
            if float(valA) > float(valB):
                xxx.write(str(float(valA)) + ",0\n")#todo, add more variables
            xxx.flush()
        return html.status_code
    except requests.exceptions.RequestException as e:
       return e
waitTime = input("Prediction pace in seconds(default 60): ")
while(True):
    xx = 1
    while(xx <= tRounds):
        print()
        print("Round", str(xx))
        url_list = []
        r = requests.get("https://poloniex.com/public?command=return24hVolume")#proc.conf
        string = r.text
        for line in string.split(","):
            if line.find("_") > -1 and line.find("BTC") > -1:     
                proc = line.split("\"")[1]
                url_list.append("https://api.poloniex.com/markets/"+proc+"/candles?interval=MINUTE_1")
        threads = []
        with ThreadPoolExecutor(max_workers=200) as executor:
            for url in url_list:
                threads.append(executor.submit(download_resource, url))
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
        xxx = open("realtime.csv", "w", encoding="utf8")
        xxx.write("1000,0\n")#todo, add more variables
        xxx.write("100,0\n")#todo, add more variables
        xxx.write("10,0\n")#todo, add more variables
        xxx.write("1,0\n")#todo, add more variables
        xxx.write("0.1,0\n")#todo, add more variables
        xxx.write("0.01,0\n")#todo, add more variables
        xxx.write("0.001,0\n")#todo, add more variables
        xxx.write("0.0001,0\n")#todo, add more variables
        xxx.close()
        time.sleep(1)
        dataset = loadtxt('realtime.csv', delimiter=',')
        X = dataset[:,0:var]
        y = dataset[:,var]
        model = keras.models.load_model('my_model')
        predictions = (model.predict(X) > 0.5).astype(int)
        i = 0
        print ("Price category & movement indicator:")
        while(i < len(dataset)):
            print('%s => %d' % (X[i].tolist(), predictions[i]))
            i+=1
        xx+=1
        print("Waiting for", str(waitTime), "seconds...")
        time.sleep(int(waitTime))
    print()
    print("Refreshing...")
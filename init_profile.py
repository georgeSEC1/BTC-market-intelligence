#copyright - george wagenknecht - 2022 - all rights reserved
import datetime
import random
import json
import subprocess
import time
import re
import pandas
import os
loadTime = 5
option = input("prepare for realtime(work in progress, needs catagorical pair approach...)?[y/n]:")
def produce(string):
    array = string.split(",")
    i = 0
    db = []
    temp = 0
    for segment in array:
        if segment.find("\'block_time\': ") > -1:
            db.append(int(segment.split(":")[1]))
    return db
def produceaddr(string):
    array = string.split(",")
    i = 0
    db = []
    temp = 0
    for segment in array:
        if segment.find("\'addresses\': [\'") > -1:
            proc =segment.split(":")[2]
            db.append(proc)
            break
    return db
os.system('CLS')
optionB = ""
#optionB = input("Preprocess valuable addresses?[y/n]: ")
if optionB == "y":
    with open("blockchair_bitcoin_addresses_and_balance_LATEST.tsv", encoding='UTF-8') as f:
            lines = f.readlines()
    i = 0
    threshold = 1000000000#input("threshold above range(e.g 10000000000): ")
    output_path='previous_transactions_detail.csv'
    for line in lines:
        proc = line.split("\t")
        if len(proc) > 1 and i > 0 and line.find("-") == -1:
            if int(proc[1]) > int(threshold):          
                your_btc_address = proc[0]
                transactions_url = 'https://chain.api.btc.com/v3/address/' + your_btc_address +'/tx'
                df = pandas.read_json(transactions_url)
                if i == 1:
                    df.to_csv(output_path, mode='a', header=not os.path.exists(output_path))
                if i > 1:
                    df.to_csv(output_path, mode='a', header=False)
                os.system('CLS')
                print("Retrieving address transactions:",i,"/",len(lines))# monitor transactions for stock movements
        i+=1
time.sleep(loadTime)
xx = 1
while(True):
    unixTime = int(time.time())
    os.system('CLS')
    print("Begin round", str(xx))
    time.sleep(loadTime)
    os.system('CLS')
    print("Preparing profile")
    subprocess.Popen("curl -s \"https://poloniex.com/public?command=return24hVolume\" -o proc.conf")
    i = 0
    instance = str(random.randint(0,10000000))
    time.sleep(loadTime)
    os.system('CLS')
    subprocess.Popen("del *.dat /q",shell=True)
    with open('proc.conf') as f:
        string = f.read()
    for line in string.split(","):
        if line.find("_") > -1 and line.find("BTC") > -1:
            proc = line.split("\"")[1]
            os.system('CLS')
            print ("Loading" ,proc)
            subprocess.Popen("curl -s \"https://api.poloniex.com/markets/"+proc+"/candles?interval=MINUTE_5\" -o " + proc + "_" + instance +".dat")
    time.sleep(loadTime)
    subprocess.Popen("dir /b *.dat > market.conf",shell=True)
    time.sleep(loadTime)
    btcA = 10000#input("BTC above amount(e.g 100000): ")
    def produce(string):
        array = string.split(",")
        i = 0
        db = []
        temp = 0
        for segment in array:
            if segment.find("\'value\': ") > -1:
                db.append(int(segment.split(":")[1]))
        return db
    with open("proc.conf", encoding='UTF-8') as f:
        lines = f.readlines()
        var = ""
        for line in lines:
            if line.find("totalBTC") > -1:
                var = (line[16:len(line)-3])
                break
    with open('market.conf') as f:
        lines = f.readlines()
    statA = 0
    statB = 0
    os.system('CLS')
    print("Analysing market movement")
    if option == "n":
        xxx = open("test.csv", "a", encoding="utf8")
    if option == "y":
        xxx = open("realtime.csv", "a", encoding="utf8")
    for line in lines:
        with open(line.strip()) as f:
            linesX = f.readlines()
            for lineX in linesX:
                proc = lineX.split(",")
                valA = proc[2][2:-1]
                valB = proc[3][2:-1]
                if float(valA) < float(valB):
                    xxx.write(str(float(valB)) + ",1\n")#todo, add more variables
                if float(valA) > float(valB):
                    xxx.write(str(float(valA)) + ",0\n")#todo, add more variables
    #copyright - george wagenknecht - 2022 - all rights reserved
    time.sleep(loadTime)
    os.system('CLS')
    print("Training data constructed")
    xx+=1
    time.sleep(loadTime)

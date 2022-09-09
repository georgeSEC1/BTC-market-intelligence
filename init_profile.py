#copyright - george wagenknecht - 2022 - all rights reserved
import datetime
import random
import json
import subprocess
import time
import re
import pandas
import os
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
option = input("Preprocess valuable addresses?[y/n]: ")
if option == "y":
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
time.sleep(5)

xx = 1
while(True):
    unixTime = int(time.time())
    os.system('CLS')
    print("Begin round", str(xx))
    time.sleep(5)
    subprocess.Popen("del *.btc /q",shell=True)
    with open("previous_transactions_detail.csv", encoding='UTF-8') as f:
        lines = f.readlines()
    time.sleep(1)
    os.system('CLS')
    print("Preparing profile")
    subprocess.Popen("curl -s \"https://poloniex.com/public?command=return24hVolume\" -o proc.conf")
    i = 0
    instance = str(random.randint(0,10000000))
    time.sleep(5)
    os.system('CLS')
    f = open("bitcoin_contempory_addr_associate.btc", "a", encoding="utf8")
    print("Analysing addresses")
    for line in lines:
        if line.find("\'block_time\': ") > -1:
            array = produce(line)
            for segment in array:
                if int(segment) > int(unixTime) and int(segment) < int(unixTime)+3600:#unix time specification, assign to blockchain time
                    addrs = produceaddr(line)
                    for addr in addrs:
                        f.write(addr + line)
        i += 1
    time.sleep(5)
    subprocess.Popen("del *.dat /q",shell=True)
    with open('proc.conf') as f:
        string = f.read()
    for line in string.split(","):
        if line.find("_") > -1 and line.find("BTC") > -1:
            proc = line.split("\"")[1]
            os.system('CLS')
            print ("Loading" ,proc)
            subprocess.Popen("curl -s \"https://api.poloniex.com/markets/"+proc+"/candles?interval=MINUTE_5\" -o " + proc + "_" + instance +".dat")
    time.sleep(5)
    subprocess.Popen("dir /b *.dat > market.conf",shell=True)
    time.sleep(5)
    with open('market.conf') as f:
        lines = f.readlines()
    statA = 0
    statB = 0
    os.system('CLS')
    print("Analysing market movement")
    for line in lines:
        with open(line.strip()) as f:
            linesX = f.readlines()
            for lineX in linesX:
                proc = lineX.split(",")
                valA = re.sub('\W+',' ',proc[2])
                valB = re.sub('\W+',' ',proc[3])
                if valA < valB:
                    statA+=1
                if valA > valB:
                    statB+=1
    #copyright - george wagenknecht - 2022 - all rights reserved
    time.sleep(5)
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
    def getValuesOverX(seg):
        lines = seg.split(",")
        i = 0
        for line in lines:
            if line.find("\'value\': ") > -1:
                array = produce(line)
                for segment in array:
                    if int(segment) > int(btcA):#btc amount
                        i+=1
        return str(i)
    i = 0
    with open("bitcoin_contempory_addr_associate.btc", encoding='UTF-8') as f:#e.g "bitcoin_contempory_addr_associate_4920994.dat"
        procX = f.readlines()
    with open("proc.conf", encoding='UTF-8') as f:
        lines = f.readlines()
        var = ""
        for line in lines:
            if line.find("totalBTC") > -1:
                var = (line[16:len(line)-3])
                break
    for proc in procX:
        f = open("test.csv", "a", encoding="utf8")
        if statA > statB:
            f.write(str(unixTime) +"," + str(round(float(var))) +","+ getValuesOverX(proc) + ",0\n")
        if statA < statB:
            f.write(str(unixTime) +"," + str(round(float(var))) +","+ getValuesOverX(proc) + ",1\n")
        i+=1
    os.system('CLS')
    print("Training data constructed")
    xx+=1
    time.sleep(1)

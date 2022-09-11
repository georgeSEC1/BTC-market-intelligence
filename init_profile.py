#copyright - george wagenknecht - 2022 - all rights reserved
import requests
import os
loadTime = 5
xx = 1
print("init_profile - Trendmaster - 2022")
print()
xxx = open("test.csv", "w", encoding="utf8")
while(True):
    print("Begin round", str(xx))
    print()
    r = requests.get("https://poloniex.com/public?command=return24hVolume")#proc.conf
    string = r.text
    for line in string.split(","):
        if line.find("_") > -1 and line.find("BTC") > -1:
            proc = line.split("\"")[1]
            print ("Loading" ,proc)
            rx = requests.get("https://api.poloniex.com/markets/"+proc+"/candles?interval=MINUTE_5")
            proc = rx.text.split(",")
            valA = proc[2][2:-1]
            valB = proc[3][2:-1]
            print("Open: " + valA + " Close: " + valB)
            if float(valA) < float(valB):
                xxx.write(str(float(valB)) + ",1\n")#todo, add more variables
            if float(valA) > float(valB):
                xxx.write(str(float(valA)) + ",0\n")#todo, add more variables
            xxx.flush()
    print("Training data constructed")
    xx+=1

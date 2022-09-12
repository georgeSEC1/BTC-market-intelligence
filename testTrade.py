#copyright - george wagenknecht - 2022 - all rights reserved
import requests
import hashlib
import time
import base64
import re 
timeStamp = str(int( time.time() ))
APIkey = "Y3KG6MET-IY5UX6P3-AL0HJMVI-DBG92NCQ"
Limit = str(5)
Symbol="ETH_USDT"
string="POST\n/orders\nsymbol="+Symbol+ "&limit="+Limit+"&signTimestamp="+timeStamp
sha256_encoded_string=hashlib.sha256(string.encode('utf8')).hexdigest()
b64encoded_string = base64.b64encode(sha256_encoded_string.encode('utf8'))
url = "https://api.poloniex.com/orders"
myobj = {'key': APIkey,'signatureMethod': 'hmacSHA256','signatureVersion': '1','signTimestamp': timeStamp ,'signature': b64encoded_string.decode(encoding="utf-8")}
print (myobj)
x = requests.post(url, json = myobj)
print(x.status_code)
print(x.text)
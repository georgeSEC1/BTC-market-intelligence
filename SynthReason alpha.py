# SynthReason - Synthetic Dawn - Intelligent symbolic manipulation
# BSD 2-Clause License
# 
# Copyright (c) 2022, GeorgeSEC1 - George Wagenknecht
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import random
import re
import math
from scipy import optimize
from scipy.spatial import distance
grip = 0
token = "."
size = 125
attempts = 10000
targetNgramSize = 3
data = []
dataX =""
def convert(lst):
    return (lst.split())
def convertB(lst):
    process = lst.split(" ")
    db = []
    total = ""
    for index in process:
        total += index + " "
        if len(index) < targetNgramSize:
            db.append(total)
            total = ""
    return db
def est(data, ini):
    i = ini
    while(i > 0 ):
        try:
            if data[i].find(token,ini) > -1:
                return i
            i-=1
        except:
            return ini
    return ini
def formatSentences(sync):
    sentences = sync.split(".")
    i = 0
    total = ""
    for sentence in sentences:
        total += sentence + ". " 
    proc = convert(total)
    totalB = ""
    n = 0
    while(n < len(proc)-7):
        if proc[n] != proc[n+1] and proc[n] != proc[n+2] and proc[n] != proc[n+3] and proc[n] != proc[n+4] and proc[n] != proc[n+5] and proc[n] != proc[n+6] :
            totalB += proc[n] + " "
        n+=1
    return totalB[:-1] + "."
def gather(user,file):
    with open(file, encoding='ISO-8859-1') as f:
        text = f.read()
    sentences = text.split(token)
    data = text.split(" ")
    output = ""
    i = 0
    words = convert(user)
    while(i < len(sentences)-1):
        if len(sentences[i]) > 0 and i <len(sentences):
            for word in words:
                if sentences[i].find(" " + word + " ") > -1:
                    output += sentences[i] +token
        i+=1
    return output
def returnWords(dataX,pos,length):
    ngram = ""
    n = 0
    while(n < length and pos+length < len(dataX)-1):
        if pos+n < len(dataX)-2 and pos+n > 0:
            ngram += dataX[pos+n] + " "
        n+=1
    return ngram
def proc(data, string):
    i = 0
    while(i < 100):
        try:
            ini = random.randint(1,len(data))
            var = convertB(string)[random.randint(0,len(convert(string))-1)]
            if len(var) > grip:
                return data.index(var,est(data,ini))
        except:
            i+=1
    return random.randint(1,len(data))
def function(x, a, b):
   return math.lgamma(b)*x+a
with open("fileList.conf", encoding='ISO-8859-1') as f:
    files = f.readlines()
    print("SynthReason - Synthetic Dawn")
    with open("questions.conf", encoding='ISO-8859-1') as f:
    	questions = f.readlines()
    filename = "Compendium#" + str(random.randint(0,10000000)) + ".txt"
    random.shuffle(questions)
    for question in questions:
        print()
        user = re.sub('\W+',' ',question)
        random.shuffle(files)
        for file in files: 
            sync = ""
            counter = 0
            try:
                counter+=1
                data = convertB(gather(user,file.strip()))
                dataX = gather(user,file.strip())
            except:
                counter+=1
            if len(dataX) > 100:
                ini = random.randint(1,len(data))
                while(counter < attempts):
                    counter += 1
                    if len(data) > 100:
                        xp = []
                        fp = []
                        for index in range(8):
                            xp.append(proc(data,user))
                        for index in range(8):
                            fp.append(proc(data,sync))
                        p , e = optimize.curve_fit(function, fp, xp,maxfev = 1000000)
                        x = distance.minkowski(xp, fp, 2)
                        for plx in p:
                            if math.isnan(x) == False and math.isnan(plx) == False:
                                string = returnWords(data,est(data, round(x))+round(plx),targetNgramSize)
                                if sync.find(string) == -1:
                                    sync += string
                                    counter = 0
                                if len(convert(sync)) >= size or counter > attempts:
                                    break
                    if len(convert(sync)) >= size or counter > attempts:
                        break
            if len(convert(sync)) >= size or counter > attempts:
                break
        print()
        sync = formatSentences(sync.replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('-', '').replace('(', '').replace(')', ''))
        print("using " , file.strip() ,  " answering: " , user)
        print("AI:" ,sync)
        f = open(filename, "a", encoding="utf8")
        f.write("\n")
        f.write("using " + file.strip() + " answering: " + user)
        f.write("\n")
        f.write(sync)
        f.write("\n")
        f.close()
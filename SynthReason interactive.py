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
from difflib import SequenceMatcher
import math
import statistics as stats
size = 128
targetNgramSize = 3
token = "."
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
def convert(lst):
    return (lst.split())
def num_to_range(num, inMin, inMax, outMin, outMax):
    return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax - outMin))
def gather(user,file):
    with open(file, encoding='ISO-8859-1') as f:
        text = f.read()
    output = ""
    words = convert(user)
    sentences = text.split(token)
    for word in words:
        for sentence in sentences:
            if sentence.find(" " + word + " ") > -1:
                output += sentence + token
    return output 
def returnWords(dataX,pos,length):
    ngram = ""
    n = 0
    while(n < length and pos+length < len(dataX)-1):
        if pos+n < len(dataX)-2 and pos+n > 0:
            ngram += dataX[pos+n] + " "
        n+=1
    return ngram
with open("fileList.conf", encoding='ISO-8859-1') as f:
    files = f.readlines()
    print("SynthReason - Synthetic Dawn")
    with open("questions.conf", encoding='ISO-8859-1') as f:
    	questions = f.readlines()
    filename = "Compendium#" + str(random.randint(0,10000000)) + ".txt"
    random.shuffle(questions)
    for question in questions:
        print()
        user = re.sub('\W+',' ',input("USER: "))
        random.shuffle(files)
        for file in files:
            data = convert(gather(user,file.strip()))
            if len(data) > 100:
                sentences = []
                db = []
                var = random.randint(0,len(data)-1)
                for i in range(size):
                    db.append(similar(user, returnWords(data,var+i,targetNgramSize)))
                    db.append(similar(returnWords(data,var,targetNgramSize), returnWords(data,var+i,targetNgramSize)))
                x = list(set(db).intersection(db)) 
                textualFeedback = ' '.join(sentences)
                for i in x:
                    n = 0
                    for j in db:
                        n=i+textualFeedback.find(data[round(num_to_range(i, 0, 1, 0, len(data)-1))])
                        sentences.append(returnWords(data,round(num_to_range(j, 0, 1, 0, len(data)-1)),targetNgramSize))
                sync = ""
                sentences = list(set(sentences))
                for line in sentences:
                    sync += ''.join(str(line)).replace('\n', '').replace('\'', '').replace('  ', ' ').replace('\"', '').replace('//', '').replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('-', '').replace('(', '').replace(')', '')
                print()
                print("using " , file.strip() ,  " answering: " , user)
                print("AI:" ,sync)
                f = open(filename, "a", encoding="utf8")
                f.write("\n")
                f.write("using " + file.strip() + " answering: " + user)
                f.write("\n")
                f.write(sync)
                f.write("\n")
                f.close()
                if len(convert(sync)) >= 0:
                    break
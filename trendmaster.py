from numpy import loadtxt
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import random
import time
import subprocess
var = 1
while(True):
    option = input("Train or predict?[t/p]:")
    if option == "t":
        dataset = loadtxt('test.csv', delimiter=',')
        X = dataset[:,0:var]
        y = dataset[:,var]
        model = Sequential()
        model.add(Dense(120, input_shape=(X.shape[-1],), activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(X, y, epochs=150, batch_size=10, verbose=1)
        model.save('my_model')
    if option == "p":
        subprocess.Popen("del realtime.csv /q",shell=True)
        time.sleep(1)
        xxx = open("realtime.csv", "a", encoding="utf8")
        print()
        xxx.write("10000,0\n")#todo, add more variables
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
        print ("Volume category & movement indicator:")
        while(i < len(dataset)):
            print('%s => %d' % (X[i].tolist(), predictions[i]))
            i+=1
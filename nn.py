# first neural network with keras make predictions
from numpy import loadtxt
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import random

# load the dataset
option = input("train or predict?[t/p]:")
if option == "t":
    dataset = loadtxt('test.csv', delimiter=',')
    # split into input (X) and output (y) variables
    X = dataset[:,0:3]
    y = dataset[:,2]
    # define the keras model
    model = Sequential()
    model.add(Dense(120, input_shape=(3,), activation='relu'))
    model.add(Dense(50, activation='sigmoid'))
    model.add(Dense(1, activation='relu'))
    # compile the keras model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # fit the keras model on the dataset
    model.fit(X, y, epochs=100, batch_size=10, verbose=1)
    model.save('my_model')
if option == "p":
    dataset = loadtxt('realtime.csv', delimiter=',')
    # split into input (X) and output (y) variables
    X = dataset[:,0:3]
    model = keras.models.load_model('my_model')
    # make class predictions with the model
    predictions = (model.predict(X)).astype(int)
    # summarize the first 5 cases
    for i in range(len(dataset)):
        print('%s => %d ' % (X[i].tolist(), predictions[i]))
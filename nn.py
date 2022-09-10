# first neural network with keras make predictions
from numpy import loadtxt
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import random
# load the dataset
var = 1
option = input("train or predict?[t/p]:")
if option == "t":
    dataset = loadtxt('test.csv', delimiter=',')
    # split into input (X) and output (y) variables
    X = dataset[:,0:var]
    y = dataset[:,var]
    # define the keras model
    model = Sequential()
    model.add(Dense(120, input_shape=(X.shape[-1],), activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # compile the keras model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # fit the keras model on the dataset
    model.fit(X, y, epochs=250, batch_size=10, verbose=1)
    model.save('my_model')
if option == "p":
    dataset = loadtxt('realtime.csv', delimiter=',')
    # split into input (X) and output (y) variables
    X = dataset[:,0:var]
    model = keras.models.load_model('my_model')
    # make class predictions with the model
    predictions = (model.predict(X) > 0.5).astype(int)# summarize the first 5 cases
    for i in range(len(dataset)):
        print('%s => %d ' % (X[i].tolist(), predictions[i]))
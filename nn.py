# first neural network with keras make predictions
from numpy import loadtxt
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
# load the dataset
option = input("train or predict?[t/p]:")
if option == "t":
    dataset = loadtxt('trainingdata.csv', delimiter=',')
    # split into input (X) and output (y) variables
    X = dataset[:,0:5]
    y = dataset[:,5]
    # define the keras model
    model = Sequential()
    model.add(Dense(12, input_shape=(5,), activation='relu'))
    model.add(Dense(5, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # compile the keras model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # fit the keras model on the dataset
    model.fit(X, y, epochs=1500, batch_size=10, verbose=1)
    model.save('my_model')
if option == "p":
    dataset = loadtxt('profile.csv', delimiter=',')
    # split into input (X) and output (y) variables
    X = dataset[:,0:5]
    model = keras.models.load_model('my_model')
    # make class predictions with the model
    predictions = (model.predict(X) > 0.5).astype(int)
    # summarize the first 5 cases
    datasetB = loadtxt('trainingdata.csv', delimiter=',')
    # split into input (X) and output (y) variables
    X = dataset[:,0:5]
    yB = datasetB[:,5]
    for i in range(5):
        print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], yB[i]))
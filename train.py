import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM
import h5py


file_path = 'abc/datafile.txt'

Data = open(file_path,'r').read()
data = Data[:100000]

# list of unique characters in the data
chars=list(set(data))
# length of the character vocabulary we have
vocabulary_size = len(chars)
# no of neurons in the hidden layer
hidden_dim = 100
# no. of characters in one sequence.. one sequence is an input to one neural network
sequence_len = 25

# mapping from char to int, to convert abc to numbers which can be predicted
char_to_index = dict((c, i) for i, c in enumerate(chars))
# mapping from int to char.. will be used in the end, to convert numbers back to abc notation
index_to_char = dict((i, c) for i, c in enumerate(chars))


# X_train is a 3D np array
X_train = np.zeros((len(data),sequence_len,vocabulary_size))
# for a sequence, y_train stores the next character index
y_train = np.zeros((len(data),vocabulary_size))

# stores different sequences possible
time_seq = []
# stores their corresponding next characters
next_char = []

for i in range(0, len(data)-sequence_len):
    time_seq.append(data[i:i+sequence_len])
    next_char.append(data[i+sequence_len])

# making X_train and y_train one hot vectors
for i, sequence in enumerate(time_seq):
    for t, c in enumerate(sequence):
        X_train[i, t, char_to_index[c]] = 1
    y_train[i, char_to_index[next_char[i]]] = 1


model = Sequential()
model.add(LSTM(100,input_shape=(sequence_len, vocabulary_size)))
model.add(Dense(vocabulary_size))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',optimizer='adagrad')
model.load_weights("./fluteweight.h5")


model.fit(X_train,y_train,batch_size=64,nb_epoch=650)


model_json = model.to_json()
model_name = 'model0.json'
with open(model_name,'w') as jsonfile:
    jsonfile.write(model_json)
weight_name = 'finalweight0.h5'
model.save_weights(weight_name)

import numpy as np
import keras
import random
import sys
import Prediction_to_ABC
import Convert_MidiABC

def predict_abc(choice,dur,tempo,meter,key):

    data_file = 'abc/datafile.txt'
    Data = open(data_file,'r').read()
    data = Data[:50000]

    # list of unique characters in the data
    chars=list(set(data))
    # length of the character vocabulary we have
    vocabulary_size = len(chars)
    # no. of characters in one sequence.. one sequence is an input to one neural network
    sequence_len = 25
    # len of characters to be predicted and printed
    
    if dur=="Short":
        len_to_print = 500
    elif dur=="Medium":
        len_to_print = 2000
    else:
        len_to_print = 5000
    

    #------------------------------MAPPING------------------------------


    # mapping from char to int, to convert abc to numbers which can be predicted
    char_to_index = dict((c, i) for i, c in enumerate(chars))
    # mapping from int to char.. will be used in the end, to convert numbers back to abc notation
    index_to_char = dict((i, c) for i, c in enumerate(chars))


    #-------------------------------------------------------------------
    
    model_name = './model0.json'
    json_file = open(model_name, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = keras.models.model_from_json(loaded_model_json)
    weight_name = './finalweight0.h5'
    loaded_model.load_weights(weight_name)
    
    text=""
    while 1:
        start_index=random.randint(0,len(data)-sequence_len-1)
        if(Prediction_to_ABC.validnote(data[start_index]) and Prediction_to_ABC.validnote(data[start_index+sequence_len-1])):
            text=data[start_index:start_index+sequence_len]
            break

    pred_text=text
    print("Seed: ",text)

    for i in range(len_to_print):

        X_pred = np.zeros((1, sequence_len, vocabulary_size))

        for t, c in enumerate(text):
            X_pred[0, t, char_to_index[c]]=1

        prob = loaded_model.predict(X_pred)[-1]
        #prob = np.random.multinomial(1, np.asarray(pred_index*0.999).astype('float64'), 1)
        next_index = np.argmax(prob)
        next_char = index_to_char[next_index]
        text = text[1:] + next_char
        pred_text = pred_text + next_char
        
    
    print (dur,tempo,meter,key)
#-------------------------------------------------------------------

    valid_abc = Prediction_to_ABC.convert(choice,pred_text,tempo,meter,key)
    gp = open("abc.txt", "w")
    gp.write(valid_abc)
    gp.close()

    filename = Convert_MidiABC.abc2midi("abc.txt")
    
    
    
    
    


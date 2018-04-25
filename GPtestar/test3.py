
from __future__ import print_function

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import matplotlib.pyplot as plt
import os
import numpy as np
import tensorflow as tf
from tensorflow.contrib import rnn
import random
import collections
import time
import sys
import math as m
import plotter

warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

start_time = time.time()
def elapsed(sec):
    if sec<60:
        return str(sec) + " sec"
    elif sec<(60*60):
        return str(sec/60) + " min"
    else:
        return str(sec/(60*60)) + " hr"

# Data
training_file_name = "arithmetic2.dat"
validation_file_name = None #if left as None a fraction of the trainingdata will be used for validation instead
fraction_as_validation = 0.1

# Parameters
learning_rate = 0.001
training_iters = 50000
save_step = 1000
display_step = 10000
n_input = 10

# number of units in RNN cell
n_hidden = 1024

# number or layers in the network
nr_of_layers = 2


# Target log path
logs_path = '/tmp/tensorflow/rnn_words'
writer = tf.summary.FileWriter(logs_path)

def importData(trainingFileName, validFileName = None):
    trainingFile = open(trainingFileName, "r")
    trainingSet = []
    splitChar = " "
    lines = trainingFile.readlines()
    lines = list(map(lambda x: x[:-1], lines))
    trainingFile.close()
    header = lines.pop(0)

    splitCharPos = header.find("splitChar:")
    if splitCharPos != -1 and splitCharPos+10 < len(header):
        splitChar = header[splitCharPos+10]
    
    actionListPos = header.find("actionList:")
    if actionListPos != -1:
        actionList = ["RETURN"]
        pos = 11+actionListPos
        while pos < len(header) and header[pos] != splitChar:
            actionList.append(header[pos])
            pos += 1

    chars = []
    charsPos = header.find("chars:")
    if charsPos != -1:
        pos = charsPos+6
        while pos < len(header) and header[pos] != splitChar:
            chars.append(header[pos])
            pos += 1

    for line in lines:
        i = line.index(splitChar)
        trainingSet.append((line[:i], line[i+1:]))
    
    validSet = []
    if validFileName != None:
        validFile = open(validFileName, "r")
        for line in validFile:
            i = line.index(splitChar)
            validSet.append((line[:i], line[i+1:]))
        validFile.close()
    else:
        for n in range(m.ceil(len(trainingSet)*fraction_as_validation)):
            i = random.randrange(0, len(trainingSet))
            validSet.append(trainingSet.pop(i))

    return (trainingSet, validSet, chars)

(dataSet, validSet, chars) = importData(training_file_name, validation_file_name)
char = 1
char_to_id = {"R":0}
for x in chars:
    char_to_id[x] = char
    char += 1


#char_to_id = {
#    "D":0,
#    "*":11,
#    "=":12,
#    "R":13,
#    "+":14
#}

#for x in range(10):
#    char_to_id[str(x)] = x+1

id_to_char = {}
for x in char_to_id:
    id_to_char[char_to_id[x]] = x

vocab_size = len(char_to_id)

print(vocab_size)

data = [(list(map(lambda x: char_to_id[x],i)), list(map(lambda x: char_to_id[x],j))) for (i,j) in dataSet]
valid = [(list(map(lambda x: char_to_id[x],i)), list(map(lambda x: char_to_id[x],j))) for (i,j) in validSet]
for (inp, out) in data:
    out.append(0)
for (inp,out) in valid:
    out.append(0)



# Dataset for multiplication with two and three numbers

#for x in range(10):
#    for y in range(10):
#        data.append(list(map(lambda x: char_to_id[x], "{}*{}={}R".format(x,y,x*y))))
#    for y in range(10):
#        for z in range(10):
#            data.append(list(map(lambda x: char_to_id[x], "{}*{}*{}={}R".format(x,y,z,x*y*z))))



# Dataset for multiplication and addition with three numbers, randomly selected

#oprL = ['*', '+']
#for x in range(1000):
#    a = random.randint(0,9)
#    b = random.randint(0,9)
#    c = random.randint(0,9)
#    o1 = random.randint(0,1)
#    o2 = random.randint(0,1)
#    
#    if o1 == 0:
#        if o2 == 0:
#            result = a*b*c
#        else:
#            result = a*b+c
#    else:
#        if o2 == 0:
#            result = a+b*c
#        else:
#            result = a+b+c
#    
#    data.append(list(map(lambda x: char_to_id[x], "{}{}{}{}{}={}R".format(a,oprL[o1],b,oprL[o2],c,result))))


# Dataset for boolean logic algebra

#oprL = ['+', '*'] # * = AND + = OR
#for x in range(2):
#    for y in range(2):
#        for z in range(2):
#            for v in range(2):
#                for w in range(2):
#                    for h in range(2):
#                        for g in range(2):
#                            if y:
#                                result = x==z
#                            else:
#                                result = x or z
#                            if v:
#                                result = result==w
#                            else:
#                                result = result or w
#                            if h:
#                                result = result==g
#                            else:
#                                result = result or g
#                            data.append(list(map(lambda x: char_to_id[x], "{}{}{}{}{}{}{}={}R".format(x,oprL[y],z,oprL[v],w,oprL[h],g,result*1))))
#
#
#testData = [
#  #  list(map(lambda x: char_to_id[x], "7*7=49R")),
#  #  list(map(lambda x: char_to_id[x], "3*0=0R")),
#  #  list(map(lambda x: char_to_id[x], "5*4=20R")),
#  #  list(map(lambda x: char_to_id[x], "5*4*0=0R")),
#  #  list(map(lambda x: char_to_id[x], "1*2*3=6R")),
#  #  list(map(lambda x: char_to_id[x], "3*2+4=10R"))
#    list(map(lambda x: char_to_id[x], "1+0+0+0=1R")),
#    list(map(lambda x: char_to_id[x], "1*1+0+0=1R")),
#    list(map(lambda x: char_to_id[x], "1*0*1+0=0R"))
#]
#
##try:
#    #data.remove(list(map(lambda x: char_to_id[x], "7*7=49R")))
#    #data.remove(list(map(lambda x: char_to_id[x], "3*0=0R")))
#    #data.remove(list(map(lambda x: char_to_id[x], "5*4=20R")))
#    #data.remove(list(map(lambda x: char_to_id[x], "5*4*0=0R")))
#    #data.remove(list(map(lambda x: char_to_id[x], "1*2*3=6R")))
#    #data.remove(list(map(lambda x: char_to_id[x], "3*2+4=10R")))
#
#print(data)
#print(list(map(lambda x: char_to_id[x], "1+0+0+0=1R")))
#data.remove(list(map(lambda x: char_to_id[x], "1+0+0+0=1R")))
#data.remove(list(map(lambda x: char_to_id[x], "1*1+0+0=1R")))
#data.remove(list(map(lambda x: char_to_id[x], "1*0*1+0=0R")))
##except ValueError:
#    print("who cares")


# tf Graph input
x = tf.placeholder("float", [None, n_input, 1])
y = tf.placeholder("float", [None, vocab_size])

# RNN output node weights and biases
weights = {
    'out': tf.Variable(tf.random_normal([n_hidden, vocab_size]))
}
biases = {
    'out': tf.Variable(tf.random_normal([vocab_size]))
}

def plot_accuracy(xs, ys):
    plt.clf()
    plt.plot(xs, ys)
    plt.axis([0,int(training_iters/display_step),0,100])
    xLabels = np.arange(0,training_iters+display_step, display_step)
    xTLabels = [""]*int(training_iters/display_step+1)
    for x in range(int(training_iters/display_step)+1):
        if x % 20 == 0: #How often we want the label written
            xTLabels[x] = str(xLabels[x])
        else:
            xTLabels[x] = ""
    plt.xticks(range(int(training_iters/display_step)+1),xTLabels)
    plt.ylabel('Accuracy')
    plt.xlabel('Training Iterations')
    plt.title('3 Layers, 1024 hidden units, 0.001 learning rate')
    plt.grid(True)
    plt.savefig('accuracy')

def RNN(x, weights, biases):

    # reshape to [1, n_input]
    x = tf.reshape(x, [-1, n_input])

    # Generate a n_input-element sequence of inputs
    # (eg. [had] [a] [general] -> [20] [6] [33])
    x = tf.split(x,n_input,1)

    # 2-layer LSTM, each layer has n_hidden units.
    # Average Accuracy= 95.20% at 50k iter
   # rnn_cell = rnn.MultiRNNCell([rnn.BasicLSTMCell(n_hidden),rnn.BasicLSTMCell(n_hidden)])
    layers = [rnn.BasicLSTMCell(n_hidden) for x in range(nr_of_layers)]
    rnn_cell = rnn.MultiRNNCell(layers)
   # rnn_cell = rnn.MultiRNNCell([rnn.BasicLSTMCell(n_hidden),rnn.BasicLSTMCell(n_hidden),rnn.BasicLSTMCell(n_hidden)])
    
    # 1-layer LSTM with n_hidden units but with lower accuracy.
    # Average Accuracy= 90.60% 50k iter
    # Uncomment line below to test but comment out the 2-layer rnn.MultiRNNCell above
    # rnn_cell = rnn.BasicLSTMCell(n_hidden)

    # generate prediction
    outputs, states = rnn.static_rnn(rnn_cell, x, dtype=tf.float32)

    # there are n_input outputs but
    # we only want the last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']

pred = RNN(x, weights, biases)

# Loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Model evaluation
correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Initializing the variables
init = tf.global_variables_initializer()

# Launch the graph
with tf.Session() as session:
    session.run(init)
    step = 0
    offset = random.randint(0,n_input+1)
    end_offset = n_input + 1
    acc_total = 0
    loss_total = 0
    accList = [0]
    validCorrectList = [0]
    iterationList = [0]

    writer.add_graph(session.graph)

    while step < training_iters:
        #symbols_in_keys = [ [dictionary[ str(training_data[i])]] for i in range(offset, offset+n_input) ]
        #symbols_in_keys = np.reshape(np.array(symbols_in_keys), [-1, n_input, 1])
       
        (inp, expected_out) = random.choice(data)
        end = random.randrange(len(expected_out))
        
        in_symbols = inp + expected_out[:end]
        in_length = len(in_symbols)
        if in_length > n_input:
            in_symbols = in_symbols[in_length-n_input:]
            in_length = n_input
        out_symbol = expected_out[end]

        symbols_in_keys = np.zeros([n_input])
        symbols_in_keys[n_input-in_length: n_input] = in_symbols
        symbols_in_keys = np.reshape(symbols_in_keys, [-1, n_input, 1])

        #symbols_out_onehot = np.zeros([vocab_size], dtype=float)
        #symbols_out_onehot[dictionary[str(training_data[offset+n_input])]] = 1.0
        #symbols_out_onehot = np.reshape(symbols_out_onehot,[1,-1])

        symbols_out_onehot = np.zeros([vocab_size], dtype=float)
        symbols_out_onehot[out_symbol] = 1.0
        symbols_out_onehot = np.reshape(symbols_out_onehot,[1,-1])

        _, acc, loss, onehot_pred = session.run([optimizer, accuracy, cost, pred], \
                                                feed_dict={x: symbols_in_keys, y: symbols_out_onehot})
        loss_total += loss
        acc_total += acc
        if (step+1) % display_step == 0:
            print("Iter= " + str(step+1) + ", Average Loss= " + \
                  "{:.6f}".format(loss_total/display_step) + ", Average Accuracy= " + \
                  "{:.2f}%".format(100*acc_total/display_step))
            accList.append(int(100*acc_total/display_step))
            acc_total = 0
            loss_total = 0

            correct = 0
            for (inp, expected_out) in valid:
                end = random.randrange(len(expected_out))
                
                in_symbols = inp + expected_out[:end]
                in_length = len(in_symbols)
                if in_length > n_input:
                    in_symbols = in_symbols[in_length-n_input:]
                    in_length = n_input
                expected_out_symbol = expected_out[end]
                
                symbols_in_keys = np.zeros([n_input])
                symbols_in_keys[n_input-in_length: n_input] = in_symbols
                symbols_in_keys = np.reshape(symbols_in_keys, [-1, n_input, 1])
                
                onehot_red = session.run(pred, feed_dict = {x: symbols_in_keys})
                out_symbol = tf.argmax(onehot_pred, 1).eval()

                if out_symbol == expected_out_symbol:
                    correct +=1
            validCorrectList.append(int(correct*100/len(valid)))
            iterationList.append(step)
            
            print("Percent correct guesses on validation data: {}%".format(correct*100/len(valid)))
                
                #symbolsT = id_to_char
                #end = random.randint(len(expected_out))
                #symbols_in_keys = np.zeros([n_input])
                #symbols_in_keys[n_input-len(symbols[0:end]):n_input] = list(symbols[0:end])
                #keys = np.reshape(np.array(symbols_in_keys), [-1, n_input, 1])
                #onehot_pred = session.run(pred, feed_dict = {x: keys})
                #symbols_in = list(map(lambda x: id_to_char[x], symbols[0:end]))#[training_data[i] for i in range(offset, offset + n_input)]
                #symbols_out = id_to_char[symbols[end]]#training_data[offset + n_input]
                #symbols_out_pred = id_to_char[int(tf.argmax(onehot_pred, 1).eval())]
                #print("%s - [%s] vs [%s]" % (symbols_in,symbols_out,symbols_out_pred))
      #  else:
      #      if step == 0:
      #          accList.append(0)
      #      else:
      #          accList.append(accList[step-1])
        step += 1
        offset += (n_input+1)
    plot_accuracy(range(int(training_iters/display_step)+1), accList)
    plotter.improvedPlot(iterationList, accList, title = "Accuracy on training set", xlabel = "Iterations", ylabel = "Accuracy", figname = training_file_name[:-4]+"training.fig")
    plotter.improvedPlot(iterationList, validCorrectList, title = "Accuracy on validation set", xlabel = "Iterations", ylabel = "Accuracy", figname = training_file_name[:-4]+"validation.fig")
    print("Plot completed")
    print("Optimization Finished!")
    print("Elapsed time: ", elapsed(time.time() - start_time))
    print("Run on command line.")
    print("\ttensorboard --logdir=%s" % (logs_path))
    print("Point your web browser to: http://localhost:6006/")
#    while True:
#        prompt = "what to multiply"
#        sentence = input(prompt)
#        sentence = sentence.strip()
#        words = list(sentence)
#        if len(words) != 4:
#            continue
#        out_symbol = ""
#        while out_symbol != "R":
#            symbols_in_keys = np.zeros([n_input])#[dictionary[str(words[i])] for i in range(len(words))]
#            symbols_in_keys[n_input-len(words):n_input] = list(map(lambda x: char_to_id[x], words))
#            keys = np.reshape(np.array(symbols_in_keys), [-1, n_input, 1])
#            onehot_pred = session.run(pred, feed_dict={x: keys})
#            onehot_pred_index = int(tf.argmax(onehot_pred, 1).eval())
#            out_symbol = id_to_char[onehot_pred_index]
#            sentence = "%s %s" % (sentence,out_symbol)
#            words.append(out_symbol)
#        print(sentence)
#



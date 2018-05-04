
from __future__ import print_function

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import plotter
import importer
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

def RNN(x, weights, biases, n_input):

    # reshape to [1, n_input]
    x = tf.reshape(x, [-1, n_input])

    # Generate a n_input-element sequence of inputs
    # (eg. [had] [a] [general] -> [20] [6] [33])
    x = tf.split(x,n_input,1)

    #An multi layer LSTM network
    layers = [rnn.BasicLSTMCell(n_hidden) for x in range(nr_of_layers)]
    rnn_cell = rnn.MultiRNNCell(layers)
    
    # generate prediction
    outputs, states = rnn.static_rnn(rnn_cell, x, dtype=tf.float32)

    # there are n_input outputs but
    # we only want the last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']


def run_lstm_test(training_file_name, fraction_as_validation = 0.1,  training_iters = 300000, nr_of_layers = 3, n_hidden = 512):
        
    # Data
    #training_file_name = "arithmetic2.dat"
    validation_file_name = None #if left as None a fraction of the trainingdata will be used for validation instead
    #fraction_as_validation = 0.2
    
    # Parameters
    learning_rate = 0.001
    #training_iters = 300000
    #display_step = 10000
    display_step = m.ceil(training_iters/30)
    n_input = 10
    
    # number of units in RNN cell
    #n_hidden = 512
    
    # number or layers in the network
    #nr_of_layers = 3
    
    info = "Dataset: {}\nFraction used for validation: {}\nNumber of iterations: {}\nHidden units per layer: {}\nNumber of layers: {}\nLearning rate: {}".format(training_file_name[:-4], fraction_as_validation, training_iters, n_hidden, nr_of_layers, learning_rate)
    info_short = "{}_{}_{}_{}_{}_{}".format(training_file_name[:-4], fraction_as_validation, training_iters, n_hidden, nr_of_layers, learning_rate)
    
    # Target log path
    logs_path = '/tmp/tensorflow/rnn_words'
    writer = tf.summary.FileWriter(logs_path)
    
    (dataSet, validSet, chars, actionList, id_to_word) = importer.importData(training_file_name, validation_file_name, fraction_as_validation)
    
    num = 0
    char_to_id = {"R":len(chars)}
    for char in chars:
        char_to_id[char] = num
        num += 1
    
    id_to_char = {}
    for x in char_to_id:
        id_to_char[char_to_id[x]] = x
    
    vocab_size = len(char_to_id)
    
    data = [(list(map(lambda x: char_to_id[x],i)), list(map(lambda x: char_to_id[x],j))) for (i,j) in dataSet]
    valid = [(list(map(lambda x: char_to_id[x],i)), list(map(lambda x: char_to_id[x],j))) for (i,j) in validSet]
    for (inp, out) in data:
        out.append(char_to_id["R"])
    for (inp,out) in valid:
        out.append(char_to_id["R"])
    
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
    
    
    pred = RNN(x, weights, biases, n_input)
    out_symbol_pred = tf.argmax(pred, 1)
    
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
        steps = 0
    
        writer.add_graph(session.graph)
    
        while step < training_iters:
            (inp, expected_out) = random.choice(data)
            for end in range(len(expected_out)):
                steps += 1
                in_symbols = inp + expected_out[:end]
                in_length = len(in_symbols)
                if in_length > n_input:
                    in_symbols = in_symbols[in_length-n_input:]
                    in_length = n_input
                out_symbol = expected_out[end]
    
                symbols_in_keys = np.zeros([n_input])
                symbols_in_keys[n_input-in_length: n_input] = in_symbols
                symbols_in_keys = np.reshape(symbols_in_keys, [-1, n_input, 1])
    
                symbols_out_onehot = np.zeros([vocab_size], dtype=float)
                symbols_out_onehot[out_symbol] = 1.0
                symbols_out_onehot = np.reshape(symbols_out_onehot,[1,-1])
    
                _, acc, loss, onehot_pred, prediction = session.run([optimizer, accuracy, cost, pred, out_symbol_pred], \
                                                        feed_dict={x: symbols_in_keys, y: symbols_out_onehot})
    
                loss_total += loss
                acc_total += acc
    
                if prediction.item(0) != out_symbol:
                    break
            if step % display_step == 0:
                print("Iter= " + str(step+1) + ", Average Loss= " + \
                      "{:.6f}".format(loss_total/steps) + ", Average Accuracy= " + \
                      "{:.2f}%".format(100*acc_total/steps))
                accList.append(int(100*acc_total/steps))
                acc_total = 0
                loss_total = 0
                steps = 0
    
                correct = 0
                for (inp, expected_out) in valid:
                    for end in range(len(expected_out)):
                    
                        in_symbols = inp + expected_out[:end]
                        in_length = len(in_symbols)
                        if in_length > n_input:
                            in_symbols = in_symbols[in_length-n_input:]
                            in_length = n_input
                        expected_out_symbol = expected_out[end]
                    
                        symbols_in_keys = np.zeros([n_input])
                        symbols_in_keys[n_input-in_length: n_input] = in_symbols
                        symbols_in_keys = np.reshape(symbols_in_keys, [-1, n_input, 1])
                    
                        out_symbol = session.run(out_symbol_pred, feed_dict = {x: symbols_in_keys})
    
                        if out_symbol.item(0) == expected_out_symbol:
                            if id_to_char[out_symbol.item(0)] == "R":
                                correct +=1
                                break
                        else:
                            break
                validCorrectList.append(int(correct*100/len(valid)))
                iterationList.append(step)
                
                print("Percent correct guesses on validation data: {}%".format(correct*100/len(valid)))
            step += 1
            offset += (n_input+1)
        plotter.improvedPlot(iterationList, accList, title = "Accuracy on training set\n"+info, xlabel = "Iterations", ylabel = "Accuracy", figname = info_short+"_training.png")
        plotter.improvedPlot(iterationList, validCorrectList, title = "Accuracy on validation set\n"+info, xlabel = "Iterations", ylabel = "Accuracy", figname = info_short+"validation.png")
        print("Plot completed")
        print("Optimization Finished!")
        print("Elapsed time: ", elapsed(time.time() - start_time))
        print("Run on command line.")
        print("\ttensorboard --logdir=%s" % (logs_path))
        print("Point your web browser to: http://localhost:6006/")
        return (iterationList, validCorrectList, info_short) 
    

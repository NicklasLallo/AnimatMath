
from __future__ import print_function

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import numpy as np
import tensorflow as tf
from tensorflow.contrib import rnn
import random
import collections
import time
import sys

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


# Target log path
logs_path = '/tmp/tensorflow/rnn_words'
writer = tf.summary.FileWriter(logs_path)

# Text file containing words for training
training_file = 'belling_the_cat.txt'

def read_data(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    content = [content[i].split() for i in range(len(content))]
    content = np.array(content)
    content = np.reshape(content, [-1, ])
    return content

training_data = read_data(training_file)
print("Loaded training data...")

char_to_id = {
    "D":0,
    "*":11,
    "=":12,
    "R":13
}

for x in range(10):
    char_to_id[str(x)] = x+1

id_to_char = {}
for x in char_to_id:
    id_to_char[char_to_id[x]] = x

vocab_size = len(char_to_id)

print(vocab_size)

data = []

for x in range(10):
    for y in range(10):
        data.append(list(map(lambda x: char_to_id[x], "{}*{}={}R".format(x,y,x*y))))

def build_dataset(words):
    count = collections.Counter(words).most_common()
    dictionary = dict()
    for word, _ in count:
        dictionary[word] = len(dictionary)
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return dictionary, reverse_dictionary

dictionary, reverse_dictionary = build_dataset(training_data)
vocab_size = len(dictionary)
vocab_size = len(char_to_id)

# Parameters
learning_rate = 0.001
training_iters = 50000
display_step = 1000
n_input = 7

# number of units in RNN cell
n_hidden = 1024

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

def RNN(x, weights, biases):

    # reshape to [1, n_input]
    x = tf.reshape(x, [-1, n_input])

    # Generate a n_input-element sequence of inputs
    # (eg. [had] [a] [general] -> [20] [6] [33])
    x = tf.split(x,n_input,1)

    # 2-layer LSTM, each layer has n_hidden units.
    # Average Accuracy= 95.20% at 50k iter
    # rnn_cell = rnn.MultiRNNCell([rnn.BasicLSTMCell(n_hidden),rnn.BasicLSTMCell(n_hidden)])
    rnn_cell = rnn.MultiRNNCell([rnn.BasicLSTMCell(n_hidden),rnn.BasicLSTMCell(n_hidden),rnn.BasicLSTMCell(n_hidden)])

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
optimizer = tf.train.RMSPropOptimizer(learning_rate=learning_rate).minimize(cost)

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

    writer.add_graph(session.graph)

    while step < training_iters:
        # Generate a minibatch. Add some randomness on selection process.
        if offset > (len(training_data)-end_offset):
            offset = random.randint(0, n_input+1)

        #symbols_in_keys = [ [dictionary[ str(training_data[i])]] for i in range(offset, offset+n_input) ]
        #symbols_in_keys = np.reshape(np.array(symbols_in_keys), [-1, n_input, 1])
        
        symbols = np.array(random.choice(data))
        
        end = random.randint(4, len(symbols)-1)

        symbols_in_keys = np.zeros([n_input])
        symbols_in_keys[n_input-end: n_input] = symbols[0:end] 
        symbols_in_keys = np.reshape(symbols_in_keys, [-1, n_input, 1])

        #symbols_out_onehot = np.zeros([vocab_size], dtype=float)
        #symbols_out_onehot[dictionary[str(training_data[offset+n_input])]] = 1.0
        #symbols_out_onehot = np.reshape(symbols_out_onehot,[1,-1])

        symbols_out_onehot = np.zeros([vocab_size], dtype=float)
        symbols_out_onehot[symbols[end]] = 1.0
        symbols_out_onehot = np.reshape(symbols_out_onehot,[1,-1])

        _, acc, loss, onehot_pred = session.run([optimizer, accuracy, cost, pred], \
                                                feed_dict={x: symbols_in_keys, y: symbols_out_onehot})
        loss_total += loss
        acc_total += acc
        if (step+1) % display_step == 0:
            print("Iter= " + str(step+1) + ", Average Loss= " + \
                  "{:.6f}".format(loss_total/display_step) + ", Average Accuracy= " + \
                  "{:.2f}%".format(100*acc_total/display_step))
            acc_total = 0
            loss_total = 0
            symbols_in = list(map(lambda x: id_to_char[x], symbols[0:end]))#[training_data[i] for i in range(offset, offset + n_input)]
            symbols_out = id_to_char[symbols[end]]#training_data[offset + n_input]
            symbols_out_pred = id_to_char[int(tf.argmax(onehot_pred, 1).eval())]
            print("%s - [%s] vs [%s]" % (symbols_in,symbols_out,symbols_out_pred))
        step += 1
        offset += (n_input+1)
    print("Optimization Finished!")
    print("Elapsed time: ", elapsed(time.time() - start_time))
    print("Run on command line.")
    print("\ttensorboard --logdir=%s" % (logs_path))
    print("Point your web browser to: http://localhost:6006/")
    while True:
        prompt = "what to multiply"
        sentence = input(prompt)
        sentence = sentence.strip()
        words = list(sentence)
        if len(words) != 4:
            continue
        out_symbol = ""
        while out_symbol != "R":
            symbols_in_keys = np.zeros([n_input])#[dictionary[str(words[i])] for i in range(len(words))]
            symbols_in_keys[n_input-len(words):n_input] = list(map(lambda x: char_to_id[x], words))
            keys = np.reshape(np.array(symbols_in_keys), [-1, n_input, 1])
            onehot_pred = session.run(pred, feed_dict={x: keys})
            onehot_pred_index = int(tf.argmax(onehot_pred, 1).eval())
            out_symbol = id_to_char[onehot_pred_index]
            sentence = "%s %s" % (sentence,out_symbol)
            words.append(out_symbol)
        print(sentence)


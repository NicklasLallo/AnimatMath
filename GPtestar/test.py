import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import numpy as np
    import tensorflow as tf

import random as r


char_to_id = {
    "*":10,
    "=":11
}

for x in range(10):
    char_to_id[str(x)] = x

vocab_size = len(char_to_id)

print(vocab_size)

data = []

for x in range(10):
    for y in range(10):
        data.append(list(map(lambda x: char_to_id[x], "{}*{}={}".format(x,y,x*y))))



n_inputs = 4

n_hidden = 128
rnn_cell = tf.contrib.rnn.BasicLSTMCell(n_hidden)

w = tf.Variable(tf.random_normal([n_hidden, vocab_size]))
b = tf.Variable(tf.random_normal([vocab_size]))

x = tf.placeholder("float", [None, n_inputs, 1])
y = tf.placeholder("float", [None, vocab_size])

x = tf.reshape(x, [-1, n_inputs])
x = tf.split(x, n_inputs, 1)


outputs, states = tf.contrib.rnn.static_rnn(rnn_cell, x, dtype = tf.float32)

pred = tf.matmul(outputs[-1], w + b)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = pred, labels = y))
optimizer = tf.train.RMSPropOptimizer(learning_rate = 0.01).minimize(cost)

correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.global_variables_initializer()

with tf.Session() as session:
    session.run(init)
    
    for iteration in range(10000):


        symbols = [r.choice(data) for i in range(20)]

        symbols_in_keys = list(map(lambda x: x[0:4], symbols))
        symbols_in_keys = np.reshape(np.array(symbols_in_keys), [20, -1])

        symbols_out_onehot = np.zeros([vocab_size, 20], dtype = float)
        print(np.shape(symbols_out_onehot))
        for x in range(20):
            symbols_out_onehot[symbols[x][4],x] = 1.0
        symbols_out_onehot = np.reshape(symbols_out_onehot, [-1, 20])

        print(symbols_out_onehot)
        print(symbols_in_keys)

        _, acc, onehot_pred = session.run([optimizer, accuracy, pred], feed_dict = {x: symbols_in_keys, y: symbols_out_onehot})

        if iteration % 1000 == 0:
            print(acc)







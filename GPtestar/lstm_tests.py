
from lstm_test import *
import pickle
import os.path


repetitions = 8

favs = [0.1, 0.5, 0.9]
trainingFileNames = ["arithmetic1.dat", "arithmetic1.dat", "arithmetic1.dat"]
nr_of_layers = 3
neurons_per_layer = 512
training_iterations = 300000

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


if not os.path.exists("lstm_data.pkl"):
    data = {}
    save_obj(data, "lstm_data")
else:
    data = load_obj("lstm_data")

for x in range(len(favs)):
    averageYs = None
    minYs = None
    maxYs = None
    if (favs[x], trainingFileNames[x], nr_of_layers, neurons_per_layer, training_iterations) not in data:
        data[(favs[x], trainingFileNames[x], nr_of_layers, neurons_per_layer, training_iterations)] = []
    if ("Acc",favs[x], trainingFileNames[x], nr_of_layers, neurons_per_layer, training_iterations) not in data:
        data[("Acc",favs[x], trainingFileNames[x], nr_of_layers, neurons_per_layer, training_iterations)] = []
    for y in range(repetitions):
        (xs, ys, zs, info) = run_lstm_test(training_file_name = trainingFileNames[x], fraction_as_validation = favs[x],  training_iters = training_iterations, nr_of_layers = nr_of_layers, n_hidden = neurons_per_layer)
        #(xs, ys, info) = run_learner_test(fraction_as_validation = favs[x], trainingFileName = trainingFileNames[x], answer_maxlen = answer_maxlens[x], abstracter_depth = abstracter_depths[x])
        data[(favs[x], trainingFileNames[x], nr_of_layers, neurons_per_layer, training_iterations)].append((xs, ys, info)) 
        data[("Acc",favs[x], trainingFileNames[x], nr_of_layers, neurons_per_layer, training_iterations)].append((zs, ys, info)) 
        save_obj(data, "lstm_data")

        if averageYs == None:
            averageYs = [0]*len(ys)
            minYs = [0]*len(ys)
            maxYs = [0]*len(ys)
        for num in range(len(ys)):
            averageYs[num] += ys[num]
            minYs[num] = min(minYs[num], ys[num])
            maxYs[num] = max(maxYs[num], ys[num])
    averageYs = [x/repetitions for x in averageYs]
    plotter.improvedPlot(xs, averageYs, title = info+"_"+str(repetitions), xlabel = "Iteration", ylabel = "Average accuracy", figname = "AvgModel_" + info + "_" + str(repetitions) + ".png")

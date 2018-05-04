
from lstm_test import *
import pickle
import os.path


repetitions = 20

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


if not os.path.exists("model_data.pkl"):
    data = {}
    save_obj(data, "model_data")
else:
    data = load_obj("model_data")

for x in range(len(favs)):
    averageYs = None
    minYs = None
    maxYs = None
    if (favs[x], answer_maxlens[x], abstracter_depths[x]) not in data:
        data[(favs[x], answer_maxlens[x], abstracter_depths[x])] = []
    for y in range(repetitions):
        (xs, ys, info) = run_learner_test(fraction_as_validation = favs[x], trainingFileName = trainingFileNames[x], answer_maxlen = answer_maxlens[x], abstracter_depth = abstracter_depths[x])
        data[(favs[x], answer_maxlens[x], abstracter_depths[x])].append((xs, ys, info)) 
        save_obj(data, "model_data")

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

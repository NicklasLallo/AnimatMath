import pickle
import os.path
import plotter

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

print("What .plk file should be read? (Do not need to specify .plk as ending)")
f = input()
data = load_obj(f)

for collection in data.values():
    (xs, ys, info) = collection[0]
    avgYs = [0]*len(ys)
    minYs = [9999]*len(ys)
    maxYs = [-9999]*len(ys)
    for (xs, ys, info) in collection:
        avgYs = [avgYs[num] + ys[num] for num in range(len(ys))]
        minYs = [min(minYs[num], ys[num]) for num in range(len(ys))]
        maxYs = [max(maxYs[num], ys[num]) for num in range(len(ys))]
    avgYs = [y/len(collection) for y in avgYs]
    plotter.improvedErrplot(xs, avgYs, xerrs = [0]*len(xs), yerrs = [maxYs, minYs], title = info+"_"+str(len(collection)), xlabel = "Iteration", ylabel = "Average accuracy", figname = "Avg" + f + "_" + info + "_" + str(len(collection)) + ".png")
    









    










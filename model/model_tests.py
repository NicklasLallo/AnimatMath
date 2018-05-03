from learner_test import *

repetitions = 5

favs = [0.1, 0.5, 0.9]
trainingFileNames = ["arithmetic1.dat", "arithmetic1.dat", "arithmetic1.dat"]
answer_maxlens = [3,3,3]
abstracter_depths = [2,2,2]

for x in range(len(favs)):
    averageYs = None
    for y in range(repetitions):
        (xs, ys, info) = run_learner_test(fraction_as_validation = favs[x], trainingFileName = trainingFileNames[x], answer_maxlen = answer_maxlens[x], abstracter_depth = abstracter_depths[x])
        if averageYs == None:
            averageYs = [0]*len(ys)
        for num in range(len(ys)):
            averageYs[num] += ys[num]
    averageYs = [x/repetitions for x in averageYs]
    plotter.improvedPlot(xs, averageYs, title = info+"_"+str(repetitions), xlabel = "Iteration", ylabel = "Average accuracy", figname = "AvgModel_" + info + "_" + str(repetitions) + ".png")

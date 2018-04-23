import matplotlib.pyplot as plt
import math
import numpy as np

def plot(xs, ys, xaxis = [0, 100], yaxis = [0, 100], title = "", xlabel = "", ylabel = "", figname = "untitled"):
    plt.clf()
    plt.plot(xs, ys)
    plt.axis(xaxis+yaxis) #([0,int(training_iters/display_step),0,100])
    #xLabels = range(0,training_iters+display_step, display_step)
    #xTLabels = [""]*int(training_iters/display_step+1)
    
    #for x in range(int(training_iters/display_step)+1):
    #    if x % 20 == 0: #How often we want the label written
    #        xTLabels[x] = str(xLabels[x])
    #    else:
    #        xTLabels[x] = ""
    
    #xnums = map(str, np.linspace(xaxis[0], xaxis[1], xticks))
    #ynums = map(str, np.linspace(yaxis[0], yaxis[1], yticks))
    
    #plt.xticks(range(int(training_iters/display_step)+1),xTLabels)
    #plt.xticks(range(xticks), xnums)
    
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.grid(True)
    plt.savefig(figname)

def improvedPlot(xs, ys, title = "", xlabel = "", ylabel = "", figname = "untitled"):
    xaxis = [min(xs),max(xs)]
    yaxis = [min(ys),max(ys)]
    plot(xs, ys, xaxis, yaxis, title, xlabel, ylabel, figname)
    




#improvedPlot(range(0, 3000000000,10000000), list(map(math.sin, range(0,3000000000, 10000000))))

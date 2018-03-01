import random as r
from Brain import *

actionList = ["RETURN", "1", "0", "2"]

#This is trinary
trainingSet = [
    "1+1=2",
    "0+0=0",
    "0+1=1",
    "1+0=1",
    "0+2=2",
    "2+0=2",
    "1+2=10",
    "2+1=10",
    "2+2=11"
]

exploreRate = 0.1

animat = Brain(actionList, 0.5, 0.9)

for x in range(100):
    for y in range(1000):
        expr = r.choice(trainingSet)
        action = animat.simpleMultiStateProgram(expr, 4, exploreRate)
        while True:
            if action == "RETURN":
                reward = -1
                if expr in trainingSet:
                    reward = 1
                a = animat.simpleMultiStateProgram(expr, 0, 0, "RETURN", reward)
                break
            expr += action
            action = animat.simpleMultiStateProgram(expr,4,exploreRate,action,0)
            
    correct = 0
    for expr in trainingSet:
        exor = expr[:-1]
        action = animat.simpleMultiStateProgram(expr, 4, 0)
        while True:
            if action == "RETURN":
                if expr in trainingSet:
                    correct += 1
                else:
                    print(expr)
                break
            expr += action
            action = animat.simpleMultiStateProgram(expr,4,0)
    print(correct/len(trainingSet))

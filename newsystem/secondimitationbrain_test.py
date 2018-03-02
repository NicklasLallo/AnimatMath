import random as r
from Brain import *

actionList = ["RETURN", ">>>", "1", "0", "2"]

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

exploreRate = 1

depth = 4

animat = Brain(actionList, 0.5, 0.9)

for x in range(20):
    for y in range(10000):
        expression = str(r.choice(trainingSet))
        position = 0
        expr = expression[0]
        action = animat.simpleMultiStateProgram(expr, depth, exploreRate)
        while True:
            reward = 0
            if action == "RETURN":
                reward = -1
                if expr in trainingSet:
                    reward = 1
                a = animat.simpleMultiStateProgram(expr+"D", 0, 0, "RETURN", reward)
                break
            elif action == ">>>":
                if position+1 < len(expression): 
                    position += 1
                expr += expression[position]
                reward = 0.1
            else:
                expr += action
            action = animat.simpleMultiStateProgram(expr,depth,exploreRate,action,reward)
            
    correct = 0
    for expression in trainingSet:
        expr = expression[0]
        position = 0
        action = animat.simpleMultiStateProgram(expr, depth, 0)
        while True:
            if action == "RETURN":
                if expr in trainingSet:
                    correct += 1
                else:
                    print(expr)
                break
            elif action == ">>>":
                if expression[position] != "=":
                    position += 1
                expr += expression[position] 
            else:
                expr += action
            action = animat.simpleMultiStateProgram(expr,depth,0)
    print(correct/len(trainingSet))

print(animat.TransitionTable)
#print(animat.QTable)
#print(animat.ETable)

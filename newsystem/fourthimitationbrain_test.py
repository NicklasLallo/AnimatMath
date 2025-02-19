import random as r
from Brain import *

actionList = ["RETURN", ">>>", "1", "0", "2","3","4","5","6","7","8","9"]


#This is decimal
trainingSet = []
for x in range(10):
    for y in range(10):
        trainingSet.append("{}*{}={}".format(x,y,x*y))


exploreRate = 0.05

depth = 4

animat = Brain(actionList, 0.5, 0.9)

f = open('validationOutput','w')
for x in range(20):
    for y in range(1000):
        expression = str(r.choice(trainingSet))
        position = 0
        expr = expression[0]
        action = animat.multiStateProgram(expr, depth, exploreRate)
        for z in range(100):
            reward = 0
            if action == "RETURN":
                reward = -1
                if expr in trainingSet:
                    reward = 1
                a = animat.multiStateProgram(expr+"D", 0, 0, "RETURN", reward)
                break
            elif action == ">>>":
                reward = 0.01
                if position+1 < len(expression): 
                    position += 1
                else:
                    reward = -0.1
                expr += expression[position]
            else:
                expr += action
                if position+1 < len(expression):
                    position+=1
            action = animat.multiStateProgram(expr,depth,exploreRate,action,reward)
            
    correct = 0
    f.write('\nIteration {}\n'.format(x))
    for expression in trainingSet:
        expr = expression[0]
        position = 0
        action = animat.multiStateProgram(expr, depth, 0, None, None, 0.01, False)
        for y in range(100):
            if action == "RETURN":
                if expr in trainingSet:
                    correct += 1
                else:
                    f.write(expr+'\n')
                    #print(expr)
                break
            elif action == ">>>":
                if expression[position] != "=":
                    position += 1
                expr += expression[position] 
            else:
                if expression[position] != "=":
                    position += 1
                expr += action
            action = animat.multiStateProgram(expr, depth, 0, None, None, 0.01, False)
    print(correct/len(trainingSet))
    print(correct)
    print(len(trainingSet))
    print(animat.topQEntries(10))
    #print(trainingSet)
#print(animat.TransitionTable)
#print(animat.QTable)
#print(animat.ETable)

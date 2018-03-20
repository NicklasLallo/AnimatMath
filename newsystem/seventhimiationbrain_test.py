from Solver2 import *
from Abstracter2 import *

def abstractState(sequence):
    ret = Abstracter.fakeMultiplicationTableAbstracter(sequence)
    return ret

def abstractGoal(sequence):
    state = Abstracter.fakeEqualsAbstracter(sequence)
    ret = {}
    if state != None:
        ret[state] = ("RETURN", 1)
    return ret

actionList = ["RETURN", "1", "0", "2","3","4","5","6","7","8","9"]


#This is decimal
trainingSet = []
print(trainingSet)
for x in range(10):
    for y in range(10):
        trainingSet.append("{}*{}={}".format(x,y,x*y))

print(trainingSet)



for x in range(90):
    trainingSet.append("{}={}".format(x,x))

exploreRate = 1

equalsTrainingProb = 0.11

depth = 4

animat = Solver(actionList, 0.5, 0.9)

f = open('validationOutput','w')
for x in range(20):
    print(len(animat.QTable))
    loading = 100
    for y in range(loading):
        if ((y/loading)*100)%10 == 0:
            print('', end = '#', flush = True)

        expression = str(r.choice(trainingSet))
        expr = expression
        if r.random() < equalsTrainingProb:
            expr = "="
        action = animat.multiStateProgram2(expr, abstractState(expr), depth, exploreRate, None, None, abstractGoal(abstractState(expr)))
        for z in range(10):
            reward = 0
            if action == "RETURN":
                reward = -1
                if expr in trainingSet:
                    reward = 1
                a = animat.multiStateProgram2(expr+"D", abstractState(expr+"D"), 0, exploreRate, "RETURN", reward, abstractGoal(abstractState(expr)))
                if x < 5 or reward != 1:
                    break
                a = Abstracter()
                print(expr)
                print(a.testStructureFormationRule(expr, animat), flush = True)
                break
            else:
                expr += action
            action = animat.multiStateProgram2(expr,abstractState(expr),depth,exploreRate,action,reward,abstractGoal(abstractState(expr)))

            
    correct = 0
    f.write('\nIteration {}\n'.format(x))
    for expression in trainingSet:
        i = expression.find("=")
        expr = expression[0:i+1]
        position = 0
        action = animat.multiStateProgram2(expr,abstractState(expr), depth, 0, None, None, abstractGoal(abstractState(expr)))
        for y in range(20):
            if action == "RETURN":
                if expr in trainingSet:
                    correct += 1
                else:
                    f.write(expr+'\n')
                    #print(expr)
                break
            else:
                expr += action
            action = animat.multiStateProgram2(expr, abstractState(expr), depth, 0, None, None, abstractGoal(abstractState(expr)))
    print(correct/len(trainingSet))
    print(correct)
    print(len(trainingSet))
    print(animat.topQEntries(10))

    #print(trainingSet)
#print(animat.TransitionTable)
#print(animat.QTable)
#print(animat.ETable)

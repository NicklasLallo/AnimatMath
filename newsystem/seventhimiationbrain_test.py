from Solver2 import *
from Abstracter2 import *

def abstractState(sequence):
    return sequence
    #ret = Abstracter.fakeMultiplicationTableAbstracter(sequence)
    #return ret

def abstractGoal(sequence):
    #state = Abstracter.fakeEqualsAbstracter(sequence)
    ret = {}
    #if state != None:
    #    ret[state] = ("RETURN", 1)
    return ret

actionList = ["RETURN", "1", "0", "2","3","4","5","6","7","8","9"]


#This is decimal
trainingSet = []
print(trainingSet)
for x in range(10):
    for y in range(10):
        trainingSet.append("{}*{}={}".format(x,y,x*y))

#print(trainingSet)

for x in range(200):
    trainingSet.append("{}={}".format(x,x))



#actionList = ["RETURN","0","1","2"]

#trainingSet = [
#    "0+0=1",
#    "1+1=2",
#    "0+1=1",
#    "1+0=1",
#    "0+2=2",
#    "2+0=2",
#    "1+2=10",
#    "2+1=10",
#    "2+2=11"
#]
#for x in range(3):
#    trainingSet.append("{}={}".format(x,x))
#    for y in range(3):
#        trainingSet.append("{}{}={}{}".format(x,y,x,y))
#        for z in range(3):
#            trainingSet.append("{}{}{}={}{}{}".format(x,y,z,x,y,z))


exploreRate = 0.9

equalsTrainingProb = 0.05

depth = 3

animat = Solver(actionList, 0.5, 0.9)

f = open('validationOutput','w')
for x in range(20):
    print(len(animat.QTable))
    loading = 1000
    for y in range(loading):
        if ((y/loading)*100)%10 == 0:
            print('', end = '#', flush = True)

        expression = str(r.choice(trainingSet))
        i = expression.find("=")
        if r.random() < equalsTrainingProb:
            expr = expression[0:i+1]
        else:
            expr = expression
        action = animat.multiStateProgram2(expr, abstractState(expr), depth, exploreRate, None, None, abstractGoal(abstractState(expr)))
        for z in range(4):
            reward = 0
            if action == "RETURN" or z == 3:
                reward = -1
                if expr in trainingSet:
                    reward = 1
                a = animat.multiStateProgram2(expr+"D", abstractState(expr+"D"), 0, 1, "RETURN", reward, abstractGoal(abstractState(expr)))
                break
            else:
                expr += action
            action = animat.multiStateProgram2(expr,abstractState(expr),depth,exploreRate,action,reward,abstractGoal(abstractState(expr)))
    if x > 10:
        seqList = []
        for sequence in animat.QTable:
            (bestAction, bestReward) = animat.bestActionAndReward(sequence)
            if bestReward >= 0.99:
                seqList.append(sequence)
        Abstracter.finiteAutomataPatternFinder(seqList)
            
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

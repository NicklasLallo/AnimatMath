from Solver2 import *
from Abstracter2 import *

abstracter = Abstracter()

def abstractSequenceAndGoal(sequence):
    (goalRule, goal, newSequence) = abstracter.structureTreeSearch(sequence, 3)
    if goalRule == None:
        return (sequence, {})
    return (newSequence, {goal: (goalRule[2][0], goalRule[3][0]) })

actionList = ["RETURN", "1", "0", "2","3","4","5","6","7","8","9"]


#This is decimal
trainingSet = []
print(trainingSet)
for x in range(10):
    for y in range(10):
        trainingSet.append("{}*{}={}".format(x,y,x*y))
        for z in range(10):
            trainingSet.append("{}*{}*{}={}".format(x,y,z,x*y*z))

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
    loading = len(trainingSet)
    for y in range(loading):
        if ((y/loading)*100)%10 == 0:
            print('', end = '#', flush = True)

        expression = trainingSet[y]#str(r.choice(trainingSet))
        i = expression.find("=")
        if r.random() < equalsTrainingProb:
            expr = expression[0:i+1]
        else:
            expr = expression

        (absExpr, absGoal) = abstractSequenceAndGoal(expr)

        action = animat.multiStateProgram2(expr, absExpr, depth, exploreRate, None, None, absGoal)
        for z in range(4):
            reward = 0
            if action == "RETURN" or z == 3:
                reward = -1
                newStructure = False
                if expr in trainingSet:
                    reward = 1
                    if x > 4: #and (expr not in animat.QTable or "RETURN" not in animat.QTable[expr]):
                        newStructure = True
                (absExpr, absGoal) = abstractSequenceAndGoal(expr)
                a = animat.multiStateProgram2(expr+"D", absExpr+"D", 0, 1, "RETURN", reward, {})
                if newStructure:
                    print("2")
                    d = abstracter.testStructureFormationRule(expr, animat)
                    print(d)
                    print(expr)
                break
            else:
                expr += action
                (absExpr, absGoal) = abstractSequenceAndGoal(expr)
            action = animat.multiStateProgram2(expr,absExpr,depth,exploreRate,action,reward,absGoal)
            
    correct = 0
    f.write('\nIteration {}\n'.format(x))
    for expression in trainingSet:
        i = expression.find("=")
        expr = expression[0:i+1]
        position = 0
        (absExpr, absGoal) = abstractSequenceAndGoal(expr)
        action = animat.multiStateProgram2(expr,absExpr, depth, 0, None, None, absGoal)
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
            (absExpr, absGoal) = abstractSequenceAndGoal(expr)
            action = animat.multiStateProgram2(expr, absExpr, depth, 0, None, None, absGoal)
    print(correct/len(trainingSet))
    print(correct)
    print(len(trainingSet))
    print(animat.topQEntries(10))
    print(abstracter.structures)

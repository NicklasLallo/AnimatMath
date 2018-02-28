from Controller import *
import random as r


animat = AnimatBrain(5,3,1,  0.8, 1, 0.9384171865197604, 0.489492166955507, 0.6602059448636848, 1,  0.05, 100000, 100)

trueExpressions = [
    "0=0",
    "1=1",
    "10=10",
    "11=11",
    "0+0=0",
    "1+0=1",
    "0+1=1",
    "1+1=10",
    "10+1=11",
    "10+0=10",
    "0+10=10",
    "1+10=11"
]

fakeExpressions = [
    "0=1",
    "1=0",
    "10=1",
    "1=10",
    "0=10",
    "10=0",
    "11=1",
    "0+0=10",
    "1+0=0",
    "1+1=0",
    "1+1=1",
    "0+0=1"
]

nr = 0
correctNr = 0
for x in range(10000000):
    nr += 1
    ture = r.random() > 0.5
    expression = "?"
    if ture:
        expression = trueExpressions[r.randrange(len(trueExpressions))]
    else:
        expression = fakeExpressions[r.randrange(len(fakeExpressions))]

    world = mathTranslator(expression, ture, -1, animat, ["0","1","+","="])

    while True:
        action = world.runAnimat(0)
        if action != 0:
            break
    
    animat.flushNetwork(True)

    if (action == 1 and ture) or (action == 2 and not ture):
        correctNr += 1

    if nr == 100000:
        print(correctNr/nr)
        nr = 0
        correctNr = 0
        print('Anmat has {} nodes'.format(animat.nodeNr))


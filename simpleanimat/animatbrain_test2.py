from AnimatBrain import *
from BrainGraph import *
from BrainTable import *
import random as r


position = 0
reward = [0,0]
attributes = [[1,0,0],[0,1,0],[1,0,0],[0,0,1],[0,1,0]]
eatRewards = [[0.7,-0.05],[-0.05,0.7],[0.7,-0.05],[-0.2,-0.2],[-0.05, -0.8]]
animat = AnimatBrain(3,2,2,  0.750721904233344, 0.5637440246471103, 0.9384171865197604, 0.489492166955507, 0.6602059448636848, 0.8178567097150351,  0.05)


for x in range(0,10000):

    action = animat.program(attributes[position], reward)

    #print(animat.needValues)
    #print(len(animat.network))
    #print(animat.prevTopActive)
    #print(animat.network)

    if action == 0:
        position = (position+1)%5
        reward = [-0.05,-0.05]
    else:
        reward = eatRewards[position]

    if x == 9999:
        print(len(animat.network))
        print(animat.qTable[(0,0,0)])
        exportBrain(animat, 'storeanimattest.sav')
        animat = importBrain('storeanimattest.sav')
        print(len(animat.network))
        print(animat.qTable[(0,0,0)])

#print(animat.historyTopActive)
#print(animat.needValues)
bGraph(animat.network)
bTable(animat.qTable,2, animat.nodeNr,2, ['Hunger', 'Thirst'], ['Walk','Eat/Drink'])
#The swamp AND-node animat from the paper
'''
position = 0

reward = [0,0]
#AnimatBrain(numberOfSensors, numberOfActions, numberOfNeeds, learningRate, discount, structureR, structureZ, structureM, policyParameter, explorationProb):
animat = AnimatBrain(2,3,2,  0.9,0.9,  0.6,0.8,0.1,  0.4,  0.2)

for x in range(0,100):

    attributes = [[0,1],[1,1],[1,0]]

    action = animat.program(attributes[position],reward)

    print(animat.needValues)
    #print(animat.qTable)
    print(animat.network)
    if x == 99:
       bGraph(animat.network)

    if action == 0:
        position = min(position+1,2)
        reward = [-0.05,-0.05]
    elif action == 1:
        position = max(position-1,0)
        reward = [-0.05,-0.05]
    else:
        if position == 0:
            reward = [0.7, -0.05]
        elif position == 1:
            reward = [-0.3,-0.3]
        else:
            reward = [-0.05, 0.7]
'''



#First two-room test
'''
#for x in range(0,10):
#
#    if position == 0:
#        attributes = [1,0]
#    else:
#        attributes = [0,1]
#
#    action = animat.program(attributes, reward)
#    print('Action: {}, Position: {}'.format(action, position))
#    if action != position:
#        position = action
#        reward[0] = 0.5
#        print('good!')
#    else:
#        reward[0] = -0.5
#        print('bad')
'''

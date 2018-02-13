from AnimatBrain import *
from BrainGraph import *


position = 0
reward = [0,0]
attributes = [np.array([1,0,0]), np.array([0,1,0]), np.array([1,0,0]), np.array([0,0,1]), np.array([0,1,0])]
eatRewards = [[0.7,-0.05],[-0.05,0.7],[0.7,-0.05],[-0.2,-0.2],[-0.05, -0.8]]
animat = AnimatBrain(3,2,2,  0.9,0.9,  0.9,0.8,0.1,  0.4,  0.05)

for x in range(0,100000):

    action = animat.program(attributes[position], reward)

    print(animat.needValues)
    print(len(animat.network))
    #print(animat.network)

    if action == 0:
        position = (position+1)%5
        reward = [-0.05,-0.05]
    else:
        reward = eatRewards[position]

bGraph(animat.network)
#The swamp AND-node animat from the paper
'''
position = 0

reward = [0,0]
#AnimatBrain(numberOfSensors, numberOfActions, numberOfNeeds, learningRate, discount, structureR, structureZ, structureM, policyParameter, explorationProb):
animat = AnimatBrain(2,3,2,  0.9,0.9,  0.6,0.8,0.1,  0.4,  0.2)

for x in range(0,100):

    attributes = [np.array([0,1]),np.array([1,1]),np.array([1,0])]

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
#        attributes = np.array([1,0])
#    else:
#        attributes = np.array([0,1])
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

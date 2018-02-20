from World import World
from AnimatBrain import AnimatBrain
from MoveHandeler import MoveHandeler
from BrainTable import *

#def __init__(self, blockTypesAndAttributesAndRewards, structure, animats, animatPos, animatTypes, animatsVisible=False, sideeffectHandeler = None):
#animat = AnimatBrain(3,2,2,  0.750721904233344, 0.5637440246471103, 0.9384171865197604, 0.489492166955507, 0.6602059448636848, 0.8178567097150351,  0.05)

sheep = AnimatBrain(6,5,1, 0.75, 0.56, 0.93, 0.49, 0,66, 0.82, 0.05)
wolf = AnimatBrain(6,5,1, 0.75, 0.56, 0.93, 0.49, 0,66, 0.82, 0.05)
blocks = {
        'left': ([1,0,0,0],[
            [[-0.05],[-0.05],[-0.05],[-0.05],[-0.2]],
            [[-0.05],[-0.05],[-0.05],[-0.05],[-0.2]]
        ]),    
        'up': ([0,1,0,0],[
            [[-0.05],[-0.05],[-0.05],[-0.05],[-0.2]],
            [[-0.05],[-0.05],[-0.05],[-0.05],[-0.2]]
        ]),
        'right': ([0,0,1,0],[
            [[-0.05],[-0.05],[-0.05],[-0.05],[-0.2]],
            [[-0.05],[-0.05],[-0.05],[-0.05],[-0.2]]
        ]),
        'rock': ([0,0,0,0],[
            [[100],[100],[100],[100],[100000]],
            [[100],[100],[100],[100],[100000]]
        ]),
        'gras': ([0,0,0,1],[
            [[-0.05],[-0.05],[-0.05],[-0.05],[0.7]],
            [[-0.05],[-0.05],[-0.05],[-0.05],[-0.1]]
        ])
        }

structure = [['right', 'right', 'gras'],
             ['up',    'rock',  'rock'],
             ['up',    'left',  'left']]

animats = [sheep, wolf]
animatPos = [(0,2),(2,2)]
animatTypes = [0,1]
nrOfAnimatNeeds = [2,2]
animatsVisible = True
sideeffectHandeler = MoveHandeler([0,1,2,3], ['rock'])


world = World(blocks, structure, animats, animatPos, animatTypes, nrOfAnimatNeeds, True, sideeffectHandeler)

for x in range(1000):
    world.worldStep()
    (animat, pos, animatType) = world.animats[0]
    needValues = animat.needValues
    print('Animat at pos {} has hunger {}'.format(pos, needValues[0]))

bTable(sheep.qTable,1,sheep.nodeNr,5,['hunger'],['right','up','left','down','eat'])

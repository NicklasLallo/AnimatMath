from World import World
from AnimatBrain import AnimatBrain
from MoveHandeler import MoveHandeler

#def __init__(self, blockTypesAndAttributesAndRewards, structure, animats, animatPos, animatTypes, animatsVisible=False, sideeffectHandeler = None):
#animat = AnimatBrain(3,2,2,  0.750721904233344, 0.5637440246471103, 0.9384171865197604, 0.489492166955507, 0.6602059448636848, 0.8178567097150351,  0.05)

sheep = AnimatBrain(3,2,2, 0.75, 0.56, 0.93, 0.49, 0,66, 0.82, 0.05)
wolf = AnimatBrain(3,2,2, 0.75, 0.56, 0.93, 0.49, 0,66, 0.82, 0.05)
blocks = {
        'snow': ([0,1],[
            [[-0.05],[-0.05],[-0.05],[-0.05],[-0.2]],
            [[-0.05],[-0.05],[-0.05],[-0.05],[-0.2]]
        ]),
        'rock': ([0,0],[
            [[-0.05],[-0.05],[-0.05],[0],[0]],
            [[-0.05],[-0.05],[-0.05],[0],[0]]
        ]),
        'gras': ([0,1],[
            [[-0.05],[-0.05],[-0.05],[-0.05],[0.7]],
            [[-0.05],[-0.05],[-0.05],[-0.05],[-0.1]]
        ])
        }

structure = [['snow', 'snow', 'gras'],
             ['snow', 'rock', 'rock'],
             ['snow', 'snow', 'gras']]

animats = [sheep, wolf]
animatPos = [(2,2),(2,2)]
animatTypes = [0,1]
animatsVisible = True
sideeffectHandeler = MoveHandeler([0,1,2,3], ['rock'])

world = World(blocks, structure, animats, animatPos, animatTypes, animatsVisible = True, sideeffectHandeler)

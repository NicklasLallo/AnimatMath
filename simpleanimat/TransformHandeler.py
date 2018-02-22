from SideeffectHandeler import *
from World import *
from AnimatBrain import *

class TransformHandeler(SideeffectHandeler):
    
    def __init__(self, transformations):
        self.transformations = transformations

    def handleAction(self, animat, action, world):
        (animatBrain, (x,y), animatType) = world.animats[animat]
        block = world.getBlock(x,y)
        if action in self.transformations:
            values = self.transformations[action]
            if block in values:
                newblock = values[block]
                world.structure[y][x] = newblock


from SideeffectHandeler import *
from World import World
import math

class MoveHandeler(SideeffectHandeler):
    
    def __init__(self, mapping, impassableBlocks):
        self.right = mapping[0]
        self.up = mapping[1]
        self.left = mapping[2]
        self.down = mapping[3]
        self.impassableBlocks = impassableBlocks

    def handleAction(self, animat, action, world):
        (animatBrain, (x,y), animatType) = world.animats[animat]
        ysize = len(world.structure)
        xsize = len(world.structure[0])
        xmove = 0
        ymove = 0
        if action == self.right:
            xmove += 1
        elif: action == self.up:
            ymove -= 1
        elif: action == self.left:
            xmove -=1
        elif: acion == self.down:
            ymove += 1
        if xmove == 0 and ymove == 0:
            return
        x += xmove
        y += ymove
        if x >= xsize or y >= ysize or x < 0 or y < 0
            return
        if world.structure[y][x] in self.impassableBlocks:
            return
        world.animats[animat] = (animatBrain, (x,y), animatType)


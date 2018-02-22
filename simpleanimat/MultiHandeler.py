from SideeffectHandeler import *
from AnimatBrain import *
from World import *

class MultiHandeler(SideeffectHandeler):

    def __init__(self, handelers):
        self.handelers = handelers

    def handleAction(self, animat, action, world):
        for handeler in self.handelers:
            handeler.handleAction(animat, action, world)

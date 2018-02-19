import numpy as np

class World:

    #blockTypesAndAttributesAndRewards is a dictionary with the blockType as key and the value as a tuple of its attributes and rewards
        #attributes is list of 1s and 0s
        #rewards is a 2d list of the rewards for this blockType depending on action and animatType
    #structure is a 2d list of blockTypes
    #animats is a list of AnimatBrain
    #animatPos is a list with the same length as animats containing tuples (x,y) which is the starting positions for all animats
    #animatTypes is a list with the same length as animats that denotes what animatType (int) for all animats
    def __init__(self, blockTypesAndAttributesAndRewards, structure, animats, animatPos, animatTypes, animatsVisible=False, sideeffectHandeler = None):
        self.blocks = blockTypesAndAttributesAndRewards
        self.structure = structure
        self.animats = []
        self.animatNr = len(animats)
        self.animatTypeNr = 0
        self.animatsVisible = animatsVisible
        self.sideeffectHandeler = sideeffectHandeler
        self.nextRewards = [0]*animatNr
        for x in range(self.animatNr):
            self.animats.append((animats[x], animatPos[x], animatType[x]))
            if animatType[x]+1 > self.animatTypeNr:
                self.animatTypeNr = animatType[x]+1

    def getAnimatAttributes(self, nr):
        (animatBrain, (x,y), animatType) = self.animats[nr]
        (attributes, rewards) = self.blocks[self.structure[y][x]]
        if self.animatsVisible:
            animatAttributes = [0]*self.animatTypeNr
            for (ani,pos,aniType) in self.animats:
                if ani == animatBrain:
                    continue
                if pos == (x,y):
                    animatAttributes[aniType] = 1
            attributes += animatAttributes
        return (attributes, rewards)

    def runAnimat(self, nr):
        (attributes, rewards) = getAnimatAttributes(nr)
        (animatBrain, pos, animatType) = self.animats[nr]
        action = animatBrain.program(attributes, self.nextRewards[nr])
        self.nextRewards[nr] = rewards[action][animatType]
        if sideeffectHandeler != None:
            sideeffectHandeler.handleAction(nr, action, self)

    def worldStep(self):
        for nr in range(animatNr):
            runAnimat(nr)
        



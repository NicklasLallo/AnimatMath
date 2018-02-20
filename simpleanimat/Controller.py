from World import *
from AnimatBrain import *
import pickle
import json
from BrainTable import *
from BrainGraph import *



def oldconfigToWorld(filename):
    jason = open(filename, 'r', encoding = 'utf-8')
    config = json.load(jason)
    
    #Meta Data
    iterations = config['iterations']
    splitter = '\n'
    if 'splitter' in config:
        splitter = config['splitter']
    secondsplitter = None
    if 'secondsplitter' in config:
        secondsplitter = config['secondsplitter']
    seed = None
    if 'seed' in config:
        seed = config['seed']


    #World
    structure = config['world'].split(splitter)
    if secondsplitter == None:
        structure = map(structure, list)
    else:
        structure = map(structure, split(secondsplitter))

    temp_blocks = config['blocks']
    blocks = {}
    nrOfAttributes = 0
    for blockType, attrs in temp_blocks.items():
        for attr, val in attrs:
            if attr > nrOfAttributes:
                nrOfAttributes = attr
    for blockType, attrs in temp_blocks.items():
        attributes = [0]*nrOfAttributes
        blocks[blockType] = (attributes,[[]])
        for attr, val in attrs:
            attributes[int(attr)] = val

    needNames = config['objectives']
    nrOfNeeds = len(needNames)

    rewards = config['rewards']
    actionNames = []
    nrOfActions = len(rewards)
    temp_action = 0
    for action, actionreward in rewards:
        actionNames.append(action)
        genericreward = [0]*nrOfNeeds
        if '*' in actionreward:
            genericreward = [reward['*']]*nrOfNeeds
        for block, (attributes, [rewards]) in blocks
            blockactionreward = genericreward
            if block in actionreward:
                temp_blockactionreward = actionreward[block]
                if type(temp_blockactionreward) is int or type(temp_blockactionreward) is float:
                    blockactionreward = [temp_blockactionreward]*nrOfNeeds
                else:
                    if '*' in temp_blockactionreward:
                        blockactionreward = [temp_blockactionreward['*']]*nrOfNeeds
                    for need in temp_blockactionreward:
                        if need == '*':
                            continue
                        blockactionreward[needNames.index(need)]
            rewards.append(blockactionreward)


    #Animats


fileToWorld('example-4-seq.json')


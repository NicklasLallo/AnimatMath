from World import *
from AnimatBrain import *
import pickle
import json
from BrainTable import *
from BrainGraph import *
from MoveHandeler import *


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
        structure = list(map(lambda x: list(x), structure))
    else:
        structure = list(map(lambda x: x.split(secondsplitter), structure))

    temp_blocks = config['blocks']
    blocks = {}
    uniqueAttributes = []
    for blockType, attrs in temp_blocks.items():
        for attr, val in attrs.items():
            if attr not in uniqueAttributes:
                uniqueAttributes.append(attr)
    nrOfAttributes = len(uniqueAttributes)
    for blockType, attrs in temp_blocks.items():
        attributes = [0]*nrOfAttributes
        blocks[blockType] = (attributes,[[]])
        for attr, val in attrs.items():
            attributes[uniqueAttributes.index(attr)] = val

    needNames = config['objectives']
    nrOfNeeds = len(needNames)

    rewards = config['rewards']
    actionNames = []
    nrOfActions = len(rewards)
    temp_action = 0
    for action, actionreward in rewards.items():
        actionNames.append(action)
        genericreward = [0]*nrOfNeeds
        if '*' in actionreward:
            genericreward = [actionreward['*']]*nrOfNeeds
        for block, (attributes, [rews]) in blocks.items():
            blockactionreward = list(genericreward)
            if block in actionreward:
                temp_blockactionreward = actionreward[block]
                if type(temp_blockactionreward) is int or type(temp_blockactionreward) is float:
                    blockactionreward = [temp_blockactionreward]*nrOfNeeds
                else:
                    if '*' in temp_blockactionreward:
                        blockactionreward = [temp_blockactionreward['*']]*nrOfNeeds
                    for need, val in temp_blockactionreward.items():
                        if need == '*':
                            continue
                        blockactionreward[needNames.index(need)] = val 
            rews.append(blockactionreward)

    sideeffectHandeler = None
    if 'sideeffectHandeler' in config:
        temp_sid = config['sideeffectHandeler']
        if temp_sid[0] == 'MoveHandeler':
            sideeffectHandeler = MoveHandeler(temp_sid[1], temp_sid[2])

    #Animats
    agent = config['agent']
    constants = agent['network']
    explorationProb = constants['epsilon']
    historyMaxLength = constants['max_reward_history']
    learningRate = constants['q_learning_factor']
    discount = constants['q_discount_factor']
    reward_learning_factor = constants['reward_learning_factor']
    structureZ = 2
    if 'surprise_const' in agent:
        structureZ = agent['surprise_const']
    structureR = 0.5
    if 'reliablility_const' in agent:
        structureR = agent['reliability_const']
    structureM = 0
    if 'newnode_const' in agent:
        structureM = agent['newnode_const']
    policyParameter = 0.7
    if 'policyParameter' in agent:
        policyParameter = agent['policyParameter']
    
    position = (0,0)
    if 'position' in agent:
        position = agent['position']


    #Putting it all together
    animat = AnimatBrain(nrOfAttributes, nrOfActions, nrOfNeeds, learningRate, discount, structureR, structureZ, structureM, policyParameter, explorationProb, historyMaxLength)
    world = World(blocks, structure, [animat], [position], [0], [nrOfNeeds], sideeffectHandeler)

    return world



import numpy as np
import random as r 
import math

class AnimatBrain:

    def __init__(self, numberOfSensors, numberOfActions, numberOfNeeds, learningRate, discount, structureLearningParameters, policyParameter, explorationProb):
        #TODO: Init network etc
        self.nrOfSensors = numberOfSensors
        self.nrOfActions = numberOfActions
        self.nrOfNeeds = numberOfNeeds
        self.needValues = [1] * numberOfNeeds
        self.learningRate = learningRate
        self.discount = discount
        self.policyParameter = policyParameter
        self.explorationProb = explorationProb

        self.prevTopActive=[]
        self.actionPerformed=0
        self.historyTopActive = []
        self.historyMaxLength = 10

        self.initTables(numberOfSensors, numberOfActions, numberOfNeeds)

        self.initNetwork(numberOfSensors, structureLearningParameters)

    def initTables(self, numberOfSensors, numberOfActions, numberOfNeeds):
        self.qTable = {}
        self.rTable = {}
        self.sumRewardTable = {}
        self.sumSqRewardTable = {}
        self.nrTable = {}
        for need in range(0,numberOfNeeds):
            for node in range(0,numberOfSensors):
                for action in range(0, numberOfActions):
                    self.qTable[(need,node,action)] = 0
                    self.rTable[(need,node,action)] = 1
                    self.nrTable[(need,node,action)] = 0
                    self.sumRewardTable[(need,node,action)] = 0
                    self.sumSqRewardTable[(need,node,action)] = 0

    def initNetwork(self, numberOfSensors, structureLearningParameters):
        #Initializes the network as a dict with key as node number and values as a list of info of this node.
        #The first value is the id of the node (0 for sensor, 1 for AND, 2 for SEQ)
        #The second value is if the node is active or inactive (1=active, 0=inactive)
        #For AND-/SEQ the thrid and fourth values are the nodes they are connected to
        #For SEQ the fifth value is whether the node was powered previous step or not
        self.network = {}
        self.nodeNr = 0
        for sensor in range(0, numberOfSensors):
            self.network[self.nodeNr] = [0,0]
            self.nodeNr += 1


    #####
    
    def program(self, attributes, rewards, forceExploitation = False):
        #Takes the active sensors (and a boolean flag for forcing exploitation), propogates the network, searches the Q-table and returns the action to perform 
        
        #TODO: Update Network

        topActive = self.propogateNetwork(attributes)
        print(topActive)
        
        self.updateTables(self.actionPerformed, topActive, self.prevTopActive, self.learningRate, self.discount, rewards)

        #Definition 12. Finding the action to take according top policy pi
        bestActionValue = -2
        bestAction = 0
        for action in range(0,self.nrOfActions):
            worstNeedValue = 2
            for need in range(0,self.nrOfNeeds):
                needValue = self.needValues[need] + self.policyParameter * self.getGlobalQValue(topActive, need, action)
                if needValue < worstNeedValue:
                    worstNeedValue = needValue
            if worstNeedValue > bestActionValue:
                bestActionValue = worstNeedValue
                bestAction = action

        if r.random() < self.explorationProb and not forceExploitation:
            bestAction = r.randint(0,self.nrOfActions-1)

        self.prevTopActive = topActive
        self.historyTopActive.append(topActive)
        if len(self.historyTopActive) > self.historyMaxLength:
            del self.historyTopActive[0]
        self.actionPerformed = bestAction
    
        #for i in self.qTable:
        #    print(i, self.qTable[i])
        return bestAction

    def propogateNetwork(self, attributes):
        #TODO: Replace placeholderfunction
        #Takes the array of active sensors and returns a list of topactive nodes
        #return [i for i, x in enumerate(attributes.tolist()) if x == 1]
        attrs = attributes.tolist()
        sensor = 0
        topActive = []
        for value in attrs:
            self.network[sensor][1] = value
            if value == 1:
                topActive.append(sensor)
            sensor += 1
    
        for node in range(self.nrOfSensors, self.nodeNr):
            values = self.network[node]
            if values[0] == 1: #if this is an AND-node
                if self.network[values[2]][1] == 1 and self.network[values[3]][1] == 1:
                    self.network[node][1] == 1
                    topActive.remove(values[2])
                    topActive.remove(values[3])
                    topActive.append(node)
            elif values[0] == 2: #if this is a SEQ-node
                if values[4] and self.network[values[3]][1] == 1:
                    self.network[node][1] == 1
                    topActive.remove(values[2])
                    topActive.remove(values[3])
                    topActive.append(node)
                self.network[node][4] = self.network[values[2]][1]
            else:
                raise ValueError('No such non-sensor node: {}'.format(values[0]))

        return topActive

    def getGlobalQValue(self, topActive, need, action):
        #Takes the topactive nodes, one action, and one need and finds the global Q-value for that need and action
        value = 0
        rsum = 0
        
        
        

        for node in topActive:
            value += self.qTable[(need,node,action)]*self.rTable[(need,node,action)]
            rsum += self.rTable[(need,node,action)]
     #       print(value,rsum)

        if rsum == 0: return(value) #TODO
        
        return (value/rsum)
            
    

    #####

    def updateTables(self, actionPerformed, topActive, prevTopActive, learningRate, discount, rewards):
        #Definition 11 in Claes animat paper
        for need in range(0, self.nrOfNeeds): #doesn't include last index
            reward = rewards[need]
            #print("{} {}".format("uTr:", reward))
            globalQValues = []
            for action in range(0,self.nrOfActions):
                globalQValues.append(self.getGlobalQValue(topActive, need, action))
            globalQ = max(globalQValues)
            for node in prevTopActive:
                key = (need,node,actionPerformed)
                self.qTable[key] = self.qTable[key] + learningRate*(reward + discount*(globalQ-self.qTable[key]))
                self.nrTable[key] = self.nrTable[key]+1
                self.sumRewardTable[key] = self.sumRewardTable[key] + reward
                self.sumSqRewardTable[key] = self.sumSqRewardTable[key] + reward**2
            #    print(self.rTable[key],self.sumSqRewardTable[key],self.sumRewardTable[key])
                self.rTable[key] = 1/(1 + math.sqrt(self.nrTable[key]*self.sumSqRewardTable[key] - self.sumRewardTable[key]**2)/self.nrTable[key])

    def updateNetwork(self, topActive, prevTopActive, need):
        #Definition 15. Run for each need for which the animat recieved a surprise
        pass

    def addNode(self, nodeType, connection1, connection2):
        node = self.nodeNr
        self.nodeNr += 1
        self.network[node] = [nodeType, 0, connection1, connection2]
        if nodeType == 2: #if we're adding a SEQ node it needs to be able to store info from the previous step
            self.network[node].append(self.network[connection1][1])
        for need in range(0,self.nrOfNeeds):
            for action in range(0,self.nrOfActions):
                    self.qTable[(need,node,action)] = 0
                    self.rTable[(need,node,action)] = 1
                    self.nrTable[(need,node,action)] = 0
                    self.sumRewardTable[(need,node,action)] = 0
                    self.sumSqRewardTable[(need,node,action)] = 0
            


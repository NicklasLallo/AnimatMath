import numpy as np
import random as r 

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

        self.initTables(numberOfSensors, numberOfActions, numberOfNeeds)

        #Should initialize the network
        pass

    def initTables(self, numberOfSensors, numberOfActions, numberOfNeeds):
        self.qTable = {}
        self.rTable = {}
        for need in range(0,numberOfNeeds-1):
            for node in range(0,numberOfSensors-1):
                for action in range(0, numberOfActions-1):
                    self.qTable[(need,node,action)] = 0
                    self.rTable[(need,node,action)] = 1
                    self.nrTable[(need,node,action)] = 0
                    self.sumRewardTable[(need,node,action)] = 0
                    self.sumSqRewardTable[(need,node,action)] = 0

    def initNetwork(self, numberOfSensors, structureLearningParameters):
        pass


    #####
    
    def program(self, attributes, rewards, forceExploitation = False):
        #Takes the active sensors (and a boolean flag for forcing exploitation), propogates the network, searches the Q-table and returns the action to perform 
        
        #TODO: Update Network

        topActive = self.propogateNetwork(attributes)
        
        self.updateTables(self.actionPerformed, topActive, self.prevTopActive, self.learningRate, self.discount, rewards)

        #Definition 12. Finding the action to take according top policy pi
        bestActionValue = -2
        bestAction = 0
        for action in range(0,self.nrOfActions-1):
            worstNeedValue = 2
            for need in range(0,self.nrOfNeeds-1):
                needValue = self.needValues[need] + self.policyParameter * self.getGlobalQValue(topActive, need, action)
                if needValue < WorstNeedValue:
                    worstNeedValue = needValue
            if worstNeedValue > bestActionValue:
                bestActionValue = worstNeedValue
                bestAction = action

        if r.random() < self.explorationProb and not forceExploitation:
            bestAction = r.randint(0,self.nrOfActions-1)

        self.prevTopActive = topActive
        self.actionPerformed = bestAction

        return bestAction

    def propogateNetwork(self, attributes):
        #TODO: Replace placeholderfunction
        #Takes the array of active sensors and returns a list of topactive nodes
        return attributes.tolist()


    def getGlobalQValue(self, topActive, need, action):
        #Takes the topactive nodes, one action, and one need and finds the global Q-value for that need and action
        for node in topActive:
            value += self.qTable[(need,node,action)]*self.rTable[(need,node,action)]
            rsum += self.rTable[(need,node,action)]
        return (value/rsum)
            
    

    #####

    def updateTables(self, actionPerfomed, topActive, prevTopActive, learningRate, discount, rewards):
        #Definition 11 in Claes animat paper
        for need in range(0, self.nrOfNeeds-1):
            reward = rewards[need]
            globalQValues = []
            for action in range(0,self.nrOfActions-1):
                globalQValues.append(self.getGlobalQValue(topActive, need, action))
            globalQ = max(globalQValues)
            for node in prevTopActive:
                key = (need,node,actionPerformed)
                self.qTable[key] = self.qTable[key] + learningRate*(reward + discount*(globalQ-self.qTable[key]))
                self.nrTable[key] = self.nrTable[key]+1
                self.sumRewardTable[key] = self.sumRewardTable[key] + reward
                self.sumSqRewardTable[key] = self.sumSqRewardTable[key] + reward**2
                self.rTable[key] = 1/(1 + math.sqrt(self.nrTable[key]*self.sumSqRewardTable[key] - sumRewardTable[key]**2)/self.nrTable[key])

    def updateNetwork(self, topActive, prevTopActive, need):
        #Definition 15. Run for each need for which the animat recieved a surprise
        pass



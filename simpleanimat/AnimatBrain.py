import numpy as np
import random as r 
import math

class AnimatBrain:

    def __init__(self, numberOfSensors, numberOfActions, numberOfNeeds, learningRate, discount, structureR, structureZ, structureM, policyParameter, explorationProb):
        #TODO: Init network etc
        self.nrOfSensors = numberOfSensors
        self.nrOfActions = numberOfActions
        self.nrOfNeeds = numberOfNeeds
        self.needValues = [1] * numberOfNeeds
        self.learningRate = learningRate        #How much does expreience from previous step influence the animats understanding of the world
        self.discount = discount                #How highly does the animat learning value future reward
        self.policyParameter = policyParameter  #How highly does the decision-making value future reward
        self.explorationProb = explorationProb  #How often will the animat make a random acion due to exploration
        self.structureR = structureR            #How high does the reliability of a Q-entry have to be for the animat to be surprised by it
        self.structureZ = structureZ            #How much must a Q-entry cahnge for the animat to be surprised by it
        self.structureM = structureM            #How much can the Q-entry of a node-candidate fluctuate and that node is still added

        self.newestNodes = [-1,-1,-1]
        self.surprisedNeeds = []
        self.prevTopActive=[]
        self.actionPerformed=0
        self.historyTopActive = []
        self.historyActionPerformed = []
        self.historyRewards = []
        self.historyGlobalQs = []
        self.historyMaxLength = 100

        self.initTables(numberOfSensors, numberOfActions, numberOfNeeds)

        self.initNetwork(numberOfSensors)

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

    def initNetwork(self, numberOfSensors):
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

        self.historyRewards.append(rewards)
        if len(self.historyRewards) > self.historyMaxLength:
            del self.historyRewards[0]

        self.needValues = [x+y for x,y in zip(self.needValues,rewards)]

        self.surprisedNeeds = []

        topActive = self.propogateNetwork(attributes)
        #print(topActive) 
        
        self.updateTables(self.actionPerformed, topActive, self.prevTopActive, self.learningRate, self.discount, rewards)
        
        self.updateNetwork()

        #Definition 12. Finding the action to take according to policy pi
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
        self.actionPerformed = bestAction
        self.historyTopActive.append(topActive)
        self.historyActionPerformed.append(bestAction)
        if len(self.historyTopActive) > self.historyMaxLength:
            del self.historyTopActive[0]
            del self.historyActionPerformed[0]
            del self.historyGlobalQs[0]
    
        #for i in self.qTable:
        #    print(i, self.qTable[i])

        #print(self.network)

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
                    self.network[node][1] = 1
                    if values[2] in topActive:
                        topActive.remove(values[2])
                    if values[3] in topActive:
                        topActive.remove(values[3])
                    topActive.append(node)
                else:
                    self.network[node][1] = 0
            elif values[0] == 2: #if this is a SEQ-node
                if values[4] and self.network[values[3]][1] == 1:
                    self.network[node][1] = 1
                    if values[2] in topActive:
                        topActive.remove(values[2])
                    if values[3] in topActive:
                        topActive.remove(values[3])
                    topActive.append(node)
                else:
                    self.network[node][1] = 0
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
        globalQs = [] #recording history
        self.historyGlobalQs.append(globalQs) #recordning history
        for need in range(0, self.nrOfNeeds): #doesn't include last index
            reward = rewards[need]
            #print("{} {}".format("uTr:", reward))
            globalQValues = []
            for action in range(0,self.nrOfActions):
                globalQValues.append(self.getGlobalQValue(topActive, need, action))
            globalQ = max(globalQValues)
            globalQs.append(globalQ) #recording history
            for node in prevTopActive:
                key = (need,node,actionPerformed)
                newQ = self.qTable[key] + learningRate*(reward + discount*(globalQ-self.qTable[key]))
                if self.isSurprised(self.qTable[key], newQ, self.rTable[key]):
                    self.surprisedNeeds.append(need)
                self.qTable[key] = newQ
                self.nrTable[key] = self.nrTable[key]+1
                self.sumRewardTable[key] = self.sumRewardTable[key] + reward
                self.sumSqRewardTable[key] = self.sumSqRewardTable[key] + reward**2
            #    print(self.rTable[key],self.sumSqRewardTable[key],self.sumRewardTable[key])
            #    print(math.sqrt(self.sumSqRewardTable[key]/self.nrTable[key] - (self.sumRewardTable[key]/self.nrTable[key])**2))
                self.rTable[key] = 1/(1 + math.sqrt(abs(self.sumSqRewardTable[key]/self.nrTable[key] - (self.sumRewardTable[key]/self.nrTable[key])**2)))

    def updateNetwork(self):
        #Definition 15
        if len(self.surprisedNeeds) == 0:
            return
        need = self.surprisedNeeds[r.randint(0,len(self.surprisedNeeds)-1)]
        action  = self.actionPerformed
        
        #Try to add an AND-node
        nodeCandidates = []
        for node1 in self.prevTopActive:
            for node2 in self.prevTopActive:
                if node1 == node2:
                    break
                if (1,node1,node2) in self.newestNodes:
                    continue
                if self.simulateNode(1, node1, node2, need, action, len(self.historyTopActive)):
                    nodeCandidates.append((node1,node2))
        if len(nodeCandidates) > 0:
            (connection1, connection2) = nodeCandidates[r.randint(0, len(nodeCandidates)-1)]
            self.addNode(1, connection1, connection2)
            self.newestNodes.append((1,connection1,connection2))
            del self.newestNodes[0]
            return

        #Try to add a SEQ-node
        if len(self.historyTopActive) < 2:
            return
        nodeCandidates = []
        for node1 in self.prevTopActive:
            for node2 in self.historyTopActive[-2]:
                if node1 == node2:
                    continue
                if (2,node1,node2) in self.newestNodes:
                    print("Should not happen")
                    continue
                print((2,node1,node2))
                if self.simulateNode(2, node1, node2, need, action, len(self.historyTopActive)):
                    nodeCandidates.append((node1,node2))
        if len(nodeCandidates) > 0:
            (connection1, connection2) = nodeCandidates[r.randint(0, len(nodeCandidates)-1)]
            self.addNode(2, connection1, connection2)
            self.newestNodes.append((2,connection1,connection2))
            del self.newestNodes[0]
            return

    def addNode(self, nodeType, connection1, connection2, qValue = 0, rValue = 1):
        node = self.nodeNr
        self.nodeNr += 1
        self.network[node] = [nodeType, 0, connection1, connection2]
        if nodeType == 2: #if we're adding a SEQ node it needs to be able to store info from the previous step
            self.network[node].append(self.network[connection1][1])
        for need in range(0,self.nrOfNeeds):
            for action in range(0,self.nrOfActions):
                    self.qTable[(need,node,action)] = qValue
                    self.rTable[(need,node,action)] = rValue
                    self.nrTable[(need,node,action)] = 0
                    self.sumRewardTable[(need,node,action)] = 0
                    self.sumSqRewardTable[(need,node,action)] = 0
            
    def isSurprised(self, prevQValue, nowQValue, prevRValue):
        return abs(nowQValue - prevQValue) > self.structureZ and prevRValue > self.structureR

    def simulateNode(self, nodeType, connection1, connection2, need, actionPerformed, historyLength):
        if historyLength < 2:
            return False
        #Hardcoded to work with the current nodes types (AND/SEQ) needs to be rewritten if more types of nodes are added
        nodeQ = 0 #Might be better to give the node Q and R from avg of its connection
        nodeR = 1
        nodeNr = 0
        nodeSumReward = 0
        nodeSumSqReward = 0
        nodeChange = 9999999

        for step in range(1,historyLength):
            if self.historyActionPerformed[step] != actionPerformed:
                continue
            if connection2 not in self.historyTopActive[step]:
                continue
            if (nodeType == 1 and connection1 not in self.historyTopActive[step]) or (nodeType == 2 and connection1 not in self.historyTopActive[step-1]):
                continue
                print('YAY!')
                nodeChange = nodeQ
                nodeQ = nodeQ + learningRate*(self.rewardHistory[step][need] + discount*(self.historyGlobalQ[step][need]-nodeQ))
                nodeChange = abs(nodeQ-nodeChange)
                #Can be added to initiate the nodes values but currently not used
                #nodeNr += 1   
                #nodeSumReward += self.historyReward[step][need]
                #nodeSumSqReward += self.historyReward[step][need]**2
                #nodeR = 1/(1 + math.sqrt(nodeNr*nodeSumSqReward - nodeSumReward**2)/nodeNr)

        return nodeChange < self.structureM

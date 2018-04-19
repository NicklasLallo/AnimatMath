import random as r
from Tree import *

class Solver():
    
    #Constructors

    def __init__(self, actionList, learningRate, discountFactor):
        self.actionList = actionList
        self.learningRate = learningRate
        self.discountFactor = discountFactor
        
        #Contains information of what states+actions lead to what states
        self.TransitionTable = {}

        #Contains Q-values for state-action pairs
        self.QTable = {}

        #Contains average reward for state-action pairs
        self.ETable = {}

        #A tree structure of rewarded sequences. Each sequence is stored in reverse to quickly find equivalent sequences
        self.rewardedSequences = Tree()

        #Same as above but not stored in reverse
        self.rewardedSequencesForward = Tree()
        self.rewardedSequencesForward.node = None

        #A set with all punished sequences
        self.inputSet = set()

    #Runnable

    def improvedProgram(self, stateSequence, depth = 4, abstractSequence = None, exploreProb = 0, prevAction = None, reward = None, potentialGoals = {}, minGoal = 0.9, debug = False, training = True):
        if abstractSequence == None:
            abstractSequence = stateSequence
        
        if prevAction != None and training:
            self.updateTransitionTable(stateSequence[-2], prevAction, stateSequence[-1])
            if reward != None:
                self.oneStateLearning(stateSequence[:-1], prevAction, stateSequence, reward) 
                if reward >= minGoal:
                    self.addRewardedSequence(stateSequence[:-1], reward, prevAction)

        if reward != None and training:
            totalReliability = 1
            fromString = stateSequence
            for end in range(1, len(stateSequence)):
                toString = fromString
                fromString = stateSequence[0:len(stateSequence)-end]
                (reliability, action) = self.reliabilityToGoal(fromString, toString, True)
                if reliability == 0:
                    break
                totalReliability *= reliability*self.discountFactor
                action = action[0]
                if debug:
                    print("{} goes from {} to {} with prob {}".format(action, fromString, toString, reliability))
                thisReward = 0
                if fromString in self.ETable and action in self.ETable[fromString]:
                    thisReward = self.ETable[fromString][action]

                self.oneStateLearning(fromString, action, toString, thisReward, totalReliability)

        if training and reward == None and prevAction == None:
            self.addInputSequence(stateSequence)

        if r.random() < exploreProb:
            return r.choice(self.actionList)
        
        stateEnd = len(abstractSequence)
        for state, stateTable in self.QTable.items():
            if state[0:stateEnd] != abstractSequence:
                continue
            for action, thisReward in stateTable.items():
                if state in potentialGoals and potentialGoals[state][1] > thisReward:
                    continue
                if thisReward > minGoal:
                    potentialGoals[state] = (action,thisReward)

        if debug:
            print(potentialGoals)

        (action, expectedReward, storage) = self.improvedTreeSearch(abstractSequence, depth, potentialGoals, 0.5, debug)
        if action == None:
            return r.choice(self.actionList)

        return action


    #Helpful functions
    def bestActionAndReward(self, state):
        bestReward = -99999999999999
        bestAction = None
        
        if state not in self.QTable:
            return (bestAction, bestReward)
        stateTable = self.QTable[state]

        for action in stateTable:
                if stateTable[action] > bestReward:
                    bestReward = stateTable[action]
                    bestAction = action

        return (bestAction, bestReward)

    def possibleGoalSequences(self, stateSequence, goals):
        stateEnd = len(stateSequence)
        possibleGoals = {}
        for sequence in goals:
            if sequence[0:stateEnd] == stateSequence:
                possibleGoals[sequence] = goals[sequence]
        return possibleGoals
       
    def topQEntries(self, number = 10):
        topList = [("","",-9999)]*number
        for state, stateTable in self.QTable.items():
            for action, reward in stateTable.items():
                for (anotherState, anotherAction, anotherReward) in topList:
                    if reward > anotherReward:
                        topList.append((state, action, reward))
                        topList.remove((anotherState, anotherAction, anotherReward)) 
                        state = anotherState
                        action = anotherAction
                        reward = anotherReward
        return topList

    #Given a state and an action finds the dictionary with the most useful transitions and the number of inserts to that dictionary
    def getTransitions(self, state, action):
        if (state, action) in self.TransitionTable:
            return self.TransitionTable[(state,action)]
        gotAction = (action) in self.TransitionTable
        gotState = (state) in self.TransitionTable
        if gotAction and not gotState:
            return self.TransitionTable[(action)]
        elif gotState and not gotAction:
            return self.TransitionTable[(state)]
        elif gotAction and gotState:
            (actionInserts, actionTransitions) = self.TransitionTable[(action)]
            (stateInserts, stateTransitions) = self.TransitionTable[(state)]
            actionEntropy = sum(map(lambda x: (actionTransitions[x]/actionInserts)**2, actionTransitions))
            stateEntropy = sum(map(lambda x: (stateTransitions[x]/stateInserts)**2, stateTransitions))
            if actionEntropy > stateEntropy:
                return self.TransitionTable[(action)]
            else:
                return self.TransitionTable[(state)]
        return (0,[])

    #Given a sequence and a goal finds the probability that one can successfully navigate from one to the other
    def reliabilityToGoal(self, sequence, goal, returnBestPath = False):
        
        if sequence != goal[0:len(sequence)]:
            if returnBestPath:
                return (0, None)
            return 0

        position = len(sequence)
        state = sequence[-1]
        reliability = 1
        actions = []
        while True:
            if position >= len(goal):
                if position > len(goal):
                    reliability = 0
                break  
            nextState = goal[position]
            actionReliability  = 0
            bestAction = None
            for action in self.actionList:
                (nrOfInserts, transitions) = self.getTransitions(state, action)
                if nextState in transitions and transitions[nextState]/nrOfInserts > actionReliability:
                    actionReliability = transitions[nextState]/nrOfInserts
                    bestAction = action
            if actionReliability == 0:
                if returnBestPath:
                    return (0, None)
                return 0
            position += 1
            reliability *= actionReliability
            state = nextState
            actions.append(bestAction)

        if returnBestPath:
            return(reliability, actions)
        return reliability

    #Takes the previous state, action, and current state and updates Q and E Tables
    def oneStateLearning(self, oldState, action, newState, reward, discount = None):
        if discount == None:
            discount = self.discountFactor
        if oldState not in self.QTable:
            self.QTable[oldState] = {}
            self.ETable[oldState] = {}
        oldStateQ = self.QTable[oldState]
        oldStateE = self.ETable[oldState]
        (bestAction, bestReward) = self.bestActionAndReward(newState)
        if bestAction == None:
            bestReward = 0
        if action in oldStateQ:
            q = oldStateQ[action]
            e = oldStateE[action]
        else:
            q = 0
            e = 0
        
        q = (1-self.learningRate)*q + self.learningRate*(reward + discount*bestReward)
        e = (1-self.learningRate)*e + self.learningRate*reward

        oldStateQ[action] = q
        oldStateE[action] = e



    #Transition table

    def updateTransitionTable(self, oldState, action, newState):
        if (oldState, action) in self.TransitionTable:
            (nrOfInserts, nextStates) = self.TransitionTable[(oldState, action)]
            if newState in nextStates:
                nextStates[newState] += 1
            else:
                nextStates[newState] = 1
            self.TransitionTable[(oldState, action)] = (nrOfInserts+1, nextStates)
        else:
            self.TransitionTable[(oldState, action)] = (1, {newState : 1})

        if (oldState) in self.TransitionTable:
            (nrOfInserts, nextStates) = self.TransitionTable[(oldState)]
            if newState in nextStates:
                nextStates[newState] += 1
            else:
                nextStates[newState] = 1
            self.TransitionTable[(oldState)] = (nrOfInserts+1, nextStates)
        else:
            self.TransitionTable[(oldState)] = (1, {newState : 1})

        if (action) in self.TransitionTable:
            (nrOfInserts, nextStates) = self.TransitionTable[(action)]
            if newState in nextStates:
                nextStates[newState] += 1
            else:
                nextStates[newState] = 1
            self.TransitionTable[(action)] = (nrOfInserts+1, nextStates)
        else:
            self.TransitionTable[(action)] = (1, {newState : 1})
    
    def addInputSequence(self, sequence):
        self.inputSet.add(sequence)

    #Takes a rewarded sequence and adds it to the tree of rewareded sequences
    def addRewardedSequence(self, sequence, reward = None, action = None):
        nextChar = sequence[-1]
        branch = self.rewardedSequences
        for x in range(len(sequence)):            
            char = nextChar
            if x < len(sequence)-1:
                nextChar = sequence[-(x+2)]
            else:
                nextChar = 1
            if char not in branch.connections:
                branch.connections[char] = Tree()
                branch.connections[char].node = False
            if nextChar == 1:
                branch.connections[char].node = True
            branch = branch.connections[char]

        nextChar = sequence[0]
        branch = self.rewardedSequencesForward
        for x in range(len(sequence)):
            char = nextChar
            if x < len(sequence)-1:
                nextChar = sequence[x+1]
            else:
                nextChar = 1
            if char not in branch.connections:
                branch.connections[char] = Tree()
                branch.connections[char].node = None
            if nextChar == 1:
                branch.connections[char].node = (action, reward)
            branch = branch.connections[char]

    #Takes a rewarded sequence and returns the list of rewarded sequences closest to that one together with the position of the split
    def findClosestRewardedSequences(self, sequence):
        split = 0
        splitNode = None
        nodeAfterSplit = None
        branch = self.rewardedSequences
        for x in range(len(sequence)):
            char = sequence[-(x+1)]

            if char not in branch.connections:
                break

            if len(branch.connections) > 1:
                split = x
                splitNode = branch
                nodeAfterSplit = branch.connections[char]

            branch = branch.connections[char]

        if splitNode == None:
            return ([], None)

        returnSequences = []
        branch = splitNode
        queue = []
        for char, twig in branch.connections.items():
            if twig != nodeAfterSplit:
                queue.append((char, twig, list([sequence[-split:len(sequence)]])))

        while len(queue) > 0:
            (char, branch, seq) = queue.pop()
            sequence = list(seq)
            sequence.insert(0,char)
            
            if branch.node == True:
                returnSequences.append("".join(sequence))

            for symbol, twig in branch.connections.items():
                queue.append((symbol, twig, list(sequence)))

        return (returnSequences, split)

    def sequenceInRewarded(self, sequence, canLeadTo = True, debug = False):
        branch = self.rewardedSequencesForward
        for char in sequence:
            if char not in branch.connections:
                if debug:
                    print("char not in connections: {} in {}".format(char, sequence))
                return (False, None)
            branch = branch.connections[char]
        if canLeadTo or branch.node != None:
            return (True, branch)
        if debug:
            print("sequence cannot lead to anything: {}".format(sequence))
        return (False, None)

    #Next Gen Tree-Search
    #sequence is a string with each char a state in the history states
    #depth is the maximum depth of the branch
    #goals is a dictionary with sequences as keys and (bestAction, reward) as value
    #distanceToGoalDiscount is a factor of how much of the goal reward is given to an end state depending on the distance to the nearest goal
    def improvedTreeSearch(self, sequence, depth, goals, distanceToGoalDiscount = 0, debug = False):
        if sequence in goals:
            (bestAction, reward) = goals[sequence]
            return (bestAction, reward, (sequence, reward, reward, None, None))

        if depth == 0:
            (bestAction, reward) = self.bestActionAndReward(sequence)
            reward = 0 
            for goal, (action, aReward) in goals.items():
                if self.reliabilityToGoal(sequence, goal)*aReward > reward:
                    reward = self.reliabilityToGoal(sequence, goal)*aReward
                    bestAction = action
            return (bestAction, reward, (sequence, reward, reward, None, None))

        nextSequences = set()
        for action in self.actionList:
            (_, nextStates) = self.getTransitions(sequence[-1], action)
            if len(nextStates) > 0:
                for nextState in nextStates:
                    nextSequences.add(sequence + nextState)

        returns = {}
        for nextSequence in nextSequences:
            possibleGoals = self.possibleGoalSequences(nextSequence, goals)
            if len(possibleGoals) == 0:
                (bestAction, reward)  = self.bestActionAndReward(nextSequence)
                returns[nextSequence] = (bestAction, reward, (nextSequence, reward, reward, None, None))
            else:
                returns[nextSequence] = self.improvedTreeSearch(nextSequence, depth-1, possibleGoals, distanceToGoalDiscount, debug)

        bestAction = None
        bestReward = -999999
        bestNextSequence = None
        thisReward = bestReward


        for action in self.actionList:
            thisNextSequence = None
            reward = -9999999
            myReward = reward
            (nrOfInserts, nextStates) = self.getTransitions(sequence[-1], action)
            if nrOfInserts == 0:
                if sequence in self.QTable and action in self.QTable[sequence]:
                    myReward = self.QTable[sequence][action]
                    reward = myReward
            else:
                if sequence in self.ETable and action in self.ETable[sequence]:
                    myReward = self.ETable[sequence][action]
                else:
                    myReward = 0
                reward = myReward
                for nextState in nextStates:
                    nextSequence = sequence + nextState
                    reward += returns[nextSequence][1]*(nextStates[nextState]/nrOfInserts)
            if reward > bestReward:
                bestAction = action
                bestReward = reward
                thisReward = myReward
        if bestAction == None:
            bestAction = r.choice(self.actionList)
        if not debug:
            returns = None
        return (bestAction, bestReward, (sequence, thisReward, bestReward, returns, None))

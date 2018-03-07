import random as r
from graph import *

class Solver():
    
    #Constructors

    def __init__(self, actionList, learningRate, discountFactor):
        self.actionList = actionList
        self.learningRate = learningRate
        self.discountFactor = discountFactor
        
        self.TransitionTable = {}
        self.QTable = {}
        self.ETable = {}

    #Runnable


    def simpleMultiStateProgram(self, stateSequence, depth=4, exploreProb=0, prevAction=None, reward=None):
        if prevAction != None:
            self.oneStateLearning(stateSequence[:-1], prevAction, stateSequence, reward)
            self.updateTransitionTable(stateSequence[-2], prevAction, stateSequence[-1])

        if r.random() < exploreProb:
            return r.choice(self.actionList)

        (action, expectedReward) = self.simpleMultiStateTreeSearch(stateSequence, depth)

        if action == None:
            return r.choice(self.actionList)

        return action

    def multiStateProgram(self, stateSequence, depth = 4, exploreProb = 0, prevAction=None, reward=None, additionalGoalStates = {}, goalReward = 0.1, debug = False):
        if prevAction != None:
            self.oneStateLearning(stateSequence[:-1], prevAction, stateSequence, reward)
            self.updateTransitionTable(stateSequence[-2], prevAction, stateSequence[-1])

        if r.random() < exploreProb:
            return r.choice(self.actionList)

        bestGain = -99999
        stateEnd = len(stateSequence)
        possibleStates = []
        for (state, action), gain in self.QTable.items():
            if state[0:stateEnd] == stateSequence:
                possibleStates.append((state,action))
                if gain > bestGain:
                    bestGain = gain 
        goodStates = additionalGoalStates
        for (state, action) in possibleStates:
            if self.QTable[(state,action)] > bestGain-goalReward:
                if state in goodStates and goodStates[state][1] < self.QTable[(state,action)]:
                    goodStates[state] = (action, self.QTable[(state,action)])
        
        #if exploreProb == 0:
        #    print(goodStates)
        if debug:
            #print(possibleStates)
            print(goodStates)

        (action, expectedReward, storage) = self.improvedTreeSearch(stateSequence, depth, goodStates, 0.5, debug)
 
        if action == None:
            return r.choice(self.actionList)
        if debug:
            if len(additionalGoalStates[0]) > 0: 
                print("AbstractState: {}, AbstractGoalStates: {}, ActionTaken: {}".format(stateSequence, additionalGoalStates, action))
                print(storage[1])
                gra = GRA()
                gra.addNodes(storage)
                gra.plotGraph()

        return action

    #Helpful functions
    
    def bestActionAndReward(self, state):
        bestReward = -99999999999999
        bestAction = None
        
        for action in self.actionList:
            if (state, action) in self.QTable:
                if self.QTable[(state, action)] > bestReward:
                    bestReward = self.QTable[(state, action)]
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
        for (state,action), reward in self.QTable.items():
            for (anotherState, anotherAction, anotherReward) in topList:
                if reward > anotherReward:
                    topList.append((state, action, reward))
                    topList.remove((anotherState, anotherAction, anotherReward)) 
                    state = anotherState
                    action = anotherAction
                    reward = anotherReward
        return topList

    def getTransitions(self, state, action):
        if (state, action) in self.TransitionTable:
            return self.TransitionTable[(state,action)]
        gotAction = (action) in self.TransitionTable
        gotState = (state in self.TransitionTable)
        if gotAction and not gotState:
            return self.TransitionTable[(action)]
        elif gotState and not gotAction:
            return self.TransitionTable[(state)]
        elif gotAction and gotState:
            (actionInserts, actionTransitions) = self.TransitionTable[(action)]
            (stateInserts, stateTransitions) = self.TransitionTable[(state)]
            actionEntropy = sum(map(lambda x: (actionTransitions[x]/actionInserts)**2))
            stateEntropy = sum(map(lambda x: (stateTransitions[x]/stateInserts)**2))
            if actionEntropy > stateEntropy:
                return self.TransitionTable[(action)]
            else:
                return self.TransitionTable[(state)]
        return (0,[])

    #oneState methods. Used when we do not wish to consider any smaller version of the state

    def oneStateQ(self, state, exploreProb=0):
        
        if r.random() < exploreProb:
            return r.choice(self.actionList)

        (bestAction, bestReward) = self.bestActionAndReward(state)

        if bestAction == None:
            return r.choice(self.actionList)

        return bestAction

    def oneStateLearning(self, oldState, action, newState, reward):
        if (oldState, action) in self.QTable:
            q = self.QTable[(oldState, action)]
            (bestAction, bestReward) = self.bestActionAndReward(newState)
            if bestAction == None:
                bestReward = 0
            q = (1-self.learningRate)*q + self.learningRate*(reward + self.discountFactor*bestReward)
            self.QTable[(oldState, action)] = q

            e = self.ETable[(oldState, action)]
            e = (1-self.learningRate)*e + self.learningRate*reward
            self.ETable[(oldState, action)] = e

        else:
            self.QTable[(oldState,action)] = reward
            self.ETable[(oldState,action)] = reward




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


    def oneStateTranstionTreeSearch(self, state, depth):
        if depth == 0:
            return bestActionAndReward(state)
        
        bestAction = None
        bestReward = -999999999999

        for action in self.actionList:
            actionReward = 0
            if (state, action) in self.ETable:
                actionReward = self.ETable[(state, action)]
            if (state, action) in self.TransitionTable:
                (nrOfInserts, nextStates) = self.TransitionTable[(state, action)]
                for nextState in nextStates:
                    (nextStateAction, nextStateReward) = oneStateTransitionTreeSearch(nextState, depth-1)
                    actionReward += (nextStates[nextState]/nrOfInserts) * nextStateReward
                if actionReward > bestReward:
                    bestReward = actionReward
                    bestAction = action
            elif (state,action) in self.QTable:
                actionReward = self.QTable[(state,action)]

        return (bestAction, bestReward)

    #Baby's first tree-serach

    def simpleMultiStateTreeSearch(self, stateSequence, depth, debug = False):
        if depth == 0:
            return self.bestActionAndReward(stateSequence)

        bestAction = None
        bestReward = -999999999999

        for action in self.actionList:
            actionReward = 0
            if (stateSequence, action) in self.ETable:
                actionReward = self.ETable[(stateSequence, action)]
            if (stateSequence[-1], action) in self.TransitionTable:
                (nrOfInserts, nextStates) = self.TransitionTable[(stateSequence[-1], action)]
                for nextState in nextStates:
                    (nextStateAction, nextStateReward) = self.simpleMultiStateTreeSearch(stateSequence + nextState, depth-1)
                    if nextStateAction == None:
                        nextStateReward = 0
                    actionReward += (nextStates[nextState]/nrOfInserts) * nextStateReward
                if actionReward > bestReward:
                    bestReward = actionReward
                    bestAction = action
            elif (stateSequence, action) in self.QTable:
                actionReward = self.QTable[(stateSequence,action)]

        return (bestAction, bestReward)


    #Smarter Tree-Search
    
    def sequenceTreeSearch(self, stateSequence, depth, goalSequences, debug = False, abstractGoals = ([],[])):
        if depth == 0:
            (bestAction, bestReward) = self.bestActionAndReward(stateSequence)
            return (bestAction, bestReward, ([],[]))

        bestAction = None
        bestReward = -99999999
        nextStorage = ([],[])
        thisStorage = ([],0)

        for action in self.actionList:
            actionReward = 0
            if (stateSequence, action) in self.ETable:
                actionReward = self.ETable[(stateSequence, action)]
            elif (stateSequence, action) in abstractGoals[0]:
                actionReward = 0.9 ##Super hardcoded
            thisReward = actionReward

            if (stateSequence[-1],action) in self.TransitionTable:
                (nrOfInserts, nextStates) = self.TransitionTable[(stateSequence[-1], action)]
                for nextState in nextStates:
                    nextSequence = stateSequence + nextState
                    possibleGoals = self.possibleGoalSequences(nextSequence, goalSequences)
                    if len(possibleGoals) == 0:
                        continue
                    (nextStateAction,nextStateReward,nextStorage) = self.sequenceTreeSearch(nextSequence, depth-1, possibleGoals)
                    actionReward += (nextStates[nextState]/nrOfInserts) * nextStateReward
            elif (stateSequence, action) in self.QTable:
                actionReward = self.QTable([stateSequence,action])
            elif (stateSequence,action) in abstractGoals[0]:
                actionReward = 0.9

            thisStorage[0].append((action, thisReward, actionReward))

            actionReward = actionReward
            #if value >= bestValue and actionReward >= bestReward:
                #if actionReward > bestReward or value > bestValue or r.random() < 2/len(self.actionList):
            if actionReward >= bestReward:
                if actionReward > bestReward or r.random() < 2/len(self.actionList):
                    bestReward = actionReward
                    bestAction = action
                    storage = nextStorage
                    thisStorage = (thisStorage[0],self.actionList.index(bestAction))
        (layers, anchors) = storage
        layers.insert(0, thisStorage[0])
        anchors.insert(0, thisStorage[1])
        return (bestAction,bestReward,storage)


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
            distanceToGoal = 0
            if len(goals) > 0:
                distanceToGoal = min(map(len, goals))
            reward += distanceToGoalDiscount**distanceToGoal
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

        for action in self.actionList:
            thisReward = -9999999
            thisNextSequence = None
            reward = thisReward
            (nrOfInserts, nextStates) = self.getTransitions(sequence[-1], action)
            if len(nextStates) == 0:
                if (sequence, action) in self.QTable:
                    thisReward = self.QTable[(sequence, reward)]
                    reward = thisReward
            else:
                if (sequence, action) in self.ETable:
                    thisReward = self.ETable[(sequence, action)]
                else:
                    thisReward = 0
                reward = thisReward
                for nextState in nextStates:
                    nextSequence = sequence + nextState
                    reward += returns[nextSequence][1]*(nextStates[nextState]/nrOfInserts)
            if reward > bestReward:
                bestAction = action
                bestReward = reward
        if bestAction == None:
            bestAction = r.choice(self.actionList)
        if not debug:
            returns = None
        return (bestAction, bestReward, (sequence, thisReward, reward, returns, None))

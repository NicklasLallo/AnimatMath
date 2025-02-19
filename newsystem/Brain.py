import random as r 

class Brain():
    
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

    def multiStateProgram(self, stateSequence, depth = 4, exploreProb = 0, prevAction=None, reward=None, goalReward = 0.1, debug = False):
        if prevAction != None:
            self.oneStateLearning(stateSequence[:-1], prevAction, stateSequence, reward)
            self.updateTransitionTable(stateSequence[-2], prevAction, stateSequence[-1])

        if r.random() < exploreProb:
            return r.choice(self.actionList)

        bestGain = -99999
        stateEnd = len(stateSequence)
        possibleStates = []
        for (state, action), gain in self.ETable.items():
            if state[0:stateEnd] == stateSequence:
                possibleStates.append((state,action))
                if gain > bestGain:
                    bestGain = gain 
        goodStates = []
        for (state, action) in possibleStates:
            if self.ETable[(state,action)] > bestGain-goalReward:
                goodStates.append(state)

        if debug:
            #print(possibleStates)
            print(goodStates)

        (action, expectedReward, actionValue) = self.sequenceTreeSearch(stateSequence, depth, goodStates, debug)
 
        if action == None:
            return r.choice(self.actionList)

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

    def possibleGoalSequences(self, stateSequence, goalSequences):
        stateEnd = len(stateSequence)
        possibleGoals = []
        for sequence in goalSequences:
            if sequence[0:stateEnd] == stateSequence:
                possibleGoals.append(sequence)
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
    
    def sequenceTreeSearch(self, stateSequence, depth, goalSequences, debug = False):
        if depth == 0:
            (bestAction, bestReward) = self.bestActionAndReward(stateSequence)
            return (bestAction, bestReward, 1)

        bestAction = None
        bestReward = -99999999
        bestValue  = 0

        for action in self.actionList:
            actionReward = 0
            value = 0
            if (stateSequence, action) in self.ETable:
                actionReward = self.ETable[(stateSequence, action)]

            if (stateSequence[-1],action) in self.TransitionTable:
                value = 1
                (nrOfInserts, nextStates) = self.TransitionTable[(stateSequence[-1], action)]
                for nextState in nextStates:
                    nextSequence = stateSequence + nextState
                    possibleGoals = self.possibleGoalSequences(nextSequence, goalSequences)
                    if len(possibleGoals) == 0:
                        value -= (nextStates[nextState]/nrOfInserts)
                        continue
                    (nextStateAction,nextStateReward,nextStateValue) = self.sequenceTreeSearch(nextSequence, depth-1, possibleGoals)
                    actionReward += (nextStates[nextState]/nrOfInserts) * nextStateReward
                    value -= (1 - nextStateValue)*(nextStates[nextState]/nrOfInserts)
            elif (stateSequence, action) in self.QTable:
                value = 0.25
                actionReward = self.QTable([stateSequence,action])

            actionReward = actionReward
            #if value >= bestValue and actionReward >= bestReward:
                #if actionReward > bestReward or value > bestValue or r.random() < 2/len(self.actionList):
            if actionReward >= bestReward:
                if actionReward > bestReward or r.random() < 2/len(self.actionList):
                    bestReward = actionReward
                    bestAction = action
                    bestValue = value
        return (bestAction,bestReward,bestValue)




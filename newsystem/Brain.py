import random as r 

class Brain():
    
    #Constructors

    def __init__(self, actionList, learningRate, discountFactor):
        self.actionList = actionList
        self.learningRate = learningRate
        self.discountFactor = discountFactor
        
        TransitionTable = {}
        QTable = {}
        ETable = {}
        
    #Helpful functions
    
    def bestActionAndReward(self, state):
        bestReward = -99999999999999
        bestAction = None
        
        for action in actionList:
            if (state, action) in self.QTable:
                if self.QTable[(state, action)] > bestActionReward:
                    bestReward = self.QTable[(state, action)]
                    bestAction = action

        return (bestAction, bestReward)
       

    #oneState methods. Used when we do not wish to consider any smaller version of the state

    def oneStateQ(self, state, exploreProb):
        
        if r.random < exploreProb:
            return r.choice(self.actionList)

        (bestAction, bestReward) = self.bestActionAndReward(state)

        if bestAction = None:
            return r.choice(self.actionList)

        return bestAction

    def oneStateLearning(self, oldState, action, newState, reward):
        if (oldState, action) in self.QTable:
            q = self.QTable[(oldState, action)]
            (bestAction, bestReward) = self.bestActionAndReward(newState)
            if bestAction = None:
                bestReward = 0
            q = (1-self.learningRate)*q + self.learningRate*(reward + self.discountFactor*bestReward)
            self.QTable[(oldState, acton)] = q

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

    def simpleTranstionTreeSearch(self, state, depth):
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
                    (nextStateAction, nextStateReward) = simpleTransitionTreeSearch(nextState, depth-1)
                    actionReward += (nextStates[nextState]/nrOfInserts) * nextStateReward
                if actionReward > bestReward:
                    bestReward = actionReward
                    bestAction = action
            elif (action, reward) in self.QTable:
                actionReward = self.QTable[(state,Action)]

        return (bestAction, bestReward)


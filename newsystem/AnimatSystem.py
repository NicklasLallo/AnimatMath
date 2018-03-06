from Abstracter import *
from Solver import *
import random as r

def systemOnFile(input_file, )


class AnimatSystem():

    #Constructor
    def __init_(self, memoryLength = None):
        self.memory = []
        self.memoryLength = memoryLength
        self.abstraction = []
        self.solver = Solver()
        self.abstracter = Abstracter()
    
    #Running the system one step
    def run(state, reward):
        self.learn(reward)
        self.memory.append(state)
        if self.memoryLength != None and len(self.memory) > self.memoryLength:
            del self.memory[0]
        self.abstraction = self.abstracter.minimize(self.memory)
        action = self.solver.solve(self.memory, abstraction)
        return action

    #Learning
    def learn(reward):
        pass

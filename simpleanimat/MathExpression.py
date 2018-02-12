import numpy as np
import random as r

class MathExpression:
    intRange = 9
    parPercentage = 0.5
    minDepth = 2
    maxDepth = 12

    def __init__(self, complexitylvl=1):
        pass

    def genExp():
        exp = {}
        boolean = False

        #determine if the expression should be correct or not
        if r.random() < 0.5:
            boolean = True

        (lHand,rHand) = MathExpression.subT(r.randrange(MathExpression.minDepth,MathExpression.maxDepth))
        
        if not boolean:
            rHand = MathExpression.fakeO(rHand)
        
        return (lHand + '=' + str(rHand), boolean)


    def subT(depth, OpL = ['*', '+', '-']): #TODO, solve integer division
        n = len(OpL) #cases
        c = r.randrange(1,n)
        
        if depth == 1:
            i = r.randrange(0,MathExpression.intRange)
            return (str(i),i)
        else:
            (ex1, val1) = MathExpression.subT(r.randrange(1, depth), OpL)
            operand = OpL[c] 
            (ex2, val2) = MathExpression.subT(r.randrange(1, depth), OpL)
            i = MathExpression.evaluateExp (val1, val2, operand)
           # if r.random() < MathExpression.parPercentage:
           #     return (ex1 + operand + ex2, i)
           # else:
            return ('(' + ex1 + operand + ex2 + ')', i)

    def evaluateExp(val1, val2, operand):
        if operand == '*':
            return val1*val2
        elif operand == '+':
            return val1+val2
        elif operand == '-':
            return val1-val2
        elif operand == '/':
            return val1/val2
        else:
            raise UnicodeError('Nonexistant operand')
            return 4
    
    def fakeO(correctO):
        if correctO == 0:
            return r.randrange(-intRange,intRange)
        candidate = r.randrange((-2)*abs(correctO),2*abs(correctO))
        if candidate != correctO:
            return candidate
        else:
            return fakeO(correctO)

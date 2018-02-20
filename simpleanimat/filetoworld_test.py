from Controller import *



world = oldconfigToWorld('example-4-seq.json')


for x in range(1000):
    world.worldStep()
    (animat, pos, animatType) = world.animats[0]
    needValues = animat.needValues
    print('Animat at pos {} has hunger {} and thirst {}'.format(pos, needValues[1], needValues[0]))


(animat, pos, animatType) = world.animats[0]
bTable(animat.qTable,2,animat.nodeNr,7,['thirst','hunger'],['eat','drink','left','right','up','down','wait'])

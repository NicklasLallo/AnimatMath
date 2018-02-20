from Controller import *



world = oldconfigToWorld('example-4-seq.json')


for x in range(1000):
    world.worldStep()
    (animat, pos, animatType) = world.animats[0]
    needValues = animat.needValues
    print('Animat at pos {} has hunger {}'.format(pos, needValues[0]))


(animat, pos, animatType) = world.animats[0]
bTable(animat.qTable,1,animat.nodeNr,5,['hunger'],['right','up','left','down','eat'])

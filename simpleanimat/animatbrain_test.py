from AnimatBrain import *

position = 0

reward = [0]

animat = AnimatBrain(2,2,1,0.2,0.5,0,0.4,0.0)


for x in range(0,10):

    if position == 0:
        attributes = np.array([1,0])
    else:
        attributes = np.array([0,1])

    action = animat.program(attributes, reward)
    print('Action: {}, Position: {}'.format(action, position))
    if action != position:
        position = action
        reward[0] = 0.5
        print('good!')
    else:
        reward[0] = -0.5
        print('bad')

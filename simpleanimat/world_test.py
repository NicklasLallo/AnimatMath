from World import World
import numpy as np

world = World(['hot','red','sweet'])
world.addNode('a')
world.addNode('b')
print(world.graph)
world.addEdge('a','b')
print(world.graph)
world.setAttribute('a', 'hot')
print(world.graph)
world.setAttributes('b', np.array([1,0,1]))
print(world.graph)


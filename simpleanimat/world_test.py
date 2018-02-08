from World import World, createTapeWorld
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

tapeWorld = createTapeWorld(['green', 'a', '+','4546', 'Hawk'], [np.array([0,0,0,0,0]),np.array([1,0,0,0,0]),np.array([0,1,0,0,0]),np.array([0,0,1,0,0]),np.array([0,0,0,1,1])])
print(tapeWorld.graph)

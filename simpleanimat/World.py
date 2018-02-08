import numpy as np

class World:

    def __init__(self, attributes=[]):
        self.attributes = attributes
        self.graph = {}

    def addNode(self, node, attributes = []):
        if node in self.graph:
            raise ValueError('Node: {} already in graph'.format(node))
        self.graph[node] = ([],np.zeros(len(self.attributes)))
        for attribute in attributes:
            setAttribute(node, attribute)
    
    def addEdge(self, start, end): 
        if start not in self.graph:
            raise ValueError('Node: {} already in graph'.format(start))
        if end not in self.graph:
            raise ValueError('Node: {} already in graph'.format(end))
        (neighbors, attr) = self.graph[start]
        neighbors.append(end)

    def setAttribute(self, node, attribute, value = 1):
        if attribute not in self.attributes:
            raise ValueError('Attribute: {} does not exist in this world'.format(attribute))
        if node not in self.graph:
            raise ValueError('Node: {} already in graph'.format(node))
        (neighbors, attr) = self.graph[node]
        index = self.attributes.index(attribute)
        attr[index] = value

    def setAttributes(self, node, attrs):
        if node not in self.graph:
            raise ValueError('Node: {} already in graph'.format(node))
        if attrs.size != len(self.attributes):
            raise ValueError('There are {} attributes but you provided values for {}'.format(len(self.attributes),attrs.size))
        (neighbors, a) = self.graph[node]
        np.copyto(a,attrs)

    def getAttributes(self, node):
        return self.graph[node][1]

    def getAttribute(self, node, attribute):
        (neighbors, attrs) = self.graph[node]
        index = self.attributes.index(attribute)
        return attrs[index]

    def getNeighbors(self, node):
        return self.graph[node][0]

    def getSize(self):
        return len(graph)

#Takes a list of all attributes and a list of setattribute arrays and creates the tapeworld with nodes connected in a tape
def createTapeWorld(attributes, allAttributes):
    tapeWorld = World(attributes)
    node = 0
    for attrs in allAttributes:
        tapeWorld.addNode(node)
        if node != 0:
            tapeWorld.addEdge(node, node-1)
            tapeWorld.addEdge(node-1, node)
        tapeWorld.setAttributes(node, attrs)
        node += 1
    return tapeWorld



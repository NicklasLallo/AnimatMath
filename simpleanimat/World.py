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
        a = attrs




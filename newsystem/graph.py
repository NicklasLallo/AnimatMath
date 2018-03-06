import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


class GRA():

    def __init__(self):
        self.G = nx.Graph()
        self.ind = 0

    def addNodes(self, nodes=([[("act","val","totVal")]], [])):
    
        # G.add_nodes_from(range(0,len(nodes)))
        (layers, anchors) = nodes
        layer = 0
        for n in layers:
            layer += 1
    
            xpos = 0
            for node in n:
    
                self.G.add_node(self.ind, pos=(xpos,layer), label="{} {} {}".format(node[0],node[1],node[2]))
                self.G.add_edge(anchors[layer]+10*layer, self.ind)
                self.ind += 1
                xpos += 1
    
    
    
    def plotGraph(self):
        pos = nx.get_node_attributes(self.G,'pos')
        labels = nx.get_node_attributes(self.G,'label')
        nx.draw(self.G,pos,labels)
    
    



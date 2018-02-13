import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


def bGraph(nodes):
    G = nx.DiGraph()

    G.add_nodes_from(range(0,len(nodes)))
    colorVals = []
    labels = {}
    i = 0
    for node in nodes:
        colorVals.append('#A0CBE2')
        if nodes[node][1] == 1:
            colorVals[i] = 'r'
        if nodes[node][0] == 0:
            colorVals[i] = 'g'
        i += 1

        if nodes[node][0] == 1 or nodes[node][0] == 2:
            G.add_edge(nodes[node][2], node)
            G.add_edge(nodes[node][3], node)

        if nodes[node][0] == 0:
            labels[node]= 'SEN ' + str(node)
        elif nodes[node][0] == 1:
            labels[node]= 'AND ' + str(node)
        elif nodes[node][0] == 2:
            labels[node]= 'SEQ ' + str(node)


    #pos = nx.spring_layout(G)
    pos = graphviz_layout(G, prog='dot')
    #nx.drawing.nx_agraph.write.write_dot()
    nx.draw_networkx_nodes(G, pos, xmap=plt.get_cmap('jet'), node_color = colorVals, node_size = 600)
    nx.draw_networkx_labels(G, pos, labels=labels, font_weight = 'normal')
    nx.draw_networkx_edges(G, pos)
    plt.show()


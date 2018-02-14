import plotly.offline as py
import plotly.graph_objs as go
import numpy as np
import random as r

def bTable(qrTable, nrOfNeeds, nrOfNodes, nrOfActions, needNames = [], actionNames = []):
    data = []
    for need in range(0,nrOfNeeds):
        columns = []
        column = []

        for node in range(0,nrOfNodes):
            column.append(str(node))
        columns.append(column)


        for action in range(0,nrOfActions):
            column = []
            for node in range(0,nrOfNodes):
                column.append(qrTable[(need,node,action)])
            columns.append(column)

        if needNames == []:
            needName = need
        else:
            needName = needNames[need]
        head = ['{}: Node\\Action'.format(needName)]
        for action in range(0,nrOfActions):
            if actionNames == []:
                head.append(str(action))
            else:
                head.append(actionNames[action])
        data.append(
            go.Table(
                header=dict(values = head),
                cells =dict(values = columns)
            )
        )
    layout = dict(width=1000, height = 400)
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename = 'bTable.html')


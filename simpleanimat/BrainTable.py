import plotly.offline as py
import plotly.graph_objs as go
import numpy as np
import random as r

def bTable(qrTable, nrOfNeeds, nrOfNodes, nrOfActions, needNames = [], actionNames = []):
    
    #Settings
    height = 600
    width  = 1000
    margin = 10
    digitsOfPrecision = 3
    

    m = margin/width
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
                column.append(round(qrTable[(need,node,action)], digitsOfPrecision))
            columns.append(column)

        if needNames == []:
            needName = need
        else:
            needName = needNames[need]
        head = ['{}\nNode\\Action'.format(needName)]
        for action in range(0,nrOfActions):
            if actionNames == []:
                head.append(str(action))
            else:
                head.append(actionNames[action])
        data.append(
            go.Table(
                domain=dict(x=[need/nrOfNeeds,(need+1-m)/nrOfNeeds], y=[0,1]),
                header=dict(values = head),
                cells =dict(values = columns)
            )
        )

    axis = dict()

    layout = dict(
        width       = width,
        height      = height,
        autosize    = True,
        showlegend  = False,
    )

    #for need in range(nrOfNeeds):
    #    layout['xaxis{}'.format(need+1)] = dict(axis, **dict(domain=[need/nrOfNeeds, need+1/nrOfNeeds]), anchor='x{}'.format(need+1))
    #    layout['yaxis{}'.format(need+1)] = dict(axis, **dict(domain=[0, 1]), anchor='y{}'.format(need+1))

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename = 'bTable.html')


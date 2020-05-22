from __future__ import division
import networkx as nx
import numpy as np
import random


#Levy flight with edge reinforcement
#a = number of max steps random walker can take
#b = edge reinforcement value
#c = levy coefficient (1 < c <= 3)
#d = graph object
#e = diameter



def generateLevy(a, b, c, d, e):
    G = d
    diam = e
    numberOfSteps = a  # set max number of steps
    deltaw = b  # edge reinforcement value
    x = np.arange(1, diam+1, 1)  # set upper bound for step size
    pdfLevy = np.power(1/x, c)  # set u value, where 1 <= u <= 3
    pdfLevy = pdfLevy/sum(pdfLevy)

    connectedNodes = list(G.edges)
    startCoord = random.choice(connectedNodes)
    levySourceNodes = []
    levyTargetNodes = []
    errwLevyWeights = []
    levySourceNodes.append(tuple(startCoord)[0])

    for k in range(0, numberOfSteps):
        stepSize = np.random.choice(x, p=pdfLevy)
        sourceNodes = []
        targetNodes = []

        if k == 0:
            sourceNodes.append(tuple(startCoord)[0])
        else:
            sourceNodes.append(levySourceNodes[k])

        for step in range(0, stepSize):
            nextNode = list(G.neighbors(sourceNodes[step]))
            s = [sourceNodes[step]] * len(nextNode)

            transitionProb = []
            for u, v in zip(s, nextNode):
                transitionProb.append(G.get_edge_data(u, v).get('weight'))
#            transitionProb = 1-np.array(transitionProb)
#            transitionProb[transitionProb < 0] = 0
            transitionProb = np.array(transitionProb)/sum(transitionProb)

            if len(transitionProb) == 1:
                targetNodes.extend(nextNode)
                sourceNodes.extend(nextNode)
            else:
                targetNodes.append(np.random.choice(nextNode, p=transitionProb))
                sourceNodes.append(targetNodes[-1])

            if step+1 == stepSize:
                if G.has_edge(sourceNodes[0], targetNodes[-1]):
                    G[sourceNodes[0]][targetNodes[-1]]['weight'] += deltaw
                    errwLevyWeights.append(G[sourceNodes[0]][targetNodes[-1]]['weight'])
                    levyTargetNodes.append(targetNodes[-1])
                    if k+1 == numberOfSteps:
                        break
                    else:
                        levySourceNodes.append(targetNodes[-1])
                else:
                    errwLevyWeights.append(0)
                    levyTargetNodes.append(targetNodes[-1])
                    if k+1 == numberOfSteps:
                        break
                    else:
                        levySourceNodes.append(targetNodes[-1])

    return levySourceNodes

import networkx as nx
import csv
import matplotlib.pyplot as plt
import random
from sklearn import linear_model
import numpy as np
import math
import sys


def frequency(dictVals):
    return { j:dictVals.count(j) for j in set(dictVals) }

def loadEdgeList(anomymizedEdges):
    G = nx.DiGraph()
    with open(anomymizedEdges,'rb') as file:
        content = csv.reader(file)
        for row in content:
            G.add_edge(row[0],row[1])

    in_degree = G.in_degree()
    out_degree = G.out_degree()

    in_freq = frequency(in_degree.values())
    out_freq = frequency(out_degree.values())

    
    plt.plot(in_freq.keys(),in_freq.values())
    plt.xlabel('in-degree')
    plt.ylabel('frequency')
    plt.show()

    plt.plot(out_freq.keys(),out_freq.values())
    plt.xlabel('out-degree')
    plt.ylabel('frequency')
    plt.show()

    lm = linear_model.LinearRegression()
    X= np.array([math.log(i) if i!=0 else 0  for i in in_freq.keys()])
    Y = np.array([ math.log(i) if i!=0 else 0  for i in  in_freq.values()])
    lm.fit(X[:,np.newaxis],Y)

    indegree_exponent = lm.predict(np.array([0]))

    print 'Indegree Exponent: {0}\n'.format( str( indegree_exponent))

    X= np.array([math.log(i) if i!=0 else 0 for i in out_freq.keys()])
    Y = np.array([ math.log(i) if i!=0 else 0 for i in  out_freq.values()])
    lm.fit(X[:,np.newaxis],Y)

    outdegree_exponent = lm.predict(np.array([0]))
    print 'Outdegree Exponent: {0}\n'.format( str(outdegree_exponent))


    noOfBridges = 0
    initialBridges = sum(1 for i in nx.weakly_connected.weakly_connected_components(G))
    tempG = G.copy()
    for e in G.edges():
        tempG.remove_edge(e[0],e[1])
        if sum(1 for i in nx.weakly_connected.weakly_connected_components(tempG)) > initialBridges:
            noOfBridges +=1
        tempG.add_edge(e[0],e[1])

    print 'Number of bridges: {0}\n'.format(str(noOfBridges))

    UG = G.to_undirected()

    print 'Number of 3 cycles: {0}\n'.format(str(sum(i for i in nx.triangles(UG).values())/3))

    print 'Graph Diameter: {0}\n'.format(str(nx.diameter(UG)))

    x = xrange(1,101)
    connectedlengths = []

    for i in x:
        tempG = UG.copy()
        totalEdges = UG.size()
        removeEdges = (i*totalEdges) /100
        for j in range(1,removeEdges):
            a = random.randrange(1,totalEdges)
            edge = tempG.edges()[a]
            tempG.remove_edge(edge[0],edge[1])
            totalEdges -= 1
        connectedlengths.append(len(max([i for i in nx.connected_components(tempG)],key=len)))

    plt.xlabel('%')
    plt.ylabel('Size of largest connected component')
    plt.plot(x,connectedlengths)
    plt.show()

try:
    if(len(sys.argv) != 2):
        print 'Usage \'P2.py filename\''
        sys.exit(-1)
    else:
        loadEdgeList(sys.argv[1])
except:
    print ''

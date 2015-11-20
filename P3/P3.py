import networkx as nx
import csv
import scipy as sp
import scipy.stats as st
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import sys

def loadEdgeList(anomymizedEdges):
    G = nx.DiGraph()
    UG = nx.Graph()
    with open(anomymizedEdges,'rb') as file:
        content = csv.reader(file)
        for row in content:
            G.add_edge(row[0],row[1])
    UG = G.to_undirected()



    print 'Average Local Clustering : {0}\n'.format(str(nx.average_clustering(UG)))

    print 'Global Clustering: {0}\n'.format(str(nx.transitivity(G)))

    print 'Page Rank Centrality:'
    pageRank = sorted(nx.pagerank_numpy(G).items(),key=lambda x:x[1])

    for i in pageRank[-10:]:
        print '{0}       {1}'.format(i[0],i[1])
    print ''
    print 'Eigenvector Centrality:'
    eigenVector = sorted(nx.centrality.eigenvector_centrality(G).items(),key=lambda x:x[1] )
    for i in eigenVector[-10:]:
        print '{0}       {1}'.format(i[0],i[1])
    print ''
    print 'Degree Centrality:'
    degreeCentrality = sorted(nx.centrality.in_degree_centrality(G).items(),key=lambda x:x[1])
    for i in degreeCentrality[-10:]:
        print '{0}       {1}'.format(i[0],i[1])
    print ''

    print 'Rank correlation between Pagerank Centrality and Eigenvector Centrality: ' ,st.spearmanr([i[1] for i in pageRank],[i[1] for i in eigenVector])[0]

    print 'Rank correlation between Pagerank Centrality and Degree Centrality: ',st.spearmanr([i[1] for i in pageRank],[i[1] for i in degreeCentrality])[0]

    print 'Rank correlation between Degree Centrality and Eigenvector Centrality: ',st.spearmanr([i[1] for i in degreeCentrality],[i[1] for i in eigenVector])[0]

    js = max([i for i in nx.algorithms.link_prediction.jaccard_coefficient(UG)], key = lambda x:x[2])
    print '\nNodes with max Jaccard Similarity : {0} {1}\n'.format(str(js[0]),str(js[1]))

 

    
try:
    if(len(sys.argv) != 2):
        print 'Usage \'p3.py filename\''
        sys.exit(-1)
    else:
        loadEdgeList(sys.argv[1])
except:
    print ''
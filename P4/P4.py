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
    return G, UG


def frequency(dictVals):
    return { j:dictVals.count(j) for j in set(dictVals) }

def directedgraph_plot(G):
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

def plot(G):
    degree = G.degree()
    freq = frequency(degree.values())
        
    plt.plot(freq.keys(),freq.values())
    plt.xlabel('degree')
    plt.ylabel('frequency')
    plt.show()

def randomGraph(G):
    n = G.number_of_nodes()
    d=  nx.average_degree_connectivity(G)
    c = sum(i[1] for i in d.items())
    p = c/(n-1)
    try: 
        RG = nx.fast_gnp_random_graph(n,p)    
        plot(RG)
        print 'Global Clustering: {0}\t'.format(str(p)),
        l = math.log(RG.number_of_nodes())/math.log(c)
        print 'Average path length : {0}\n'.format(str(l))
    except:
        'Failed attempt to get connected random graph..Try again!!!'



def smallworld(G):
    n = G.number_of_nodes()
    d=  nx.average_degree_connectivity(G)
    c = sum(i[1] for i in d.items())
    c0 = 0.75*(c-2)/(c-1)
    beta = random.uniform(0.01,0.1)
    try:
        SG= nx.connected_watts_strogatz_graph(n,int(c),beta)
        plot(SG)
        c = ((1-beta)**3)*c0
        print 'Global Clustering: {0}\t'.format(str(c)),
        print 'Average path length : {0}\n'.format(str(nx.average_shortest_path_length(SG)))
    except:
        'Failed attempt to get connected small world graph..Try again!!!'


def preferentialAttachment(G):
    n = G.number_of_nodes()
    m =  random.randrange(15,20)
    PG = nx.barabasi_albert_graph(n,m)
    plot(PG)
    l =  math.log(n)/math.log(math.log(n))
    print 'Global Clustering: {0}\t'.format(str(nx.transitivity(PG))),
    print 'Average path length : {0}\n'.format(str(l))


def main(filename):
    G, UG = loadEdgeList(filename)
    print 'Original Graph'
    print '--------------\n'
    directedgraph_plot(G)
    print 'Global Clustering: {0}\t'.format(str(nx.transitivity(G))), 
    print 'Average path length : {0}\n'.format(str(nx.average_shortest_path_length(UG)))
    print '\nRandom Graph Model'
    print '------------------\n'
    randomGraph(G)
    print '\nSmall World Model'
    print '-----------------\n' 
    smallworld(G)
    print '\nPreferential Attachement Model'
    print '------------------------------\n'
    preferentialAttachment(G)


try:
    if(len(sys.argv) != 2):
        print 'Usage \'p4.py filename\''
        sys.exit(-1)
    else:
        main(sys.argv[1])
except:
    print ''

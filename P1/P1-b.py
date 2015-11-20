
import csv
import sys
import random
def anonymize(file,sample):
    edges = []
    nodeDict = {}
    anonymizedEdges = []    

    with open(file,'r') as datafile:
        anonymizedCount = 1
        content = csv.reader(datafile)    
        for row in content:
            node = row[0].strip()
            if not nodeDict.has_key(node):
                nodeDict[node] = anonymizedCount
                anonymizedCount += 1
            if sample=='True': 
                n = len(row)
                if n>1000:
                    n = random.sample(n,1000)
                    x = [row[i] for i in n]
                else:
                    x=row[1:n]             
            else: 
                n = len(row)
                x = row[1:n]
            for i in x:
                edges.append([node,i])                
                if not nodeDict.has_key(i):
                    nodeDict[i] = anonymizedCount
                    anonymizedCount += 1
                anonymizedEdges.append([nodeDict[node],nodeDict[i]])
            if sample=='True':                 
                if len(nodeDict.items())>=3000:
                    break
     
    with open('edges.csv','wb') as edgeFile:
        writer = csv.writer(edgeFile, quoting=csv.QUOTE_ALL)
        writer.writerows(edges)  
    
    with open('anonymizededges.csv','wb') as edgeFile:
        writer = csv.writer(edgeFile, quoting=csv.QUOTE_ALL)
        writer.writerows(anonymizedEdges)     
        
    with open('nodes.csv','wb') as edgeFile:
        writer = csv.writer(edgeFile, quoting=csv.QUOTE_ALL)
        writer.writerows(nodeDict.items())           


try:
    if(len(sys.argv) != 3):
        print 'Usage \'P1-b.py filename True/0\''
        sys.exit(-1)
    else:
        anonymize(sys.argv[1],sys.argv[2])
except:
    print ''
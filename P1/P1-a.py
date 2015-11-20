import requests
from bs4 import BeautifulSoup
import re
import csv
import sys
import json

def findId(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html)

    parentName = re.split('[|-]',soup.title.string)[0].strip()
    title = parentName.encode('ascii','xmlcharrefreplace')

    id = re.search('viewedUser = c.User.set_viewed\({"id":(\d*),',html).group(1)

    followers = soup.find('a',class_='js-profile-followers').find('span').text
    
    return title, id, followers

def scrapSite(url):    
    neighbours = [url]
    nameAndCount = []
    try:
        #currentURL = ''.join([url,'/Followers?_pjax=.center-column+>+.content&page=',str(pageNumber)])
        title, id, followersCount = findId(url.encode('ascii'))
        pageNumber = (int(followersCount)/15)+ (1 if int(followersCount)%15 > 0 else 0)
        for p in range(1,pageNumber+1):
            currentURL = ''.join(['https://asu.academia.edu/v0/profiles/user_relation?subdomain_param=api&id=',id,'&type=followers&page=',str(p)])
            jsontext = requests.get(currentURL).text

            followers = json.loads(jsontext)

            for i in followers:
                neighbours.append(i['url'])
                #if len(neighbours) > 1000:
                #    break
        nameAndCount.append(title)
        nameAndCount.append(followersCount)

    except:
        pageNumber = 1
        neighbours = [url]
        nameAndCount = []
        while True:
            try:
                currentURL = ''.join([url,'/Followers?_pjax=.center-column+>+.content&page=',str(pageNumber)])
                htmlText = requests.get(currentURL).text
                soup = BeautifulSoup(htmlText)

                followers = soup.find_all('div',class_ = 'user_strip')

                if len(followers) == 0: 
                    parentName = re.split('[|-]',soup.title.string)[0].strip()
                    nameAndCount.append(parentName.encode('ascii','xmlcharrefreplace'))   
                    nameAndCount.append(len(neighbours)-1)                     
                    break                                  
                else:          
                    pageNumber +=1
                    for i in followers:
                        neighbours.append(i.find('a', attrs={"data-has-card-for-user": re.compile(u'\d+')})['href'])
                        #if len(neighbours) > 2000:
                        #    break
            except:
                break

    return neighbours,nameAndCount


def BFS(startNode):    

    neighbours=[]
    nodesScraped = []
    counts =[]
    depth = 0
    followers,nameCounts = scrapSite(startNode)
    neighbours.append(followers)
    nodesScraped.append(startNode)
    count = int(nameCounts[1])

    counts.append(nameCounts)

    file = open('output.csv','wb')
    wr =  csv.writer(file)
    wr.writerow(followers)
    
    while True:
        try:
            depth += 1
            flag = False
            for node in neighbours[depth-1]:
                if node not in nodesScraped:
                    followers,nameCounts = scrapSite(node)
                    neighbours.append( followers)
                    nodesScraped.append(node)
                    wr.writerow(followers)   
                    counts.append(nameCounts)             
                    #count += int(nameCounts[1])
                    if len(nodesScraped) > 1000: 
                        flag= True
                        break
            if flag: break
        except:
            continue
    file.close()
    with open('count.csv','wb') as countfile:
        writer = csv.writer(countfile, quoting=csv.QUOTE_ALL)
        writer.writerows(counts)

try:
    if(len(sys.argv) != 2):
        print 'Usage \'P1-a.py filename\''
        sys.exit(-1)
    else:
        BFS(sys.argv[1])
except:
    print ''


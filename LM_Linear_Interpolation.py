import math
from collections import defaultdict
import nltk
from nltk.corpus import brown
import re
from collections import Counter
from nltk.collocations import *
from nltk import sent_tokenize, word_tokenize
RAW_SENTENCES =[]

print("READFILES...")

outData = open("output.txt" , 'w')
wordlist = " "
map_lexicon = {}

class Graph:
  def __init__(self):
    self.nodes = set()
    self.edges = defaultdict(list)
    self.distances = {}

  def add_node(self, value):
    self.nodes.add(value)

  def add_edge(self, from_node, to_node, distance):
    self.edges[from_node].append(to_node)
    self.edges[to_node].append(from_node)
    self.distances[(from_node, to_node)] = distance


def dijsktra(graph, initial):
  visited = {initial: 0}
  path = {}

  nodes = set(graph.nodes)

  while nodes:
    min_node = None
    for node in nodes:
      if node in visited:
        if min_node is None:
          min_node = node
        elif visited[node] < visited[min_node]:
          min_node = node

    if min_node is None:
      break

    nodes.remove(min_node)
    current_weight = visited[min_node]

    for edge in graph.edges[min_node]:
      weight = current_weight + graph.distance[(min_node, edge)]
      if edge not in visited or weight < visited[edge]:
        visited[edge] = weight
        path[edge] = min_node

  return visited, path


def readFile():
    with open("lexiconv5.txt") as f:
        for line in f.readlines():
            map_lexicon[line.replace("\n" , "")] = 1
    print(map_lexicon)


    data = open("VNTQcorpus-small.txt", 'r').read()
    fThree = (data.replace("''", " "))
    fFour = (data.replace("--", " "))
    finalData = (re.sub('[0-9\W]+', " ", fThree))
    return finalData

def cal_C2(wi, wj):
    return wordCounter2[(wj , wi)]

def cal_C1(wi):
    return unigram[(wi)]

def cal_Unigram(wi):
    return cal_C1(wi)  / len(tokens)

def cal_Pml(wi , wj):
    return cal_C2(wi , wj) / cal_C1(wj)

def getLamda():
    r1 = r2 = 0.5
    e = 0.01
    e_ = 0.02
    while ( e_ > e ):
        r1_ = r1
        r2_ = r2
        c1 = c2 = 0.0
        for item in bigram:
            # print(cal_Pml(item[1], item[0]), "||||", cal_Unigram(item[1]))
            c1 = (cal_C2(item[1] , item[0]) * r1 * cal_Pml(item[1] , item[0])) / (r1 * cal_Pml(item[1] , item[0]) + r2 * cal_Unigram(item[1]))
            c2 = (cal_C2(item[1] , item[0]) * r2 * cal_Unigram(item[1])) / (r1 * cal_Pml(item[1] , item[0]) + r2 * cal_Unigram(item[1]))
            r1 = c1 / (c1 + c2)
            r2 = 1 - r1_
            e_ = math.sqrt(math.pow(r1_ - r1 , 2) + math.pow(r2_ - r2 , 2) )
    return r1 , r2

def cal_Bigram(wi,wj):
    return r1 * cal_Pml(wi , wj) + r2 * cal_Unigram(wi)

def AccepteString(s):
    # print(s)
    if (s == 'xông xáo'):
        print('Hleeoo')
        print(map_lexicon[s])

    if (map_lexicon.__contains__(s) == True):
        return True
    return False

def output_Str(s):
    inp_Str = []
    for word in s.split():
        inp_Str.append(word)

    gp = Graph()
    pre = defaultdict(list)
    n = len(inp_Str)
    for i in range(0 , n):
        gp.add_node(i)
    dp = []
    for i in range(0 , n-1):
        s_cat = ''
        for j in range( i , n):
            s_cat = s_cat + inp_Str[j]
            print(s_cat)
            # print(s_cat)
            if (AccepteString(s_cat) == True):
                print(s_cat)
                pre[j].append[i]
            s_cat = s_cat + ' '

    for i in range(2 * n):
        dp.append(0)
    dp[0] = 1
    for i in range (1 , n):
        dp[i] = dp[i-1] + 1
        for j in pre[i]:
            dp[i] = min (dp[i] , dp[j-1] + 1)
    print(dp[n-1])
    return 0

finalData = readFile()
# tokens = word_tokenize(finalData)
# unigram = Counter(finalData.split())
# sent_tokenize_list = sent_tokenize(finalData)
# bigram = list(nltk.bigrams(finalData.split()))
# wordCounter2 = Counter(bigram)
#
# r1,r2 = getLamda()
output_Str("anh xông xáo tấn công")
print("Done")


#A Large-scale Vietnamese News Text Classification Corpus
#https://github.com/magizbox/underthesea/wiki/Vietnamese-NLP-Tools
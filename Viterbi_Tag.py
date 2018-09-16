import nltk
import pandas as pd
import os
from os.path import join
from nltk import sent_tokenize, word_tokenize
import re

ROOT_FOLDER = "brown"

word = []
tag = []
wC1 = {}
tC2 = {}
tC3 = {}
tC1 = {}
trace = {}
S = []
wtC2 = {}
rm = {}
r1 = 0.01
r2 = r3 = r1
Y = []
listNum = ('0','1','2','3','4','5','6','7','8','9')
def readFile():
    for fileName in os.listdir(ROOT_FOLDER):
        # print(fileName)
        with open(join(ROOT_FOLDER, fileName), 'r') as fi:
            for index , line in enumerate(fi):
                for ch in listNum:
                    line = line.replace(ch, "")
                for text in line.split():
                    pos_tag = nltk.tag.str2tuple(text)
                    # print(pos_tag)
                    word.append(pos_tag[0])
                    tag.append(pos_tag[1])

def initWC():
    for idx in range(0, len(word)):
        wC1[word[idx]] = 0
        tC1[tag[idx]] = 0
        wtC2[(word[idx] , tag[idx])] = 0
        if (idx + 1 < len(word)):
            tC2[(tag[idx], tag[idx + 1])] = 0
        if (idx + 2 < len(tag)):
            tC3[(tag[idx], tag[idx + 1], tag[idx + 2])] = 0
        tC2[('START', tag[idx])] = 1
        tC2[('START' , 'START')] = 1
        tC3[('START', 'START', tag[idx])] = 1
        tC1[('STOP')] = 1
        tC1[('START')] = 1
        tC2[(tag[idx], 'STOP')] = 1

    for t1 in tC1:
        for t2 in tC1:
            tC3[(t1 , t2 , 'STOP')] = 1

    for idx in range(0, len(word)):
        wC1[word[idx]] += 1
        tC1[tag[idx]] += 1
        wtC2[(word[idx], tag[idx])] += 1
        if (idx + 1 < len(word)):
            tC2[(tag[idx], tag[idx + 1])] += 1
        if (idx + 2 < len(tag)):
            tC3[(tag[idx], tag[idx + 1], tag[idx + 2])] += 1

    print("init() done.")

    print("Length data = ", len(word))
    print("Unigram ", len(tC1))
    print("Bigram = ", len(tC2))
    print("Trigram = ", len(tC3))
    S.append(['START'])
    S.append(['START'])
    S.append([x for x in tC1])

def calc_1(w):
    # if (w == 'START' or w == 'STOP'):return len(tC1)/len(word)
    return tC1[w] / len(word)

def calc_2(wj, wi):

    if (tC2.__contains__((wj ,wi)) == False):
        return 0
    return tC2[(wj , wi)] / tC1[(wj)]

def calc_3(wj , wi, wk):
    if ( tC3.__contains__((wj ,wi ,wk)) == False):
        return 0

    if ( tC2.__contains__((wj, wi)) == False):
        return 0
    return tC3[(wj , wi , wk)] / tC2[(wj , wi)]

def get_L():
    r2 = 0.31
    r3 = 0.42
    r1 = 1 - r2 - r3
    return r1,r1,r3

def calc_q(D,N,V):
    return r1 * calc_3(D,N,V) + r2 * calc_2(N , V) + r3 * calc_1(V)

def calc_e(w_, t_):
    if ( wtC2.__contains__((w_ , t_)) == False):
        return 0

    return wtC2[w_, t_] / tC1[t_]

def get_Y(inputString):
    resu = resv = 's'
    word = inputString.split()
    n = len(word)
    count_step = n
    k = 1

    for k1 in range(0 , n + 1):
        for i1 in S[2]:
            for i2 in S[2]:
                rm[(k1 , i1 , i2)] = 0

    maxres = -1.000
    rm[(0, 'START', 'START')] = 1

    # k = 1
    for v in tC1:
        rm[(1, 'START' , v)] = rm[(0 , 'START' , 'START')] * calc_q('START' , 'START' , v) * calc_e(word[0] , v)
        # if (v == 'PPSS'):
        #     print(calc_q('START' , 'START' , v) , " + " , calc_e(word[0] , v))
        #     exit(
        trace[(1, 'START', v)] = 'START'

    # k = 2
    for v in tC1:
        for u in tC1:
            rm[(2 , u , v)] = rm[(1 , 'START' , u)] * calc_q('START' , u , v) * calc_e(word[1] , v)
            trace[(2, u, v)] = 'START'
    print("Flag 0")

    for k in range(3 , len(word)+1):
        print(k)
        for uv in tC2:
            u = uv[0]
            v = uv[1]
            maxW = 0.0
            for w in tC1:
                calcW = rm[(k - 1, w, u)] * calc_q(w, u, v) * calc_e(word[k - 1], v)
                if (maxW < calcW):
                    maxW = calcW
                    trace[(k, u, v)] = w
                # if (w == 'PPSS' and u == 'MD' and v == 'VBN'):
                #     print(calcW)
                #     exit()

            rm[(k , u , v)] = maxW

    print("Flag 1")
    maxW = 0.0
    k = n
    for v in tC1:
        for u in tC1:
            if maxW < rm[( k , u , v)]:
                maxW = rm[(k , u , v)]
                resu =u
                resv= v
                print(maxW)

    Y.append(resv)
    Y.append(resu)

    idx = n
    while (True):
        Y.append(trace[(idx,resu , resv)])
        if (idx - 1 == 1): break
        temp = trace[(idx, resu, resv)]
        resv = resu
        resu = temp
        idx -= 1

    print(Y)

get_L()
readFile()
initWC()
get_Y("i want to do")




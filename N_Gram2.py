import os
from os.path import join
import joblib
import nltk
from nltk.corpus import brown

word1 = word2 = word3 = []
cnt1  = cnt2  = cnt3  = {}
nWord = 0

ROOT_FOLDER = "brown"
RAW_SENTENCES =[]

def readFile():
    output = open("outputt.txt", 'w')
    count = 0
    print("READ FILE ... ")
    for fileName in os.listdir(ROOT_FOLDER):
        with open(join(ROOT_FOLDER , fileName),'r') as fi:
            for sent in brown.sents(fileName):  # First 5 sentences.
                #print(' '.join(sent))
                output.write(' '.join(sent))

            count += 1
            print(fileName)
            # if (count == 20): exit()
            print("------------------------")
            for index , line in enumerate(fi):
                print(line)
                line = line.replace("\n","").strip()
                line = line.replace("./.","").strip()
                line = line.replace(",/,","").strip()
                line = line.replace("''/''","").strip()
                line = line.replace("'/'","").strip()
                line = line.replace("/","").strip()
                print(line)
                if line!= '' and len(line) > 0:
                    line = line.lower()
                    tokens = nltk.word_tokenize(line)
                    token  = [item.split('/')[0] for item in tokens if item.split('/')[0]!= '']
                    RAW_SENTENCES.append(token)
                    print(token)
    print("READING TOTAL :{} SENTENCES".format(len(RAW_SENTENCES)))
    joblib.dump(RAW_SENTENCES , 'sentences.n')
    #RAW_SENTENCES = joblib.load('se# ntences.n')

readFile()
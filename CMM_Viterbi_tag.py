
from nltk.classify import MaxentClassifier
import nltk
from nltk.stem.porter import *
from io import open
import os
from os.path import join

word = []
tag = []
wordStartlist = []
labeled_features = []
pos_list = []
ch_list = []
ne_list = []
dic_Potag = {}
list_POS = []

def read_file():
    end_line = 0
    previous_WO = "start"
    previous_PO = "start"
    previous_CH = "start"
    previous_NE = "start"
    train_data = open("eng-ner/eng.train")

    for line in train_data:
        s = re.match(r'^\s*$', line)
        if s:
            previous_WO = "start"
            previous_PO = "start"
            previous_CH = "start"
            previous_NE = "start"
            end_line = 1
        else:
            sentence_list = line.split()
            word = sentence_list[0]
            pos_tag = sentence_list[1]
            ch_tag = sentence_list[2]
            ne_tag = sentence_list[3]

            if end_line == 1:
                wordStartlist.append(word)
                end_line = 0

            pos_list.append(pos_tag)
            ch_list.append(ch_tag)
            ne_list.append(ne_tag)
            item = word, pos_tag, ch_tag, ne_tag, previous_NE, previous_CH, previous_PO

            labeled_features.append(item)
            previous_WO , previous_PO, previous_CH, previous_NE = word, pos_tag, ch_tag, ne_tag
    train_data.close()

def CMM_features(word , previousPo ,  currentCh, currenNe):

    features = {}
    features['cur_word'] = word
    features['cur_chtag'] = currentCh
    features['cur_netag'] = currenNe
    features['cap'] = word[0].isupper()
    features['pre_pos'] = previousPo
    return features

def init():
    for item in labeled_features:
        pos_tag = item[1]
        if ( pos_tag not in dic_Potag):
            dic_Potag[pos_tag] = 1
            list_POS.append(pos_tag)

    print("Init -> Ok")


def CMM_calc(list_word, list_CHtag, list_NEtag):
    word = list_word[0]
    tag  = list_CHtag[0]
    tRange = len(list_POS)
    wRange = len(list_word)

    viterbi = [[0 for x in range(300)] for x in range(300)]
    backpointer = [['' for x in range(300)] for x in range(300)]

    for t in range(tRange):
        probability = maxent_classifier.prob_classify(CMM_features(list_word[0],  "start" , list_CHtag[0], list_NEtag[0]))
        posterior = float(probability.prob(list_POS[t]))
        viterbi[t][0] = posterior
        backpointer[t][0] = -1

    maxviterbi = 0
    for k in range(0 , wRange):
        for t in range(tRange):
            # word = list_word[k]
            # chtag = list_CHtag[k]
            # netag = list_NEtag[k]
            # probability = maxent_classifier.prob_classify(CMM_features(word, list_POS[0], chtag, netag))
            # posterior = float(probability.prob(list_POS[t]))
            # maxviterbi = float(viterbi[0][k]) * posterior
            maxPreviousState = 0
            maxviterbi = 0.0
            for i in range ( tRange):
                word = list_word[k]
                chtag = list_CHtag[k]
                netag = list_NEtag[k]
                probability = maxent_classifier.prob_classify(CMM_features(word, list_POS[i], chtag,netag))
                posterior = float(probability.prob(list_POS[t]))
                if float (viterbi[i][k] * posterior) > maxviterbi:
                    maxviterbi =  float (viterbi[i][k] * posterior)
                    maxPreviousState = i
            viterbi[t][k + 1] = maxviterbi
            backpointer[t][k+1] = maxPreviousState


    maxviterbi = 0.0
    mt = 0.0
    for t in range(tRange):
        if maxviterbi < viterbi[t][wRange]:
            maxviterbi = viterbi[t][wRange]
            mt = t

    # print(list_POS)
    # print(maxviterbi  , mt , list_POS[mt])
    vecto_res = []
    # vecto_res.append(list_POS[backpointer[mt][wRange]])
    vecto_res.append(list_POS[mt])
    k = wRange
    while ( k > 1):
        vecto_res.append(list_POS[backpointer[mt][k]])
        mt = backpointer[mt][k]
        k -= 1

    index = len(vecto_res)
    path = []
    while index >= 1:
        path.append(vecto_res[index - 1])
        index = index - 1
    print("Prediction = " , path)
    return path

read_file()
init()

print("Training data features...")
print(len(labeled_features))
train_set = [ (CMM_features(word , previous_PO , ch_tag, ne_tag) , pos_tag) for (word, pos_tag, ch_tag, ne_tag, previous_NE, previous_CH, previous_PO)
                 in labeled_features]
maxent_classifier = MaxentClassifier.train(train_set, max_iter=3)

#///////////////////////////Test file/////////////////////////////
print("Training finished!!")
print("Start test...")
output_file = open("ner_output.txt", "w")
test_data = open("eng-ner/eng.testa" )
word_list = []
Ptag_list = []
Ctag_list = []
Ntag_list = []
change_of_sentence_flag = 0

sum_pos_tag = 0
correct_pos_tag = 0
for line in test_data:
    if line.strip() != '':
        sentenceList = line.split()
        sentence_list = line.split()
        word = sentence_list[0]
        pos_tag = sentence_list[1]
        ch_tag = sentence_list[2]
        ne_tag = sentence_list[3]

        word_list.append(word)
        Ptag_list.append(pos_tag)
        Ctag_list.append(ch_tag)
        Ntag_list.append(ne_tag)
        if change_of_sentence_flag == 1:
            change_of_sentence_flag = 0

    s = re.match(r'^\s*$', line)
    if s:
        change_of_sentence_flag = 1
        previous_BOI = "start"
        path = CMM_calc(word_list, Ctag_list , Ntag_list )

        # for i in range(len(word_list)):
        #     print(word_list[i] + "	" + Ptag_list[i] + " " + path[i] + "\n")

        for i in range(len(word_list)):
            if (Ptag_list[i] == path[i]):
                correct_pos_tag += 1

        sum_pos_tag += len(word_list)
        print("Current Accuracy = " , correct_pos_tag * 1.0 * 100 / sum_pos_tag, "%")
        word_list = []
        Ptag_list = []
        Ctag_list = []


# proxy_servers:
#     http: http://proxy.cyberspace.vn:3128
#     https: https://proxy.cyberspace.vn:3128
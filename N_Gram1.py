import re
import math
import nltk
import nltk
from nltk.collocations import *
from nltk import sent_tokenize, word_tokenize
from nltk import ngrams
from nltk import FreqDist
import itertools

# this pythonic version is not complete, would love some guidance!

sentenceStart = "<s>"
sentenceEnd = "</S>"

data = open("sdata.txt", 'r').read()
fTwo = (re.sub('[0-9\W]+', " ", data))
fThree = (fTwo.replace("SCENE", " "))
fFour = (fThree.replace("ACT", " "))
finalData = fFour

output = open("outputt.txt" , 'w')


tokens = word_tokenize(finalData)
unigram = Counter(finalData.split())

for item in unigram.items():
    unigramModel = ("{}\t{}".format(*item))
    output.write(str(item))

sent_tokenize_list = sent_tokenize(finalData)
token = sent_tokenize

bigram = list(nltk.bigrams(finalData.split()))
trigram = list(nltk.trigrams((finalData.split())))
print(trigram)
#print(sep=',', *map(' '.join, bigram))
wordCounter = Counter(bigram)

for k, v in wordCounter.items():
     bigramModel = (k, (v/988559))
     #print(bigramModel)


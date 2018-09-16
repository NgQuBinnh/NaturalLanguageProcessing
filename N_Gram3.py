from nltk.collocations import BigramCollocationFinder
import re
import codecs
import numpy as np
import string


def train_language(path):
    words_all = []
    translate_table = dict((ord(char), None) for char in string.punctuation)
    # reading the file in unicode format using codecs library
    with codecs.open(path, "r", "utf-8") as filep:
        for i, line in enumerate(filep):
            line = " ".join(line.split()[1:])
            line = line.lower()  # to lower case
            line = re.sub(r"\d", line)  # remove digits
            if len(line) != 0:
                line = line.translate(translate_table)  # remove punctuations
            print(line)
            words_all += line
            words_all.append(" ")  # append sentences with space

    all_str = ''.join(words_all)
    all_str = re.sub(' +', ' ', all_str)  # replace series of spaces with single space
    seq_all = [i for i in all_str]

    # extracting the bi-grams and sorting them according to their frequencies
    finder = BigramCollocationFinder.from_words(seq_all)
    finder.apply_freq_filter(5)
    bigram_model = finder.ngram_fd.viewitems()
    bigram_model = sorted(finder.ngram_fd.viewitems(), key=lambda item: item[1], reverse=True)

    print(bigram_model)

train_language('brown')
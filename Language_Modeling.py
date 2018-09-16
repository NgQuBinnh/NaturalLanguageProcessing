
word1 = word2 = word3 = []
cnt1  = cnt2  = cnt3  = {}
nWord = 0

ROOT_FOLDER = "brown"
RAW_SENTENCES =[]

print("READFILES...")

data = open("outputt.txt", 'r').read()
fThree = (data.replace("''", " "))
fFour = (data.replace("--" , " "))
finalData = (re.sub('[0-9\W]+', " ", fThree))

tokens = word_tokenize(finalData)

unigram = Counter(finalData.split())
print(finalData)
dd = {}
alpha = {}
sum = {}
sent_tokenize_list = sent_tokenize(finalData)
token = sent_tokenize
bigram = list(nltk.bigrams(finalData.split()))
trigram = list(nltk.trigrams((finalData.split())))
wordCounter2 = Counter(bigram)
wordCounter3 = Counter(trigram)

outData = open("output.txt" , 'w')

print("unigram" , len(unigram))
print("len bigram" ,len(bigram))
print("len word COunter 2" ,len(wordCounter2))
print("len trigram" , len(trigram))
print("len word C3" , len(wordCounter3))
print("len tokens" , len(tokens))

def check_In2(wj):
    ctnA = []
    ctnB = []
    for str1 in unigram:
        if ( wordCounter2[(wj , str1)] >= 1 ):
            ctnA.append(str1)
        else:
            ctnB.append(str1)
    return ctnA , ctnB

def check_In3(wj,wk):
    ctnA = []
    ctnB = []
    for str1 in unigram:
        if ( wordCounter3[(wk , wj , str1)] >= 1):
            ctnA.append(str1)
        else:
            ctnB.append(str1)
    return ctnA , ctnB

def cal_C3(wi , wj , wk):
    return wordCounter3[(wk ,wj , wi)]

def cal_C2(wi, wj):
    return wordCounter2[(wj , wi)]

def cal_C1(wi):
    return unigram[(wi)]

def cal_A1(wi , ctnA):
    sum  = 1.0
    for w in ctnA:
        sum -= (cal_C2(w , wi) - 0.5) / cal_C1(wi)
        # print((cal_C2(w , wi)) , cal_C1(wi))
    return sum

def cal_A2(wj , wk , ctnA):
    sum = 1.0
    for w in ctnA:
        sum -= ( cal_C3(w , wj , wk) - 0.5) / cal_C2(wj, wk)
    return sum

def cal_Unigram(wi):
    return cal_C1(wi)  / len(tokens)

def cal_Bigram(wi,wj):
    # A , B = check_In2(wj)

    if ((wordCounter2[wj , wi] >= 1)):
        return (cal_C2(wi , wj) - 0.5) / cal_C1(wj)
    else:
        # for w in B:
        #     sum += cal_Unigram(w)
        s = sum[wj]
        return alpha[wj] * cal_Unigram(wi) / s

def cal_Trigram(wi,wj,wk):
    A , B = check_In3(wj , wk)

    if (wordCounter3[(wk , wj , wi)] == True):
        return (cal_C3(wi,wj,wk) - 0.5) / cal_C2(wj, wk)
    else:
        sum = 0
        for w in B:
            sum += cal_Bigram(w,wj)
        return cal_A2(wj,wk,A) * cal_Bigram(wi,wj) / sum

listSG = []

def next_Str(wj,wi):
    maxcalc = 0.0
    ww = 's'
    for str1 in unigram:
        calB = cal_Bigram(str1, wi)

        if (maxcalc <= calB):
            maxcalc = calB
            ww = str1
    print(ww)
    next_Str(wi ,ww)

def init():
    for w in unigram:
        sum[w] = 0
        alpha[w] = 0

    for wj , wi in bigram:
        sum[wj] = sum[wj] + cal_C1(wi)
        alpha[wj] = alpha[wj] + cal_C2(wi , wj) / cal_C1(wj)

    for w in unigram:
        sum[w] = (len(tokens) - sum[w] - cal_C1(w)) / len(tokens)
        alpha[w] = 1 - alpha[w]

print(unigram['the'])
wj = "they"
wi = "will"

init()

while (1):
    print('----------')
    maxcalc = 0.0
    ww = 's'
    for wwj , str1 in bigram:
        if (wi == wwj ):
            calB = cal_Trigram(str1,wi,wj)
            if (maxcalc < calB):
                maxcalc = calB
                ww = str1

    print(ww)
    wj = wi
    wi = ww
    exit()
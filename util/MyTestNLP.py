import jieba
import nltk

from util import MyTestFile

from bs4 import BeautifulSoup
import urllib.request
import nltk


def wordWebFreq():
    response = urllib.request.urlopen('http://php.net/')
    html = response.read()
    soup = BeautifulSoup(html, "html5lib")
    text = soup.get_text(strip=True)
    tokens = [t for t in text.split()]
    freq = nltk.FreqDist(tokens)
    for key, val in freq.items():
        print(str(key) + ':' + str(val))

def wordFreq(txt: str):
    tokens = [t for t in jieba.lcut(txt)]
    freq = nltk.FreqDist(tokens)
    for key, val in freq.items():
        print(str(key) + ':' + str(val))

def splitTxt(txt: str):
    res = nltk.sent_tokenize(txt)
    # print(res)
    return res


def splitSentence(txt: str):
    res = nltk.word_tokenize(txt)
    print(res)
    return res


def start():
    txt = MyTestFile.getTxt()
    sens = splitTxt(txt)
    for sen in sens:
        splitSentence(sen)


if __name__ == "__main__":
    # start()
    wordFreq(MyTestFile.getTxt())


# -*- encoding:utf8 -*-
from random import *
from pymongo import MongoClient
import jieba # 结巴分词
import collections


def getArticleFromMongo():
    cli = MongoClient("localhost", 27017)
    db = cli['wechat']
    collection = db['articles']
    allArticlesCursor = collection.find()
    allArticles = []
    for i in allArticlesCursor:
        allArticles.append(i)

    numOfArticles = len(allArticles)
    i = randrange(0, numOfArticles-1)
    return allArticles[i]
    # words = jieba.cut(strip_markup(article))
    # for word in words:
    #     print word

def analysisWordsInArticle():
    pass

def cleanArticle(articleContent=""):
    madeup = []
    a = collections.Counter()
    paragraphs = articleContent.split("\n")
    paragraphs =  list(set(paragraphs))
    if "" in paragraphs:
        paragraphs.remove("")
    for paragraph in paragraphs:
        sentences = paragraph.split(" ")
        sentences =  list(set(sentences))
        if "" in sentences:
            sentences.remove("")
        # print sentences
        # print "\n"
        for sentence in sentences:
            a += collections.Counter(list(jieba.cut(sentence)))
    return a

        # madeup.append(sentences)
    # return madeup

def countWord(words=[]):
    for paragraph in words:
        pass
    pass

print(cleanArticle(getArticleFromMongo()["content"]))

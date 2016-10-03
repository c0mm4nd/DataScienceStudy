#-*- coding:utf8 -*-
import requests
from lxml import etree
from pymongo import MongoClient
from django_html_cleaner import cleaner
from htmllaundry import strip_markup
import jieba
import sys
import HTMLParser

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}

def pullLatestHotArticles():
    ''' 全部文章中 的 热门 '''
    url = "http://werank.cn/"
    urlList = []
    html = requests.get(url).text
    et = etree.HTML(html)
    list = et.xpath("//table/tbody/tr/td[2]/a")
    # print list
    for element in list :
        # print element.attrib["href"]
        urlList.append(element.attrib["href"])
    print "already get all urls"
    return urlList

def pointedWechatOfficialAccountsArticles(wechatOfficialAccountName):
    ''' 指定威信公众号 文章'''
    # url =
    urlList = []
    i = 0
    while i >= 0 :
        url = "http://chuansong.me/account/" + wechatOfficialAccountName + "?start=" + str(i)
        html = requests.get(url, headers=headers).text
        et = etree.HTML(html)
        list = et.xpath("//h2/span/a")
        # print list
        for element in list :
            urlList.append("chuansong.me" + element.attrib["href"])
        if len(list) < 12 :
            break
        i = i + 12
    return urlList


def saveArticlesToMongo(urlList):
    try :
        mongo = MongoClient('localhost', 27017)
        db = mongo.wechat
    except Exception,e:
        print e
        print "Error in connection"
        exit()
    # print urlList
    for url in urlList:
        print "start read article in " + url
        html = requests.get(url, headers=headers).text
        try:
            articleNCR = etree.tostring(etree.HTML(html).xpath("//div[@id='page-content']")[0])
            #
            h = HTMLParser.HTMLParser()      # local encode
            article = h.unescape(strip_markup(articleNCR))
            db.articles.insert({
                "url": url,
                "content": article,
            })
            print "finish insert article in " + url
        except:
            log = open("urlfailed.log","a")
            log.write(url + "\n")
            log.close()
            print "failed on url " + url
        # words = jieba.cut(strip_markup(article))
        # for word in words :
        #     print word
    pass

# saveArticlesToMongo(pullLatestHotArticles())
print pointedWechatOfficialAccountsArticles("xineuro")

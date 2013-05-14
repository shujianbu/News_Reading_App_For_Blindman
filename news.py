# -*- coding: utf-8 -*-

#####################################
## News Searching and Filtering Model
#####################################

from bs4 import BeautifulSoup
import urllib2
import urllib
from cookielib import CookieJar
import re
import requests
import unicodedata
from os import system

storydict = dict()
pressdict = dict()
contentlist = []

# Function for filtering targeted news articles.
def filterNews(query):
    query = query.replace(" ", "+")
    googlenews = 'http://news.google.com/news?q=' + query + "&output=rss"
    googlenewsopen = urllib2.urlopen(googlenews)
    googlenewssoup = BeautifulSoup(googlenewsopen)
    for newsitem in googlenewssoup.findAll('item'):
        title = re.compile('<title>(.*?)</title>').search(str(newsitem.findAll('title')[0])).group(1)
        link = re.compile('cluster=(.*?)</guid>').search(str(newsitem.findAll('guid')[0])).group(1)
        press = re.compile('(.*?) - USA TODAY').search(str(title))
        if press != None:
            storydict[title] = link
            pressdict[title] = "USA TODAY"
        press = re.compile('(.*?) - NBCNews.com').search(str(title))
        if press != None:
            storydict[title] = link
            pressdict[title] = "NBCNews.com"
        press = re.compile('(.*?) - Fox News').search(str(title))
        if press != None:
            storydict[title] = link
            pressdict[title] = "Fox News"
        press = re.compile('(.*?) - Washington Post').search(str(title))
        if press != None:
            storydict[title] = link
            pressdict[title] = "Washington Post"
        press = re.compile('(.*?) - New York Times').search(str(title))
        if press != None:
            storydict[title] = link
            pressdict[title] = "New York Times"
        press = re.compile('(.*?) - Los Angeles Times').search(str(title))
        if press != None:
            storydict[title] = link
            pressdict[title] = "Los Angeles Times"
        press = re.compile('(.*?) - Reuters').search(str(title))
        if press != None:
            storydict[title] = link
            pressdict[title] = "Reuters"

# Function for filtering news article from a particular url.
def getNews(link):
    googlenewsopen = urllib2.urlopen(link)
    googlenewssoup = BeautifulSoup(googlenewsopen)
    for newsitem in googlenewssoup.findAll('item'):
        title = re.compile('<title>(.*?)</title>').search(str(newsitem.findAll('title')[0])).group(1)
        link = re.compile(';url=(.*?)<guid').search(str(newsitem)).group(1)
        press = re.compile('(.*?) - USA TODAY').search(str(title))
        if press != None:
            storydict[title] = link
            pressdict[title] = "USA TODAY"
        press = re.compile('(.*?) - NBCNews.com').search(str(title))
        if press != None:
            storydict[title] = link
            pressdict[title] = "NBCNews.com"
        press = re.compile('(.*?) - Fox News').search(str(title))
        if press != None:
            storydict[title] = link
            pressdict[title] = "Fox News"
        press = re.compile('(.*?) - Washington Post').search(str(title))
        if press != None:
            storydict[title] = link
            pressdict[title] = "Washington Post"
        press = re.compile('(.*?) - New York Times').search(str(title))
        if press != None:
            storydict[title] = link
            pressdict[title] = "New York Times"
        press = re.compile('(.*?) - Los Angeles Times').search(str(title))
        if press != None:
            storydict[title] = link
            pressdict[title] = "Los Angeles Times"
        press = re.compile('(.*?) - Reuters').search(str(title))
        if press != None:
            storydict[title] = link
            pressdict[title] = "Reuters"

# Function for removing all punctuations except (! . ? - ; ;).
def remove_punctuation(text):
    return re.sub(r'((?!,)(?!\.)(?!\?)(?!;)(?!:))[^\w]', " ",text)

# Funtion for encoding the article content.
def encoding(text):
    print content.encode("utf-8")

# Function filters news article from USATODAY.
def readUSATODAY(urllink):
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    p = opener.open(urllink)
    urlsoup = BeautifulSoup(p.read())
    content = ""
    for item in urlsoup.findAll('p', {'class': None, 'style': None}):
        for subitem in item.findAll(text = True):
            if subitem != "Close" and subitem != "\n":
                content = content + subitem
    return content

# Function filters news article from FOXNEWS.
def readFOXNEWS(urllink):
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    p = opener.open(urllink)
    urlsoup = BeautifulSoup(p.read())
    content = ""
    for article in urlsoup.findAll('article', {'class': 'article-text'}):
        for articleitem in article.findAll('p', {'class': None, 'style': None}):
            for item in articleitem.findAll(text = True):
                if item != "\n" and item != ".":
                    content = content + item
    return content

# Function filters news article from NBCNEWS.
def readNBCNEWS(urllink):
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    p = opener.open(urllink)
    urlsoup = BeautifulSoup(p.read())
    content = ""
    for item in urlsoup.findAll('p', {'class': None, 'style': None}):
        for subitem in item.findAll(text = True):
            if subitem != "\n":
                content = content + subitem
    return content

# Function filters news article from WASHINTONPOST.
def readWashingtonPost(urllink):
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    p = opener.open(urllink)
    urlsoup = BeautifulSoup(p.read())
    content = ""
    for article in urlsoup.findAll('article'):
        for articleitem in article.findAll('p', {'class': None, 'style': None}):
            for item in articleitem.findAll(text = True):
                if item != "\n":
                    content = content + item
    return content

# Function filters news article from NYTIMES.
def readNYTIMES(urllink):
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    p = opener.open(urllink)
    urlsoup = BeautifulSoup(p.read())
    content = ""
    for article in urlsoup.findAll('div', {'class': 'articleBody'}):
        for articleitem in article.findAll('p', {'itemprop': 'articleBody'}):
            for item in articleitem.findAll(text = True):
                if item != "\n":
                    content = content + item
    return content

# Function filters news article from LATIMES.
def readLATIMES(urllink):
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    p = opener.open(urllink)
    urlsoup = BeautifulSoup(p.read())
    content = ""
    for article in urlsoup.findAll('div', {'id': 'story-body-text'}):
        for articleitem in article.findAll('p'):
            for item in articleitem.findAll(text = True):
                content = content + item
    return content

# Function filters news article from REUTERS.
def readReuters(urllink):
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    p = opener.open(urllink)
    urlsoup = BeautifulSoup(p.read())
    content = ""
    for article in urlsoup.findAll('span', {'class': None, 'modulename': None}):
        for story in article.findAll('p'):
            for item in story.findAll(text = True):
                content = content + item
    return content

# Function manages news articles from various sources and get content.
def readStory(storyname):
    s = requests.Session()
    if str(s.get(storydict[storyname])) == "<Response [200]>":
        if pressdict[storyname] == "USA TODAY":
            newscontent = readUSATODAY(storydict[storyname])
        elif pressdict[storyname] == "NBCNews.com":
            newscontent = readNBCNEWS(storydict[storyname])
        elif pressdict[storyname] == "Fox News":
            newscontent = readFOXNEWS(storydict[storyname])
        elif pressdict[storyname] == "Washington Post":
            newscontent = readWashingtonPost(storydict[storyname])
        elif pressdict[storyname] == "New York Times":
            newscontent = readNYTIMES(storydict[storyname])
        elif pressdict[storyname] == "Los Angeles Times":
            newscontent = readLATIMES(storydict[storyname])
        elif pressdict[storyname] == "Reuters":
            newscontent = readReuters(storydict[storyname])
        templist = []
        templist.append(storyname)
        templist.append(newscontent)
        contentlist.append(templist)

# Function returns international news content.
def readInternationalNews():
    getNews('https://news.google.com/news/section?cf=all&ned=us&topic=w&output=rss')
    print "------------List of International News------------"
    for story in storydict.keys():
        print story
        print ""
        readStory(story)
    reading_content = ""
    for item in contentlist:
        reading_content = reading_content + "Now reading article: " + item[0] + ". " + item[1]
    return remove_punctuation(reading_content.replace('.','. '))

# Function returns national news content.
def readNationalNews():
    getNews('https://news.google.com/news/section?cf=all&ned=us&topic=n&output=rss')
    print "--------------List of National News--------------"
    for story in storydict.keys():
        print story
        print ""
        readStory(story)
    reading_content = ""
    for item in contentlist:
        reading_content = reading_content + "Now reading article: " + item[0] + ". " + item[1]
    return remove_punctuation(reading_content.replace('.','. '))
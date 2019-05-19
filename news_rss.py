#!/opt/app-root/bin/python
#-*- coding: UTF-8 -*-

import time
import argparse
import feedparser
from httplib2 import Http
from json import dumps

# Google chat room URL, need token from args
chatRoomUrl="https://chat.googleapis.com/v1/spaces/AAAAPwc3WLo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token="

# rss URL
rssList=[
        'http://feeds.japan.zdnet.com/rss/zdnet/all.rdf',
        'https://news.yahoo.co.jp/pickup/computer/rss.xml',
        'https://rss.itmedia.co.jp/rss/2.0/news_bursts.xml',
        'https://rss.itmedia.co.jp/rss/2.0/ait.xml',
        'https://tech.nikkeibp.co.jp/rss/index.rdf',
        'https://jp.techcrunch.com/feed/',
        'http://feeds.japan.cnet.com/rss/cnet/all.rdf',
        'https://weekly.ascii.jp/cate/1/rss.xml',
        ]

# Keywork List
keywordList=[
        'Canonical',
        'Ubuntu',
        'Linux',
        'OpenStack',
        'Kubernetes',
        'Redhat',
        'Red hat',
        'レッドハット',
        'Microsoft',
        'マイクロソフト',
        'Yahoo!Japan',
        '買収',
        '日立製作所',
        ]

sentLinks='/tmp/sentLinks'

# Hangouts Chat incoming webhook
def sendChat(chatRoom, chatContent):
    bot_message = { 'text' :  chatContent}

    message_headers = { 'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    response = http_obj.request(
        uri=chatRoom,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )

def rssBot(rssLink):

    # open and read file which contains already sent link
    try:
        with open(sentLinks) as f:
            sentLinkList = f.read().splitlines()
    except IOError:
        sentLinkList = []

    # get rss data and parse to d
    d=feedparser.parse(rssLink)

    for entry in d.entries:
        # haven't been sent before
        if entry.link not in sentLinkList:

            for keyword in keywordList:
                if keyword in entry.title:
                    #print(entry.title + ' ' + entry.link)
                    sendChat(chatRoomUrl + token, entry.title + ' ' + entry.link)

                    f = open(sentLinks, 'a+')
                    f.write(entry.link + '\n')
                    f.close()
                    break
            

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('token', type=str, help='token of Google chat room')
    token=parser.parse_args().token

    for rssLink in rssList:
        rssBot(rssLink)


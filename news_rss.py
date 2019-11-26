#!/opt/app-root/bin/python
# -*- coding: UTF-8 -*-

import argparse
import feedparser
from httplib2 import Http
from json import dumps

# Google chat room URL, need token from args
chatRoomUrl = "https://chat.googleapis.com/v1/spaces/AAAAPwc3WLo/messages" \
              "?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token="

# rss URL
rssList = [
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
keywordList = [
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
    'ヤフー',
    '買収',
    '日立製作所',
    'VMware',
    'IBM',
    'SUSE',
    # 'クラウド',
    # 'cloud',
    'Dell',
    'nuc'
    'Intel'
]

sentLinks = '/tmp/sentLinks'
sentTitles = '/tmp/sentTitles'


# Hangouts Chat incoming webhook
def sendChat(chatRoom, chatContent):
    bot_message = {'text':  chatContent}

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    http_obj.request(
        uri=chatRoom,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )


def readFile(sentFile):
    try:
        with open(sentFile) as f:
            sentList = f.read().splitlines()
    except IOError:
        sentList = []

    return sentList


def writeFile(writeFile, data):
    f = open(writeFile, 'a+')
    f.write(data + '\n')
    f.close()


def rssBot(rssLink):

    # open and read file which contains already sent link and title
    # return a list
    sentLinkList = readFile(sentLinks)
    sentTitleList = readFile(sentTitles)

    # get rss data and parse to d
    d = feedparser.parse(rssLink)

    for entry in d.entries:
        # haven't been sent before
        if entry.link not in sentLinkList and entry.title not in sentTitleList:

            # keyword is in the title
            for keyword in keywordList:
                if keyword in entry.title:
                    sendChat(chatRoomUrl + token,
                             entry.title + ' ' + entry.link)

                    # save sent link and title to file
                    writeFile(sentLinks, entry.link)
                    writeFile(sentTitles, entry.title)
                    break


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('token', type=str, help='token of Google chat room')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    token = args.token

    sentLinkList = readFile(sentLinks)
    if args.debug:
        sendChat(chatRoomUrl + token,
                 'DEBUG: sentLinkList\n' + '\n'.join(sentLinkList))

    for rssLink in rssList:
        rssBot(rssLink)

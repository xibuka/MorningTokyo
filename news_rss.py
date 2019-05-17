#!/opt/app-root/bin/python
#-*- coding: UTF-8 -*-

import time
import argparse
import feedparser
from httplib2 import Http
from json import dumps

# User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}]

# Google chat room URL, need token from args
chatRoomUrl="https://chat.googleapis.com/v1/spaces/AAAAPwc3WLo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token="

# rss URL
rssUrl='http://feeds.japan.zdnet.com/rss/zdnet/all.rdf'

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


def str2time(s):
    return(time.strptime(s, '%Y-%m-%d %H:%M:%S'))

def time2str(t):
    return(time.strftime('%Y-%m-%d %H:%M:%S', t))

def rssBot():

    # get last updated time
    try:
        f = open('lastUpdateTime_rss', 'r')
        preUpdateTime = str2time(f.read())
        f.close()
    # set last updated time if file not exists
    except IOError:
        preUpdateTime = str2time('2019-01-01 00:00:00')

    # get rss data and parse to d
    d=feedparser.parse(rssUrl)

    for entry in d.entries:
        if time.mktime(entry.updated_parsed) > time.mktime(preUpdateTime):
            print(token)
            sendChat(chatRoomUrl + token, entry.title + ' ' + entry.link)
        else:
            break
            
    f = open('lastUpdateTime_rss', 'w')
    f.write(time2str(d.feed.updated_parsed))
    f.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('token', type=str, help='token of Google chat room')
    token=parser.parse_args().token

    rssBot()

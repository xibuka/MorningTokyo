#!/opt/app-root/bin/python
#-*- coding: UTF-8 -*-

#import sys
#import os
import time
import requests
import argparse
from bs4 import BeautifulSoup
from httplib2 import Http
from json import dumps

# User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}]

# Google chat room URL, need token from args
chatRoomUrl="https://chat.googleapis.com/v1/spaces/AAAAPwc3WLo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token="

# Greeting 
greeting="おはようございます！本日東京の天気とITニュースです。\n\n"

# weather URL 
weatherUrl='https://weather.yahoo.co.jp/weather/jp/13/4410.html' # Tokyo

# news URL    
newsUrl='https://news.yahoo.co.jp/categories/it'

# Hangouts Chat incoming webhook
def sendChat(chatRoom, chatContent):
    print(chatRoom)
    bot_message = {
        'text' :  greeting + chatContent}

    message_headers = { 'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    response = http_obj.request(
        uri=chatRoom,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )

    #print(response)

def requestSoup(url):
    try:
         html = requests.get(url, headers=hds[0], allow_redirects=False, timeout=3)

         #print (html.status_code)
         if html.status_code == 200:
             return BeautifulSoup(html.text.encode(html.encoding), "html.parser")

         else:
             return ''

    except Exception as e:
        print(url, e, str(time.ctime()))
        return ''

def weatherBot():

    weatherSoup=requestSoup(weatherUrl)

    date=weatherSoup.find('p', {'class': 'date'}).text
    weather=weatherSoup.find('p', {'class': 'pict'}).text
    temp=weatherSoup.find('ul', {'class': 'temp'}).text

    return(date + weather + temp)

def newsBot():

    newsSoup=requestSoup(newsUrl)
   
    newsBody=''
    topicsList = newsSoup.find('ul', {'class': 'topicsList_main'})
    for topic in topicsList.find_all('a'):
        title=topic.text
        link=topic['href']
        newsBody = newsBody + title + ' ' + link + '\n'

    return(newsBody)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('token', type=str, help='token of Google chat room')
    token=parser.parse_args().token

    news = newsBot()
    weather = weatherBot()
    sendChat(chatRoomUrl + token, weather + '\n' + news)

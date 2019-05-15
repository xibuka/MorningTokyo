#!/opt/app-root/bin/python
#-*- coding: UTF-8 -*-

import argparse
from httplib2 import Http
from json import dumps

# User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}]

# Google chat room URL, need token from args
chatRoomUrl="https://chat.googleapis.com/v1/spaces/AAAAPwc3WLo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=" # Test env

# Hangouts Chat incoming webhook
def sendChat(chatRoom, chatContent):
    print(chatRoom)
    bot_message = {
        'text' :  chatContent}

    message_headers = { 'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    response = http_obj.request(
        uri=chatRoom,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )

    #print(response)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('token', type=str, help='token of Google chat room')
    parser.add_argument('text', type=str, help='chat contents')
    token=parser.parse_args().token
    text=parser.parse_args().text

    sendChat(chatRoomUrl + token, text)

from __future__ import unicode_literals
from flask import Flask, request, abort
# from linebot import LineBotApi, WebhookHandler
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
import logging
import jieba
import pandas as pd

import random
import os
import json

# 旅遊地點的資料集
place1 = ['日月潭水社遊客中心','23.8666722,120.9112069']
place2 = ['九份老街','25.1098743,121.842994']
place3 = ['墾丁大街','21.9459605,120.7945187']
place4 = ['太魯閣遊客中心','24.1580813,121.620049']
place5 = ['阿里山旅客服務中心','23.5113938,120.8014224']
place6 = ['野柳地質公園','25.2096467,121.6883887']
place7 = ['淡水老街','25.1707561,121.4186507']
place8 = ['國立故宮博物院','25.1023602,121.5463038']
place9 = ['安平古堡','23.0015142,120.1584357']
place10 = ['平溪老街','25.0253135,121.7366306']
# googleAPI的key
gtoken = 'AIzaSyCWzBkM4jnBcvnNqCbRg4AqmLzMyREZRk4'
# 定義旅遊地點的list
travel_place = []

def call_views(messages):
    # 匯入模型權重(行為)資料(tf-idf)
    df = pd.read_csv(r'Dataset/df_csv.csv')

    # jieba斷詞 user說的話
    jieba.load_userdict('Dataset/dict.txt')
    a = jieba.lcut(messages)

    # 迴圈搜尋行為與哪一個景點有關聯性
    for i in range(len(df)):
        
        # 如果權重(行為)資料與user輸入的話，沒有mapping到，就換下一個權重(行為)
        if (df.weight[i] not in a):
            continue
        
        # 如果有mapping到，就將景點顯示出來，若有兩個(含)以上的景點，就隨機給一個景點
        else:
            views_name = df[df['weight']==df.weight[i]]['views_name'].values
            c = random.randrange(0, len(views_name), 1)
            place = views_name[c]
    return place

def days(messages):
    cut_days = jieba.lcut(messages)
    l1 = ['一天', '1']
    l2 = ['二天', '兩天', '2']
    l3 = ['三天', '3']
    l4 = ['四天','4']
    for word in cut_days:
        if word in l1:
            day = 1
        elif word in l2:
            day = 2
        elif word in l3:
            day = 3
        elif word in l4:
            day = 4
    return day

def call_url(pl):
    response = requests.post(
            url='https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+pl+'&radius=15000&keyword=attractions&language=zh-TW&key='+gtoken+''
        )
    for name in response.json()['results']:
        url = name.get('name')
        travel_place.append(url)

def get_travel(place):
    if place in place1:
        pl = place1[1]
    elif place in place2:
        pl = place2[1]
    elif place in place3:
        pl = place3[1]
    elif place in place4:
        pl = place4[1]
    elif place in place5:
        pl = place5[1]
    elif place in place6:
        pl = place6[1]
    elif place in place7:
        pl = place7[1]
    elif place in place8:
        pl = place8[1]
    elif place in place9:
        pl = place9[1]
    elif place in place10:
        pl = place10[1]
    return pl

def plan_travel(day):
    travel_day = day*2
    googlemap_url = 'https://www.google.com.tw/maps/dir/'
    for i in range(travel_day):
        googlemap_url += str(travel_place[i])+'/' 
    # print(googlemap_url)
    return googlemap_url
    
messages = '我想去放天燈玩兩天'

def travel_message(event):
    #定義linebot傳過來的字串為變數
    # messages = event.message.text
    # 開始進行自動規劃
    place = call_views(messages)
    get_travel(place)
    pl = get_travel(place)
    call_url(pl)
    day = days(messages)
    plan_travel(day)
    googlemap_url = plan_travel(day)
    recommend = '推薦景點:'
    for i in range(day*2):
        recommend += str(travel_place[i])+'/'
    answer = recommend, googlemap_url
    print(answer)

    
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=answer)
    # )
    
# if __name__ == '__main__':
#     travel_message(messages)
travel_message(messages)
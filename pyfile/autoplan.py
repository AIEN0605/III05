import sys 
import json

import requests


# result = {
#     'place'': sys.argv[1],
#     'day': sys.argv[2]
#   }


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
token = 'AIzaSyCWzBkM4jnBcvnNqCbRg4AqmLzMyREZRk4'

# node.js傳進來的地點、天數
place = '日月潭水社遊客中心'
day = 4


travel_place = []

def call_url(pl):
    response = requests.post(
            url='https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+pl+'&radius=15000&keyword=attractions&language=zh-TW&key='+token+''
        )
    for name in response.json()['results']:
        url = name.get('name')
        travel_place.append(url)
    plan_travel()


def get_travel():
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
    else:
        return
    call_url(pl)

def plan_travel():
    travel_day = day*2
    googlemap_url = 'https://www.google.com.tw/maps/dir/'
    for i in range(travel_day):
        googlemap_url += str(travel_place[i])+'/' 
    # print(googlemap_url)
    return googlemap_url
    

def posttonodejs():
    # travel_day = day*2
    recommend = '推薦景點:'
    for i in range(day*2):
        recommend += str(travel_place[i])+'/'
    print(recommend)
    print(plan_travel())




if __name__ == '__main__':
    get_travel()
    posttonodejs()
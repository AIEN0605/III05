# 引用 sys 與 json 套件並使用
import sys 
import json
import jieba
import pandas as pd
import random
import requests

#--------------------------#
# 建function-行為預測景點  #
#--------------------------#
def call_views(action):
    # 匯入模型權重(行為)資料(tf-idf)
    df = pd.read_csv(r'C:/AIEN06/Project/Dataset/df_csv.csv')

    # jieba斷詞 user說的話
    jieba.load_userdict('Dataset/dict.txt')
    a = jieba.lcut(action)

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

            
#--------------------------#
# 建function-天數          #
#--------------------------#
def call_days(days):
    cut_days = jieba.lcut(days)
    l1 = ['一天', '1']
    l2 = ['二天', '兩天', '2']
    l3 = ['三天', '3']
    l4 = ['四天','4']
    l5 = ['五','五天','5']
    l6 = ['六','六天','6']
    l7 = ['七','七天','7']
    l8 = ['八','八天','8']
    l9 = ['九','九天','9']    
    for word in cut_days:
        if word in l1:
            day = 1
        elif word in l2:
            day = 2
        elif word in l3:
            day = 3
        elif word in l4:
            day = 4
        elif word in l5:
            day = 5
        elif word in l6:
            day = 6
        elif word in l7:
            day = 7
        elif word in l8:
            day = 8
        elif word in l9:
            day = 9
        else:
            day = 1
    return day


#--------------------------#
# 旅遊地點的資料集         #
#--------------------------#
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

#--------------------------#
# googleAPI的key           #
#--------------------------#
gtoken = 'AIzaSyCWzBkM4jnBcvnNqCbRg4AqmLzMyREZRk4'

#--------------------------#
# 定義旅遊地點的list       #
#--------------------------#
travel_place = []

#----------------------------#
# 確認旅遊點在哪一個資料集   #
#----------------------------#
def get_travel(place):
    if place in place1:
        pl = place1
    elif place in place2:
        pl = place2
    elif place in place3:
        pl = place3
    elif place in place4:
        pl = place4
    elif place in place5:
        pl = place5
    elif place in place6:
        pl = place6
    elif place in place7:
        pl = place7
    elif place in place8:
        pl = place8
    elif place in place9:
        pl = place9
    elif place in place10:
        pl = place10
    return pl

#---------------------------------------------------------#
# 把旅遊地點放進API並把回傳的JSON抓出景點名稱放進LIST     #
#---------------------------------------------------------#
def call_url(idx):
    response = requests.post(
            url='https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+idx+'&radius=5000&keyword=attractions&language=zh-TW&key='+gtoken+''
        )
    for name in response.json()['results']:
        url = name.get('name')
        if url in travel_place:
            continue
        else:
            travel_place.append(url)


#--------------------------------------------------#
# 使用者輸入的天數*2 = 規劃景點數(最高上限10天)    #
#--------------------------------------------------#
def plan_travel(day):
    travel_day = day*2
    googlemap_url = 'https://www.google.com.tw/maps/dir/'
    for i in range(travel_day):
        googlemap_url += str(travel_place[i])+'/' 
    # print(googlemap_url)
    return googlemap_url

#---------------------------------------------------#
# 將 Query String 的 name 與 from 包成 result 物件  #
#---------------------------------------------------#
action = sys.argv[1]
if action=='':
    place =''
    day=''
    recommend=''
    url=''
else:
# action = '我要去逛老街1天'
# action = '我想去一天'
    travel_place.clear()
    place = call_views(action)
    day = call_days(action)
    pl = get_travel(place)
    travel_place.append(pl[0])
    idx = pl[1]
    call_url(idx)
    url = plan_travel(day).replace(" ", "")
    recommend = ''
    for i in range(day*2):
            recommend += str(travel_place[i])+'/'

result = {
    'views':place,
    'day':day,
    'recommend':recommend,
    'url':url,
    'gtoken':gtoken
  }
# print(result)
# 轉成資料為字串
json = json.dumps(result)

# 將結果回傳給 Node.js 程式
print(str(json))
sys.stdout.flush()
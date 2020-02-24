# 引用 sys 與 json 套件並使用
import sys 
import json
import jieba
import pandas as pd
import random

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


#---------------------------------------------------#
# 將 Query String 的 name 與 from 包成 result 物件  #
#---------------------------------------------------#
action = sys.argv[1]

# action = '我要去逛老街,我想去一天'
# action = '我想去一天'
view = call_views(action)
day = call_days(action)




result = {
    'views':view,
    'day':day
  }
# print(result)
# 轉成資料為字串
json = json.dumps(result)

# 將結果回傳給 Node.js 程式
print(str(json))
sys.stdout.flush()
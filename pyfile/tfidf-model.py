# 載入套件
import jieba
from gensim import corpora,models,similarities
from collections import defaultdict
import re

#--------------------------------
# 日月潭 九份 墾丁 太魯閣 阿里山 野柳 淡水 故宮 安平古堡 平溪
#--------------------------------
b1 = open("C:/AIEN06/Project/Dataset/dataset/b1.txt" , 'r', encoding='utf-8').read()
b2 = open("C:/AIEN06/Project/Dataset/dataset/b2.txt" , 'r', encoding='utf-8').read()
b3 = open("C:/AIEN06/Project/Dataset/dataset/b3.txt" , 'r', encoding='utf-8').read()
b4 = open("C:/AIEN06/Project/Dataset/dataset/b4.txt" , 'r', encoding='utf-8').read()
b5 = open("C:/AIEN06/Project/Dataset/dataset/b5.txt" , 'r', encoding='utf-8').read()
b6 = open("C:/AIEN06/Project/Dataset/dataset/b6.txt" , 'r', encoding='utf-8').read()
b7 = open("C:/AIEN06/Project/Dataset/dataset/b7.txt" , 'r', encoding='utf-8').read()
b8 = open("C:/AIEN06/Project/Dataset/dataset/b8.txt" , 'r', encoding='utf-8').read()
b9 = open("C:/AIEN06/Project/Dataset/dataset/b9.txt" , 'r', encoding='utf-8').read()
b10 = open("C:/AIEN06/Project/Dataset/dataset/b10.txt" , 'r', encoding='utf-8').read()

#--------------------------------
# 用正規表達式移除英文、數字與表點符號
#--------------------------------
pat = r"[^\u4e00-\u9fa5]"
b1 = re.sub(pat, '', b1)
b2 = re.sub(pat, '', b2)
b3 = re.sub(pat, '', b3)
b4 = re.sub(pat, '', b4)
b5 = re.sub(pat, '', b5)
b6 = re.sub(pat, '', b6)
b7 = re.sub(pat, '', b7)
b8 = re.sub(pat, '', b8)
b9 = re.sub(pat, '', b9)
b10 = re.sub(pat, '', b10)

#--------------------------------
# 載入自定義詞庫 jieba.load_userdict(file_path)
#--------------------------------
jieba.load_userdict('Dataset/dict.txt')

data1 = jieba.cut(b1)
data2 = jieba.cut(b2)
data3 = jieba.cut(b3)
data4 = jieba.cut(b4)
data5 = jieba.cut(b5)
data6 = jieba.cut(b6)
data7 = jieba.cut(b7)
data8 = jieba.cut(b8)
data9 = jieba.cut(b9)
data10 = jieba.cut(b10)

#--------------------------------
# 讀入停用詞檔
#--------------------------------
with open('Dataset\stopWords.txt', 'r', encoding='UTF-8') as file:
    stopWords=[]
    for data in file.readlines():
        data = data.strip()
        stopWords.append(data)

#------------------------------
# 移除停用詞及跳行符號
#------------------------------
#data1
remainderWords1 = list(filter(lambda a: a not in stopWords and a != '\n', data1))
data1 = ' '.join(remainderWords1)
#data2
remainderWords2 = list(filter(lambda a: a not in stopWords and a != '\n', data2))
data2 = ' '.join(remainderWords2)
#data3
remainderWords3 = list(filter(lambda a: a not in stopWords and a != '\n', data3))
data3 = ' '.join(remainderWords3)
#data4
remainderWords4 = list(filter(lambda a: a not in stopWords and a != '\n', data4))
data4 = ' '.join(remainderWords4)
#data3
remainderWords5 = list(filter(lambda a: a not in stopWords and a != '\n', data5))
data5 = ' '.join(remainderWords5)
#data5
remainderWords6 = list(filter(lambda a: a not in stopWords and a != '\n', data6))
data6 = ' '.join(remainderWords6)
#data7
remainderWords7 = list(filter(lambda a: a not in stopWords and a != '\n', data7))
data7 = ' '.join(remainderWords7)
#data8
remainderWords8 = list(filter(lambda a: a not in stopWords and a != '\n', data8))
data8 = ' '.join(remainderWords8)
#data9
remainderWords9 = list(filter(lambda a: a not in stopWords and a != '\n', data9))
data9 = ' '.join(remainderWords9)
#data10
remainderWords10 = list(filter(lambda a: a not in stopWords and a != '\n', data10))
data10 = ' '.join(remainderWords10)

#------------------------------
# 合併文章
#------------------------------
docs = [data1,data2,data3,data4,data5,data6,data7,data8,data9,data10]

texts=[[word for word in document.split()] for document in docs]
print(type(texts))

#------------------------------
# 使用sklearn工具計算文本tf-idf值
#------------------------------
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

vectorizer = CountVectorizer()

X = vectorizer.fit_transform(docs)

word = vectorizer.get_feature_names()
# print(word)

# print(X.toarray())

transformer = TfidfTransformer()
tfidf = transformer.fit_transform(X)
tfidf_weight = tfidf.toarray() 
# print(tfidf_weight)


#------------------------------
# 將每篇文章權重大於0.08的字詞與其相對應的文章名稱列出來
#------------------------------

views = []
views_name = []
weight = []
view_name_index = ['日月潭水社遊客中心','九份老街','墾丁大街','太魯閣遊客中心','阿里山旅客服務中心','野柳地質公園','淡水老街','國立故宮博物院','安平古堡','平溪老街']


for i in range(len(tfidf_weight)):
    print("-------output {}-th document tf-idf weight------".format(i))
    for j in range(len(word)):
        if tfidf_weight[i][j] >=0.08:
            views.append(i)
            weight.append(word[j])
            views_name.append(view_name_index[i])
            print(word[j],tfidf_weight[i][j])

#------------------------------
# 將每篇文章權重大於0.08的字詞與其相對應的文章名稱列出來
#------------------------------
import pandas as pd

df = pd.DataFrame({"views":views,"views_name":views_name,"weight":weight})

a = '我想去峽谷'
a = jieba.cut(a)

for word in a:
#     print(word+'/', end='')
#     if [df.weight== word]['views_name'].values :
    print(df[df.weight== word ])
    print(word,'/',df[df.weight== word]['views_name'].values)


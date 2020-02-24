import time

import chardet
import requests

def getYahooNewsPage(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f'status is not 200 ({response.status_code})')
        return
    det = chardet.detect(response.content)
    print(response.content.decode(det['encoding']))
    with open('Dataset/b11.html', 'wb') as f:
        f.write(response.content)

if __name__ == '__main__':
    getYahooNewsPage('https://24h.pchome.com.tw/prod/DECL4V-1900AAPNV?fq=/S/DECL4V')
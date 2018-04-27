import requests
from bs4 import BeautifulSoup
import os
import re

file = open('E:/wechat_3.5.txt', 'r').readlines()
url_all = [item.strip('\n') for item in file]

headers = {
    
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'If-Modified-Since': 'Wed, 30 **********',
    'If-None-Match': '"59*******"',
    'Cache-Control': 'max-age=0',
}
fail_case = open('E:/fail_case.txt', 'a')

def get_text():
    count = 0
    for url in url_all:
        if url == '':
            continue
        response = requests.get(url,headers=headers)
        if response.status_code != 200:
            fail_case.writelines(url + '\n')
            continue
        text = BeautifulSoup(response.text, "lxml")
        title = text.find('h2', {'id': "activity-name"}).text.strip()
        print(title)
        file = open('E:/'+title+'.txt', 'w', encoding='utf-8')
        for item in text.find_all('p'):
            file.writelines("{}\n".format(item.text))
        file.close()
        count += 1
        
if __name__ == "__main__":
    get_text()

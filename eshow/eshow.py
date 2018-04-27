import requests
import os
from bs4 import BeautifulSoup

headers = {
    #'Host': 'www.qichacha.com',
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'If-Modified-Since': 'Wed, 30 **********',
    'If-None-Match': '"59*******"',
    'Cache-Control': 'max-age=0',
}


def get_eshow(url):
    path = 'E:/eshow'
    base_url = "http://www.eshow365.com"
    if not os.path.exists(path):
        os.makedirs(path)

    response = requests.get(url, headers=headers)

    text = BeautifulSoup(response.text, "lxml")
    for item in text.find_all('p', {'class': "zhtitle"})[1:]:
        # 访问新链接
        url_new = base_url + item.find('a').get('href')
        print("url_new", url_new)
        response_new = requests.get(url_new, headers=headers)
        text_new = BeautifulSoup(response_new.content, "lxml", from_encoding="uft8")

        # 文章
        title = text_new.find('h1').text.strip()
        path_new = path + '/' + title
        file = open(path_new + ".txt", "w",encoding='utf-8')
        file.writelines(title + "\n")
        print(title)
        
        # 表格
        table = text_new.find('div', {'class': 'zhxxcontent'})
        for cell in table.find_all('p'):
            file.writelines("{}\n".format(cell.text.strip()))

        # 展会概况
        zhgk = text_new.find_all('div', {'class': 'zhgk'})
        for cell in zhgk:
            head = cell.find('h4')
            file.writelines(head.text.strip() + "\n")
            for div in cell.find_all('div'):
                if div is None:
                    continue
                file.writelines(div.text.strip() + "\n")                
        file.close()

#每次只需修改get_eshow中的链接就可爬取新的展会信息
get_eshow('http://www.eshow365.com/zhanhui/0-0-1-20180301/20180331/')

import requests
from bs4 import BeautifulSoup
import os
import re

### 说明：
### 爬取前请在以下网页的最下部确认最大页数，然后修改MAX_PAGE
### https://beijing.douban.com/events/week-exhibition 
MAX_PAGE = 7



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

fail_case = open('E:/fail_case.txt', 'a', encoding='utf-8')


# 得到主要数据，并写入文件夹
def main():
    base_url = "https://beijing.douban.com/events/week-exhibition?start="
    end_url = "&orderby=recent"
    path = "豆瓣"
    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(0, MAX_PAGE * 10 , 10):
        url = base_url + str(i) + end_url
        response = requests.get(url, headers=headers)
        text = BeautifulSoup(response.text, "lxml")
        for item in text.find_all('div', {'class': "title"}):
            # 请求新链接
            url_new = item.find('a').get('href')
            response_new = requests.get(url_new, headers=headers)
            text_new = BeautifulSoup(response_new.content, "lxml", from_encoding="utf-8")

            title = text_new.find('head').find('title').text.strip()
            title = title.replace("|", ",").replace("<", " ").replace(">", " ").replace(":", ",").replace("\"", " ").replace("*", " ").replace("?", " ")
            print(title)
            print(url_new)
            file = open(path + "/" + title + ".txt", "w", encoding="utf-8")
            file.writelines(title + "\n")
            try:
                event_info = text_new.find_all('div', {'class': 'event-detail'})
                time = event_info[0].find('li').text.replace('显示时间详情', ' ').strip('\n').strip()
                file.writelines("时间: " + time + "\n")
                for item in event_info[1:]:
                    if item is None:
                        continue
                    file.writelines(item.text.strip() + "\n")
            except Exception as e:
                print(title, e, "top table fail!")
                fail_case.writelines(url_new + " " + title + "\n")
            try:
                file.writelines("\n活动详情\n")
                related_info = text_new.find('div', {'class':'related_info'}).find('div', {'id': 'link-report'}).find('div', {'id': "edesc_s"})
                file.writelines(str(related_info).replace('<br/>','\n'))
            except Exception as e:
                print(title, e, "realted info fail!")
        file.close()

				
# 从文件夹读入数据，并清理无用数据
def precess():
    file_all = (list(os.walk(top="豆瓣")))[0][2]
    if not os.path.exists("豆瓣/清洗后"):
        os.makedirs("豆瓣/清洗后")
    for file in file_all:
        f = open("豆瓣/" + file, "r+", encoding="utf-8")
        data = f.readlines()
        new_file = open('豆瓣/清洗后/' + file, "w", encoding="utf-8")
        for item in data:
            if re.search("^<", item):
                print("检测到", item)
                continue
            else:
                new_file.writelines(item)
        new_file.close()

if __name__ == "__main__":
    main()
    precess()

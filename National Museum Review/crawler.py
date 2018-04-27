from selenium import webdriver
import time
import random


file = open('国家博物馆.txt', "w")
url = "http://www.mafengwo.cn/poi/34665.html"
# 初始化
driver = webdriver.Safari()
# 请求网页
driver.get(url)
# 最大化浏览器窗口
driver.maximize_window()
# 查找元素
button = driver.find_element_by_xpath("//a[@title='后一页']")
count = 1
while True:
    print("*" * 100)
    print("第{}页".format(count))
    print("*" * 100, "\n")
    data = driver.find_elements_by_xpath("//p[@class='rev-txt']")
    for content in data:
        file.writelines(content.text.strip("\n").strip() + "\n")
        print(content.text)
    try:
        count += 1
        button = driver.find_element_by_xpath("//a[@title='后一页']")
        button.click()
        if count > 5 and random.uniform(0, 1) > 0.5:
            time.sleep(1)
            head = driver.find_element_by_xpath("//h1")
            head.click()
            time.sleep(random.uniform(1, 1.5))
        time.sleep(random.uniform(5, 9))
    except Exception as e:
        print("\n\n", e)
        print("结束!")
        break

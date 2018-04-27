

'''
第1部分，定义读取信息，得到表格的函数
'''
###工商信息
def get_table(bs2bj,str2):
    #str1 中文; str2 网页
    table_info = []
    try:
        print("爬取工商信息")
        #table_row = bs2bj.find('section',{'id':str2}).find('table').findAll('tr')
        table_row = bs2bj.find_all('table')[0].findAll('tr')
        table = []
        for row in table_row:
            for cell in row.findAll('td'):
                table.append(cell.get_text().strip(" 查看地图  附近").strip())
        label = [table[x] for x in range(0,len(table),2)]
        data = [table[x] for x in range(1,len(table),2)]
        table_info.append( dict(zip(label,data)) )
    except Exception as e:
        print(e)
    return table_info
###股东信息
def get_table1(bs2bj,str2):
    table_info = []
    try:
        print("爬取股东信息")
        #table_row = bs2bj.find('section',{'id':str2}).find("table").findAll('tr')
        table_row = bs2bj.find_all('table')[1].findAll('tr')
        label = []
        data = []
        for row in table_row:
            people = []
            for cell in row.findAll('th'):
                label.append(cell.get_text().strip())
            for cell in row.findAll('td'):
                people.append(cell.get_text().strip()[:10].strip())
            data.append(people)
        for people in data[1:]:
            table_info.append( dict(zip(label,people)) )
    except Exception as e:
        print(e)
    return table_info
###主要人员
def get_table2(bs2bj,str2):
    table_info = []
    try:
        print("爬取主要人员信息")
        #table_row = bs2bj.find('section',{'id':str2}).find("table").findAll('tr')
        table_row = bs2bj.find_all('table')[2].findAll('tr')
        label = []
        data = []
        for row in table_row:
            people = []
            for cell in row.findAll('th'):
                label.append(cell.get_text().strip())
            for cell in row.findAll('td'):
                people.append(cell.get_text().strip())
            data.append(people)
        for people in data[1:]:
            people[0] = people[0][11:].strip()
            table_info.append( dict(zip(label,people)) )
    except Exception as e:
        print(e)
    return table_info
'''
第2部分，获取公司的链接，开始得到信息
'''


###获取公司链接得到bs0bj
def search_firm(company_name):
    ###获取公司链接得到bs0bj
    try:
        print("开始爬取:"+company_name)
        params = {'key':company_name}
        response = requests.get(url="http://www.qichacha.com/search",params = params,headers=headers)
        response.encoding = 'utf-8'
        html = response.text
        bs0bj = BeautifulSoup(html,"lxml")
        return bs0bj
    except Exception as e:
        print(e)
        print("ip被封,程序休眠")
        coll.remove({"公司": company_name})
        time.sleep(random.uniform(30000, 40000))
        main()

###获取基本信息
def get_firm_info(bs0bj,Name):
    host_link = "http://www.qichacha.com"
    ###Target_url
    try:
        Target_url = bs0bj.findAll("a",href = re.compile("^(/firm_)((?!:).)*$"))[0]
        Final_url = host_link  + Target_url.get('href')
        ###获取目标公司的详细页面
        print(Final_url)
        response_2 = requests.get(url=Final_url,headers=headers)
        print(response_2.status_code)
        response_2.encoding = 'utf-8'
        html_2 = response_2.text
        bs2bj = BeautifulSoup(html_2,"lxml")
        ###获取公司基本信息
        print("开始爬取基本信息")
        com_info = get_table(bs2bj,'Cominfo')
        com_list = {"工商信息":com_info}
        time.sleep(0.8)
        stock_info = get_table1(bs2bj,'Sockinfo')
        stock_list = {"股东信息":stock_info}
        time.sleep(0.8)
        staff_info = get_table2(bs2bj,'Mainmember')
        staff_list = {"主要人员":staff_info}
        time.sleep(0.8)
        return [com_list,stock_list,staff_list]
    except Exception as e:
        print(e)
        print("ip被封,程序休眠")
        coll.remove({"公司": Name})
        time.sleep(random.uniform(30000, 40000))
        main()
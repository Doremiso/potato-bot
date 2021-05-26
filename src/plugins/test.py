import requests
from bs4 import BeautifulSoup, Tag


WIKI_HOST = "https://wiki.biligame.com"

res = requests.get("https://wiki.biligame.com/pcr/静流")
# print(res.text)
html = BeautifulSoup(res.text, 'lxml')
html = html.find(title="角色讨论/攻略")
tables = html.find_all('table')
if tables:
    table1 = tables[0]
    # 判断有没有攻略
    if '角色攻略' in table1.th.text:
        for li in table1.find_all('li'):
            print(li.a['title'])
            print(WIKI_HOST + li.a['href'])
            # 有攻略的话把第一个表格抛出去
            tables.pop(0)
    for table in tables:
        # 下面的表格都是评价
        print(table.text)
else:
    print("暂无")

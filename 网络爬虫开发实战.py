import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from lxml import etree

def get_one_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def main():
    url = 'https://www.taptap.com/top/sell'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    html = requests.get(url)
    # html = get_one_page(url)
    selector = etree.HTML(html.text)
    print(selector)
    # doc = pq(html)
    # doc=pq(filename='test.html', parser='html')
    # print(doc('#2021-11-12 .gamelist a'))
    # items=doc('#2021-11-11 .gamelist a')
    # print(items)
    # left=items.find('.item .subdiv.leftside img')
    # itemss=items.items()
    # i=0
    # for item in itemss:
    #     print(i,item.find('.item .subdiv.leftside img').attr('data-original'))
    #     print(i, item.find('.item .subdiv.rightside .info_title em').text())
    #     print(i,item.find('.item .subdiv.rightside .info_title span').text())
    #     print(i, item.find('.item .subdiv.rightside .info_mark div').text())
    #     print(i, item.find('.item .subdiv.rightside .info_mark span img').attr('src'))
    #     if 'android' in str(item.find('.item .subdiv.rightside .info_mark span')):
    #         print(i,'安卓')
    #     if 'android' in str(item.find('.item .subdiv.rightside .info_mark span')):
    #         print(i,'ios')
    #     i=i+1


main()
import requests
import random
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
from pyquery import PyQuery as pq

def my_get_soup(url):
    headers = {'user-agent':get_ua()}
    res = requests.get(url,headers = headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    return soup

def get_ua():
    au = random.choice(uas)
    return au

uas = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",\
       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",\
       "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"]

# url='https://www.taptap.com/webapiv2/app-list/v1/detail?_trackParams=%7B%22refererLogParams%22%3A%7B%7D%7D&from=10&id=378&limit=10&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D50%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC'
# url='https://www.taptap.com/webapiv2/app-list/v1/detail?rec_by_app_id=204487&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D50%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC'
page=0
# url='https://www.taptap.com/webapiv2/app-list/v1/detail?_trackParams=%7B%22refererLogParams%22%3A%7B%7D%7D&id=378&limit='+str(page*10)+'&from=10&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D50%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC'
url='https://www.taptap.com/webapiv2/app-list/v1/detail?id=378&_trackParams=%7B%22refererLogParams%22:%7B%7D%7D&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D50%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC'
res = requests.get(url)
res.encoding = 'utf-8'
soup = my_get_soup(url)
# print(soup)
data0=json.loads(str(soup))
print(data0)
data=open("tmp/tmp.txt", 'w+')
print(data0,file=data)
data.close()
mlist=data0['data']['list']
for game in mlist:
    print(game['id'],
          game['title'],
          game['stat']['rating']['score'])
    mbrowser = webdriver.Chrome()
    mbrowser.get('https://www.taptap.com/app/'+str(game['id']))
    time.sleep(3)
    mdoc = pq(mbrowser.page_source)
    mbrowser.close()
    for yanfa in mdoc('.tap-text-group.tap-text-group--inline a').items():
        print(yanfa.find('.caption-m12-w14.gray-04.game-info__key').text(),
              yanfa.find('.caption-m12-w14.gray-06').text())
    for guanzhu in mdoc('.game-info__text-item .game-info__stat--text').items():
        print(guanzhu.find('.caption-m12-w14.gray-04.game-info__key').text(),
              guanzhu.find('.caption-m12-w14.gray-06').text())
    for pingtai in mdoc(
            '.app-detail-button.tap-button.tap-button--large.tap-button--primary.tap-button--wide-screen.tap-button--pc.flex-center').items():
        column = pingtai.find('svg').attr('class')[pingtai.find('svg').attr('class').rfind('-') + 1:]
        value = pingtai.text()
        print(column,value)

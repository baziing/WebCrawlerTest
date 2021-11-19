import requests
import random
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
from pyquery import PyQuery as pq
import pandas as pd

def get_soup(url):
    headers = {'user-agent':get_ua()}
    res = requests.get(url,headers = headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    return soup

def get_ua():
    au = random.choice(uas)
    return au

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

df = pd.DataFrame(columns=['input','update','来源','id','name','评分','下载','关注','预约','label','开发','发行','厂商','android','ios','href'])
uas = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",\
       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",\
       "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"]

url0='https://www.taptap.com/webapiv2/app-list/v1/detail?id=378&_trackParams=%7B%22refererLogParams%22:%7B%7D%7D&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D50%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC'
page=364
i=0
while True:
    print('page'+str(page)+'-----------------------------------------------------')
    if page == 0:
        murl = url0
        print('0')
    else:
        murl = 'https://www.taptap.com/webapiv2/app-list/v1/detail?_trackParams=%7B%22refererLogParams%22%3A%7B%7D%7D&id=378&limit=10&from='+str(page*10)+'&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D50%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC'
        print('1')
    msoup = get_soup(murl)
    mjson = json.loads(str(msoup))
    mlist = mjson['data']['list']
    if len(mlist)<=0:
        break
    for game in mlist:
        strlabel=''
        j=0
        for tag in game['tags']:
            if j>0:
                strlabel=strlabel+','
            strlabel=strlabel+tag['value']
            j=j+1
        if '单机' in strlabel:
            continue
        df.loc[i, 'input'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        df.loc[i, 'update'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        df.loc[i, '来源'] = 'TAPTAP新游'
        df.loc[i, 'id']=game['id']
        df.loc[i,'name']=game['title']
        df.loc[i, '评分']=game['stat']['rating']['score']
        df.loc[i,'label']=strlabel
        df.loc[i, 'href']='https://www.taptap.com/app/'+str(game['id'])
        mbrowser = webdriver.Chrome(options=chrome_options)
        mbrowser.get('https://www.taptap.com/app/' + str(game['id']))
        time.sleep(3+random.random()*2)
        mdoc = pq(mbrowser.page_source)
        mbrowser.close()
        for yanfa in mdoc('.tap-text-group.tap-text-group--inline a').items():
            # print(yanfa.find('.caption-m12-w14.gray-04.game-info__key').text(),
            #       yanfa.find('.caption-m12-w14.gray-06').text())
            column=yanfa.find('.caption-m12-w14.gray-04.game-info__key').text()
            value=yanfa.find('.caption-m12-w14.gray-06').text()
            if column in ['开发','发行','厂商']:
                df.loc[i,column]=value
        for guanzhu in mdoc('.game-info__text-item .game-info__stat--text').items():
            # print(guanzhu.find('.caption-m12-w14.gray-04.game-info__key').text(),
            #       guanzhu.find('.caption-m12-w14.gray-06').text())
            column=guanzhu.find('.caption-m12-w14.gray-04.game-info__key').text()
            value=guanzhu.find('.caption-m12-w14.gray-06').text()
            if column in ['下载','关注','预约']:
                df.loc[i,column]=int(value)
        for pingtai in mdoc('.app-detail-button.tap-button.tap-button--large.tap-button--primary.tap-button--wide-screen.tap-button--pc.flex-center').items():
            column=pingtai.find('svg').attr('class')[pingtai.find('svg').attr('class').rfind('-')+1:]
            value=pingtai.text()
            if column in ['android','ios']:
                df.loc[i, column] = value
        print(i,df.loc[i,'name'])
        i=i+1
    page=page+1
    df.to_excel('新游'+str(page)+'-.xlsx', index=False)
    # murl = url
    # msoup = get_soup(murl)
    # mjson = json.loads(str(msoup))
    # mlist = mjson['data']['list']

df.to_excel('新游.xlsx',index=False)


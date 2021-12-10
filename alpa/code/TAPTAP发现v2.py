import requests
import random
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import pandas as pd
from alpa.model.TaptapDetail import TDetail

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

def run(tag,page):
    while True:
        print('page' + str(page) + '-----------------------------------------------------')
        if tag=='预约':
            if page == 0:
                murl = 'https://www.taptap.com/webapiv2/app-list/v1/detail?id=378&_trackParams=%7B%22refererLogParams%22:%7B%7D%7D&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D50%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC'
            else:
                murl = 'https://www.taptap.com/webapiv2/app-list/v1/detail?_trackParams=%7B%22refererLogParams%22%3A%7B%7D%7D&id=378&limit=10&from=' + str(
                    page * 10) + '&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D50%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC'
        elif tag=='测试':
            if page == 0:
                murl = 'https://www.taptap.com/webapiv2/app-list/v1/detail?id=386&_trackParams=%7B%22refererLogParams%22:%7B%7D%7D&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D51%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC'
            else:
                murl = 'https://www.taptap.com/webapiv2/app-list/v1/detail?_boothInfo=%7B%22booth%22%3A%226380ff69_fdb81479%22%2C%22booth_id%22%3A%22251a4226e33e48a383b05730714b4035_6285fd916742407c8f1e9f5b8ec54911%22%2C%22booth_index%22%3A%222_8%22%7D&_trackParams=%7B%22refererLogParams%22%3A%7B%7D%2C%22rBoothInfo%22%3A%7B%22booth%22%3A%226380ff69_fdb81479%22%2C%22booth_id%22%3A%22251a4226e33e48a383b05730714b4035_6285fd916742407c8f1e9f5b8ec54911%22%2C%22booth_index%22%3A%222_8%22%7D%7D&id=386&limit=10&from=' + str(
                    page * 10) + '&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D51%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC'
        else:
            print('输入格式不对')
            return
        msoup = get_soup(murl)
        mjson = json.loads(str(msoup))
        mlist = mjson['data']['list']
        if len(mlist) <= 0:
            break
        for game in mlist:
            strlabel = ''
            j = 0
            for tag in game['tags']:
                if j > 0:
                    strlabel = strlabel + ','
                strlabel = strlabel + tag['value']
                j = j + 1
            if '单机' in strlabel:
                continue
            TDetail().loadUrl('https://www.taptap.com/app/' + str(game['id']))
        page = page + 1


if __name__ == '__main__':
    print('TAPTAP最新预约-----------------------------------------------------')
    run('预约', 0)
    print('TAPTAP最新测试-----------------------------------------------------')
    run('测试',0)
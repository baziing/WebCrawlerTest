import requests
from pyquery import PyQuery as pq
from selenium import webdriver
import time
import numpy as np
import pandas as pd

def refresh(browser):
    jsCode = "var q=document.documentElement.scrollTop=100000"
    for i in range(0, 3):
        browser.execute_script(jsCode)
        time.sleep(3)

def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # 1手动刷新
    # browser = webdriver.Chrome(options=chrome_options)
    browser = webdriver.Chrome()
    browser.get('https://www.taptap.com/top/reserve')
    time.sleep(3)
    # refresh(browser)
    doc=pq(browser.page_source)
    browser.close()
    gamemain=doc('.tap-list.list-content__list .game-card.flex-center--y')
    gameByDay=gamemain.items()
    i=0
    for day in gameByDay:
        strlabel=''
        j=0
        for label in day('.tap-row-card__contents.flex-1.x-start-y-center .label-tag-group-wrapper.app-row-card__tags a').items():
            if j>0:
                strlabel=strlabel+','
            strlabel=strlabel+label.find('div').text()
            j=j+1
        if '单机' in strlabel:
            continue
        print(day.find('.tap-row-card__contents.flex-1.x-start-y-center a').attr('href'),
              day.find('.tap-row-card__contents.flex-1.x-start-y-center a').attr('title'),
              day.find('.tap-row-card__contents.flex-1.x-start-y-center .app-rating__number.font-bold.rate-number-font').text(),
              strlabel)
        df.loc[i,'input']=time.strftime('%Y/%m/%d',time.localtime(time.time()))
        df.loc[i, 'update'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        df.loc[i,'来源']='TAPTAP热门榜'
        df.loc[i,'id']=int(day.find('.tap-row-card__contents.flex-1.x-start-y-center a').attr('href')[day.find('.tap-row-card__contents.flex-1.x-start-y-center a').attr('href').rfind('/')+1:])
        df.loc[i,'name']=day.find('.tap-row-card__contents.flex-1.x-start-y-center a').attr('title')
        df.loc[i,'评分']=float(day.find('.tap-row-card__contents.flex-1.x-start-y-center .app-rating__number.font-bold.rate-number-font').text())
        df.loc[i,'label']=strlabel
        df.loc[i,'href']='https://www.taptap.com'+day.find('.tap-row-card__contents.flex-1.x-start-y-center a').attr('href')
        # mbrowser = webdriver.Chrome(options=chrome_options)
        mbrowser = webdriver.Chrome()
        mbrowser.get('https://www.taptap.com'+day.find('.tap-row-card__contents.flex-1.x-start-y-center a').attr('href'))
        time.sleep(3)
        mdoc=pq(mbrowser.page_source)
        mbrowser.close()
        for yanfa in mdoc('.tap-text-group.tap-text-group--inline a').items():
            print(yanfa.find('.caption-m12-w14.gray-04.game-info__key').text(),
                  yanfa.find('.caption-m12-w14.gray-06').text())
            column=yanfa.find('.caption-m12-w14.gray-04.game-info__key').text()
            value=yanfa.find('.caption-m12-w14.gray-06').text()
            if column in ['开发','发行','厂商']:
                df.loc[i,column]=value
        for guanzhu in mdoc('.game-info__text-item .game-info__stat--text').items():
            print(guanzhu.find('.caption-m12-w14.gray-04.game-info__key').text(),
                  guanzhu.find('.caption-m12-w14.gray-06').text())
            column=guanzhu.find('.caption-m12-w14.gray-04.game-info__key').text()
            value=guanzhu.find('.caption-m12-w14.gray-06').text()
            if column in ['下载','关注']:
                df.loc[i,column]=int(value)
        for pingtai in mdoc('.app-detail-button.tap-button.tap-button--large.tap-button--primary.tap-button--wide-screen.tap-button--pc.flex-center').items():
            column=pingtai.find('svg').attr('class')[pingtai.find('svg').attr('class').rfind('-')+1:]
            value=pingtai.text()
            if column in ['android','ios']:
                df.loc[i, column] = value
        if i>2:
            break
        i=i+1


df = pd.DataFrame(columns=['input','update','来源','id','name','评分','下载','关注','label','开发','发行','厂商','android','ios','href'])
main()
print(df)
df.to_excel('tmp.xlsx',index=False)
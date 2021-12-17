from selenium import webdriver
from pyquery import PyQuery as pq
import time
import alpa.model.GameDB
import re
import requests
from bs4 import BeautifulSoup
import random
import json
from urllib.parse import quote

class TDetail:
    chrome_options = webdriver.ChromeOptions()
    test1 = {'开发': 'yanfa', '发行': 'faxing', '厂商': 'changshang', '下载': 'taptap_downloads', '关注': 'taptap_follow',
             '预约': 'taptap_reserve', 'android': 'taptap_android', 'ios': 'taptap_ios'}

    def __init__(self):
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')


    def my_get_soup(self,url):
        headers = {'user-agent': self.get_ua()}
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup

    def get_ua(self):
        uas = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"]
        au = random.choice(uas)
        return au

    def loadUrl(self,url):
        mbrowser = webdriver.Chrome(options=self.chrome_options)
        mbrowser.get(url=url)
        time.sleep(3)
        mdoc = pq(mbrowser.page_source)
        mbrowser.close()

        # 判断tag
        strlabel = ''
        tags=mdoc('.app-info-summary.app-detail__section-card.app-detail__warp .swiper-wrapper .swiper-slide').items()
        for tag in tags:
            if '单机' in tag.find('a').text():
                return
            if tag.find('a').text()=='':
                continue
            if strlabel!='':
                strlabel=strlabel+','
            strlabel=strlabel+tag.find('a').text()

        dict = {}
        dict['input_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dict['update_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dict['source'] = 'TAPTAP'
        dict['taptap_id'] =int(re.findall('\d+',url)[0])
        dict['name'] = mdoc.find(
            '.tap-long-text__contents.list-heading-m16-w18.font-bold.primary-white.header-banner__title-text.tap-long-text__contents--inline').text().replace('（预下载）','').replace('预下载','')
        if dict['name']=='':
            soup=self.my_get_soup('https://www.taptap.com/webapiv2/review/v2/by-app?app_id='+str(dict['taptap_id'])+'&limit=4&type=no_collapsed&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D53%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC')
            data = json.loads(str(soup))
            dict['name']=data['data']['list'][0]['moment']['app']['title']
        try:
            dict['taptap_score']=float(mdoc.find('.game-info__stat--review-number.app-rating__number.font-bold.rate-number-font').text())
        except :
            dict['taptap_score']=float(0)
        dict['label'] = strlabel
        dict['href']=url
        for yanfa in mdoc('.tap-text-group.tap-text-group--inline a').items():
            column=yanfa.find('.caption-m12-w14.gray-04.game-info__key').text()
            value=yanfa.find('.caption-m12-w14.gray-06').text()
            if column in ['开发','发行','厂商']:
                dict[self.test1[column]] = value
        for guanzhu in mdoc('.game-info__text-item .game-info__stat--text').items():
            column=guanzhu.find('.caption-m12-w14.gray-04.game-info__key').text()
            value=guanzhu.find('.caption-m12-w14.gray-06').text()
            if column in ['下载','关注','预约']:
                dict[self.test1[column]] = int(value)
        for pingtai in mdoc('.app-detail-button.tap-button.tap-button--large.tap-button--primary.tap-button--wide-screen.tap-button--pc.flex-center').items():
            column=pingtai.find('svg').attr('class')[pingtai.find('svg').attr('class').rfind('-')+1:]
            value=pingtai.text()
            if column in ['android','ios']:
                dict[self.test1[column]] = value
        for infos in mdoc('.app-detail__section-card.app-detail__warp').items():
            if 'data-v-07d6a776' in str(infos):
                for info in infos('main .info-form__item').items():
                    if info.find('.paragraph-m14-w14.gray-06.info-form__item__label').text() in ['网络', 'Network']:
                        dict['network'] = info.find('.paragraph-m14-w14.gray-08.info-form__item__value').text()
                        break
        alpa.model.GameDB.Game('gamedb', 'detail').input(dict)
        return

    def loadName(self,name):
        urlSearch='https://www.taptap.com/webapiv2/mix-search/v2/by-keyword?kw='+quote(name)+'&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D54%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3D28e54860-dfa0-4874-b6d0-433570e41dbe%26DT%3DPC'
        soup = self.my_get_soup(urlSearch)
        results = json.loads(str(soup))['data']['list']
        for result in results:
            if result['type']=='app':
                self.loadUrl('https://www.taptap.com/app/'+str(result['app']['id']))
        return
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
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.30'
        headers = {'user-agent': user_agent,
                   'cookie': '_uab_collina=163697383941465721317365; locale=zh_CN; tapadid=96394516-1882-4570-bdce-528a064420b5; discover_is_old_version=0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217d310432746ef-04f60e17277db5-561a1154-2073600-17d31043275982%22%2C%22%24device_id%22%3A%2217d310432746ef-04f60e17277db5-561a1154-2073600-17d31043275982%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%2C%22%24latest_referrer_host%22%3A%22cn.bing.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; tap_theme=light; _gid=GA1.2.1390872645.1646721036; acw_tc=276077de16467350672614137e06c6f3ce7061772dcb9859e7335a32d8c5f0; _gat=1; _ga_6G9NWP07QM=GS1.1.1646735082.98.1.1646735083.0; _ga=GA1.1.684186635.1637134734; ssxmod_itna=YqRxBD0QG=0Q7qWq0dD=G7Iya1xUr42Bg24rqGXd3DZDiqAPGhDC84U3O8iobnqpXK8Y0TpYef3IjrP4AbzRueDHxY=DUc7GIPTDee=D5xGoDPxDeDAiqGaDb4DrXV4GPnUpT567Dpx0YDzqDgD7j/BqDfiqeeidtLKjX4xGUK+M+diqDMD7tD/3+N1eDBDaWeUdUdueIxlDDHKB47XA47HB+KlDGWirjDqeGuDG=esqL4h16lIMdzyE4WKA+otODqIY4a8B4qYA4YB0mQoDlYlYM37YxqK7GYRtwTRB4DGfx4jFqxD=; ssxmod_itna2=YqRxBD0QG=0Q7qWq0dD=G7Iya1xUr42Bg24xA6uAPqD/U8lDFOizcPrtXE6bz9TdqRGrjbN+H/cfFeOe8cBEQH3v1xxuEUzYkr63lfr0FW+cFA1Ad0osouH8EDcUG7FptgtPfcpbdfNfFfKjAS=RfRIvn+U9WW3HIr+mbdNOBob+bkQXfkEd2S=senUY/WWplxRMtxG2R4GcDiQeeD==; acw_sc__v3=62272ef967702ac2286b767df3943679b4bc2d52; XSRF-TOKEN=eyJpdiI6IjZScklreEtmRkpKK2pIc0ZFcGRVNXc9PSIsInZhbHVlIjoicXFVTVVwSlR4SFdsNU5DbXI1Q0p3WG5mb0xqZWZ1cVk2NG9JQ01zZVpSWXg4OVhsb01aYzFmSXVpNXZzK05EWWkxVXlMUWZaN2RWTHVpRVkrR0M4Umc9PSIsIm1hYyI6IjhiYTk2NjE3NjMxMzUzYjgxY2M0MjAwMTE2MjExZjhiODUwMzhjNDZiMjg3NDhhNDgyMTJhNGY4YTZkMWZhZjMifQ%3D%3D; tap_sess=eyJpdiI6IjI3RkxMMXowbkVaclVBak0xMTdcL21nPT0iLCJ2YWx1ZSI6IjVtdCtEa201bjVYbWlcL3JMRGRIY3JhSk5qcmdBZjY5blRmcmZKSjh6VU9ZQklOU201SDZiRTUxUDNHWE1qZlU4SGVQS01ENlV3ZEZiUVg4WjBQMDR6Zz09IiwibWFjIjoiYzI0YjYxMTY3NmI1NDdlZWZhMjdhMTJkZTEwN2ZjZmI0MzdmMzE0MTVkN2FmNDQ0ZThhZDdmNjY2MDM3MDYxNyJ9'}
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

    def isJson(self,str):
        try:
            json.loads(str)
        except Exception as e:
            return False
        return True

    def getJson(self,id):
        url='https://www.taptap.com/webapiv2/app/v2/detail-by-id/'+str(id)+'?X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D64%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC%26OS%3DWindows%26OSV%3D10'
        soup=self.my_get_soup(url)
        data = str(soup)[:str(soup).rfind('}') + 1].replace('\\','\\\\')
        print(data)
        dict=self.loadJson(json.loads(data))


    def loadJson(self,mjson):
        dict={}
        dict['input_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dict['update_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dict['source'] = 'TAPTAP'
        dict['taptap_id'] = int(mjson['data']['id'])
        dict['name']=mjson['data']['title']
        print(dict)
        return dict





    def loadUrl(self,url):
        mbrowser = webdriver.Chrome(options=self.chrome_options)
        mbrowser.delete_all_cookies()
        mbrowser = webdriver.Chrome()
        mbrowser.get(url=url)
        time.sleep(3)
        mdoc = pq(mbrowser.page_source)
        # print('doc\n',str(mdoc))
        mbrowser.close()
        # if self.isJson(str(mdoc))==True:
        #     mjson=json.loads(str(mdoc))['data']['list'][0]
        if '验证' in str(mdoc):
            return

        # 判断tag
        strlabel = ''
        name=mdoc('tap-long-text__contents list-heading-m16-w18 font-bold extension-button-label-white header-banner__title-text tap-long-text__contents--inline').text()
        tags=mdoc('.web-aside-wrapper--tags').items()
        for tag in tags:
            print(tag)
            if '单机' in tag.find('a').text():
                return
            if tag.find('a').text()=='':
                continue
            if strlabel!='':
                strlabel=strlabel+','
            strlabel=strlabel+tag.find('a').text()

        # 判断区服，非国服
        groupid=mdoc('.tap-long-text.app-detail__banner-title-text.tap-text.tap-text__multi-line.list-heading-m16-w18.font-bold.primary-white.header-banner__title-text')
        if 'tap-tag caption-m10-w12 font-bold tap-tag--default tap-tag--outline tap-tag--gray caption-m10-w12 font-bold gray-06 tap-app-title__tag' in str(groupid):
            return
        # 提示该地区不可下载
        if 'app-detail__button--tips' in str(mdoc):
            return

        dict = {}
        dict['input_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dict['update_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dict['source'] = 'TAPTAP'
        dict['taptap_id'] =int(re.findall('\d+',url)[0])
        dict['name'] = mdoc.find(
            '.tap-long-text__contents.list-heading-m16-w18.font-bold.primary-white.header-banner__title-text.tap-long-text__contents--inline').text().replace('（预下载）','').replace('预下载','')
        print('name',mdoc.find(
            '.tap-long-text__contents.list-heading-m16-w18.font-bold.primary-white.header-banner__title-text.tap-long-text__contents--inline').text().replace('（预下载）','').replace('预下载',''))
        if dict['name']=='':
            soup=self.my_get_soup('https://www.taptap.com/webapiv2/review/v2/by-app?app_id='+str(dict['taptap_id'])+'&limit=4&type=no_collapsed&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D53%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC')
            try:
                data = json.loads(str(soup)[:str(soup).rfind('}') + 1])
                print(data)
                dict['name']=data['data']['list'][0]['moment']['app']['title']
            except:
                print('更新失败')
                return
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
            try:
                column=pingtai.find('svg').attr('class')[pingtai.find('svg').attr('class').rfind('-')+1:]
                value=pingtai.text()
                if column in ['android','ios']:
                    dict[self.test1[column]] = value
            except:
                print('更新平台失败')
        for infos in mdoc('.app-detail__section-card.app-detail__warp').items():
            if 'data-v-07d6a776' in str(infos):
                for info in infos('main .info-form__item').items():
                    if info.find('.paragraph-m14-w14.gray-06.info-form__item__label').text() in ['网络', 'Network']:
                        dict['network'] = info.find('.paragraph-m14-w14.gray-08.info-form__item__value').text()
                        break
        # print(dict)
        alpa.model.GameDB.Game('gamedb', 'detail').input(dict)
        return

    def loadName(self,name):
        urlSearch='https://www.taptap.com/webapiv2/mix-search/v2/by-keyword?kw='+quote(name)+'&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D54%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3D28e54860-dfa0-4874-b6d0-433570e41dbe%26DT%3DPC'
        # urlSearch='https://www.taptap.com/webapiv2/mix-search/v2/by-keyword?kw=%E7%8E%8B%E5%9B%BD%E4%BF%9D%E5%8D%AB%E6%88%98&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D54%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3D28e54860-dfa0-4874-b6d0-433570e41dbe%26DT%3DPC'
        soup = self.my_get_soup(urlSearch)
        try:
            results = json.loads(str(soup)[:str(soup).rfind('}')+1])['data']['list']
            for result in results:
                if result['type']=='app':
                    self.loadUrl('https://www.taptap.com/app/'+str(result['app']['id']))
        except Exception as e:
            print(e,name)
        return
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
                   'cookie':
                       '_uab_collina=163697383941465721317365; locale=zh_CN; tapadid=96394516-1882-4570-bdce-528a064420b5; discover_is_old_version=0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217d310432746ef-04f60e17277db5-561a1154-2073600-17d31043275982%22%2C%22%24device_id%22%3A%2217d310432746ef-04f60e17277db5-561a1154-2073600-17d31043275982%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%2C%22%24latest_referrer_host%22%3A%22cn.bing.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; _gid=GA1.2.1390872645.1646721036; tap_theme=light; acw_tc=276077dc16468212538201552e75f1bc175c5cc45bea6aeadc1f4042fb3dde; _ga_6G9NWP07QM=GS1.1.1646818894.101.1.1646821279.0; _ga=GA1.1.684186635.1637134734; ssxmod_itna=eqUxnDcDuDRiit3q0du7tD97RDC7qt1OD0lQx+x0yDReGzDAxn40iDt==knr+bRDxEteWoWxI5QY28Yux3s8Bh3I/4=x0aDbqGk=0mO4GGUxBYDQxAYDGDDpkDj4ibDY8/7Dj0FU1lj=qGRD0YDzqDgD7jDxeDf7wDPYh6S9S0DTeDSWAUxKG=DjqGgDBdeY1bDGLnToOXSBnuOCDDHDh9xQG9QKix4DYPaQL04xBQD7w2gS3r8sLXMKMHWQiPKA05KS74e7rhxSBxqYrh=fGeNsiCeY7kq70wh7YA6XB3QDDfpIB3xD; ssxmod_itna2=eqUxnDcDuDRiit3q0du7tD97RDC7qt1OD0lQx4nF3q4qDsqK3DLeby4w7vOqk7kD=4X9=iY++/ApoKoCNMeTYqGqYPwxthqWlRivtnDn+B03iYZgTXZKq+IH6wX8qMTS+o+s0tEwoGQOAgX1Dm0HAwN6U325YMr+KM229EoPod0tbxG204GcDiQbeD==; acw_sc__v3=62287fff6b0bceb3eaa3ed54b27c688d9db77161; XSRF-TOKEN=eyJpdiI6InhpV0d6SWV3Y0RBVzF3UEJmNlwvU1wvdz09IiwidmFsdWUiOiJ1UHlCRkV3RHd6d1NkYTdpUWNtVCtEWmVqaFhIeVE2eUgrUmFxc0dOWXNGRGhsZkF4c2RvcFFlOUpxTEZhNFN6Y2FPSVJTZ2EyVXRRUXphUVpHbjRTUT09IiwibWFjIjoiNjg3MmU3NzZlYjdmMzllNjFlNzdmZWQ1MzEwMWU4YTk4Y2ZlNzliNTNmZjhhZWNmNTQ5MjQ4ZjdlZDQ3MzQyYSJ9; tap_sess=eyJpdiI6IlFERFwvRk5iNUV0YlczQnZITjZUMDdRPT0iLCJ2YWx1ZSI6IkdrTjV1cmJ1a2lyVFdNQUdnSU5GRnU5bUpkSzJzbzR3YU5raTZkMEtuaVFsc2owWnNzTmZjZUJvYVozVUlmekZERVg2V2cxM3lvTkRWbFBPM2d5bW1RPT0iLCJtYWMiOiIwNjA3MjU5OTc3NzY3ZDFiYjczMGE1NjRlZTkxYmFjYWRmZGNlYmI1YTFjOGJiZTk3Mjk4MTk3MmJiNWUzNzA5In0%3D'
                   }
        res = requests.get(url, headers=headers)
        res.encoding = 'gbk'
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


    def loadJson(self,id):
        url = 'https://www.taptap.com/webapiv2/app/v2/detail-by-id/' + str(id) \
              + '?X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D64%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC%26OS%3DWindows%26OSV%3D10'
        soup=self.my_get_soup(url)
        soup.prettify("gbk")

        dict={}
        dict['input_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dict['update_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dict['source'] = 'TAPTAP'
        print(str(soup))
        dict['name']=re.search("\"title\":.*?,",str(soup)).group().replace('\"title\":\"','').replace(',','').rstrip('\"').encode('utf-8').decode('unicode_escape')
        dict['href']='https://www.taptap.com/app/'+str(id)
        dict['network'] = json.loads('{' + re.search(r'\"title\":\"\\u7f51\\u7edc\",\"text\":.+?}', str(soup)).group())['text']
        dict['taptap_android']=re.search("\"button_label\":.*?,",str(soup)).group().replace('\"button_label\":\"','').rstrip(',').rstrip('\"').encode('utf-8').decode('unicode_escape')
        dict['taptap_ios']=re.search('\"apple\":.*?\,\"taptap_current\"',str(soup)).group().replace('\"apple\":\"','').replace('\",\"taptap_current\"','').encode('utf-8').decode('unicode_escape')
        if dict['taptap_ios']=='':
            dict['taptap_ios']=json.loads('{'+re.search('\"uri\":{\"apple\":.*?}',str(soup)).group()+'}')['uri']['apple']
        dict['score']=float(json.loads(re.search('{\"score\":.*?,',str(soup)).group().rstrip(',')+'}')['score'])


        labels=json.loads('{'+re.search('\"tags":.*?\]',str(soup)).group()+'}')['tags']
        strlabel=''
        for label in labels:
            if strlabel!='':
                strlabel=strlabel+','
            strlabel=strlabel+label['value']
        dict['label']=strlabel

        devs=json.loads('{'+ re.search('\"developers":.*?\]',str(soup)).group()+'}')['developers']
        for dev in devs:
            if dev['label'] in ['开发', '发行', '厂商']:
                dict[self.test1[dev['label']]]=dev['name']


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
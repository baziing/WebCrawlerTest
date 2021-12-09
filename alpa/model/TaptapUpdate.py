from selenium import webdriver
from pyquery import PyQuery as pq
import time
import alpa.model.GameDB

class TUpdate:
    chrome_options = webdriver.ChromeOptions()
    test1 = {'开发': 'yanfa', '发行': 'faxing', '厂商': 'changshang', '下载': 'taptap_downloads', '关注': 'taptap_follow',
             '预约': 'taptap_reserve', 'android': 'taptap_android', 'ios': 'taptap_ios'}

    def __init__(self):
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')


    def loadUrl(self,url):
        mbrowser = webdriver.Chrome(options=self.chrome_options)
        mbrowser.get(url=url)
        time.sleep(3)
        mdoc = pq(mbrowser.page_source)
        mbrowser.close()
        dict = {}
        dict['input_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dict['update_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dict['source'] = 'TAPTAP'
        # dict['taptap_id']=int(url[url.rfind('/')+1:])
        # dict['name']=mdoc.find('.tap-long-text__contents.list-heading-m16-w18.font-bold.primary-white header-banner__title-text tap-long-text__contents--inline span').text().strip('（预下载）').replace('预下载','')
        dict['name'] = mdoc.find(
            '.tap-long-text__contents.list-heading-m16-w18.font-bold.primary-white.header-banner__title-text.tap-long-text__contents--inline').text().replace('（预下载）','').replace('预下载','')
        try:
            dict['taptap_score']=float(mdoc.find('.game-info__stat--review-number.app-rating__number.font-bold.rate-number-font').text())
        except :
            dict['taptap_score']=float(0)
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
        db = alpa.model.GameDB.Game('gamedb', 'detail').input(dict)
        # print(dict)
        return
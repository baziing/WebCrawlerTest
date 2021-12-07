from pyquery import PyQuery as pq
from selenium import webdriver
import time
from alpa.GameDB import Game

def refresh(browser):
    jsCode = "var q=document.documentElement.scrollTop=100000"
    for i in range(0, 10):
        browser.execute_script(jsCode)
        time.sleep(3)

def run(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # 1手动刷新
    browser = webdriver.Chrome(options=chrome_options)
    # browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(3)
    refresh(browser)
    doc=pq(browser.page_source)
    browser.close()
    gamemain=doc('.tap-list.list-content__list .game-card.flex-center--y')
    gameByDay=gamemain.items()
    i=0
    for day in gameByDay:
        dict={}
        strlabel=''
        j=0
        for label in day('.tap-row-card__contents.flex-1.x-start-y-center .label-tag-group-wrapper.app-row-card__tags a').items():
            if j>0:
                strlabel=strlabel+','
            strlabel=strlabel+label.find('div').text()
            j=j+1
        if '单机' in strlabel:
            continue
        dict['input_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dict['update_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dict['source'] = 'TAPTAP'
        dict['taptap_id'] = int(day.find('.tap-row-card__contents.flex-1.x-start-y-center a').attr('href')[day.find('.tap-row-card__contents.flex-1.x-start-y-center a').attr('href').rfind('/')+1:])
        dict['name'] = day.find('.tap-row-card__contents.flex-1.x-start-y-center a').attr('title')
        dict['taptap_score'] = float(day.find('.tap-row-card__contents.flex-1.x-start-y-center .app-rating__number.font-bold.rate-number-font').text())
        dict['label'] = strlabel
        dict['href'] = 'https://www.taptap.com'+day.find('.tap-row-card__contents.flex-1.x-start-y-center a').attr('href')
        mbrowser = webdriver.Chrome(options=chrome_options)
        mbrowser.get('https://www.taptap.com'+day.find('.tap-row-card__contents.flex-1.x-start-y-center a').attr('href'))
        time.sleep(3)
        mdoc=pq(mbrowser.page_source)
        mbrowser.close()
        for yanfa in mdoc('.tap-text-group.tap-text-group--inline a').items():
            column=yanfa.find('.caption-m12-w14.gray-04.game-info__key').text()
            value=yanfa.find('.caption-m12-w14.gray-06').text()
            if column in ['开发','发行','厂商']:
                dict[test1[column]] = value
        for guanzhu in mdoc('.game-info__text-item .game-info__stat--text').items():
            column=guanzhu.find('.caption-m12-w14.gray-04.game-info__key').text()
            value=guanzhu.find('.caption-m12-w14.gray-06').text()
            if column in ['下载','关注','预约']:
                dict[test1[column]] = int(value)
        for pingtai in mdoc('.app-detail-button.tap-button.tap-button--large.tap-button--primary.tap-button--wide-screen.tap-button--pc.flex-center').items():
            column=pingtai.find('svg').attr('class')[pingtai.find('svg').attr('class').rfind('-')+1:]
            value=pingtai.text()
            if column in ['android','ios']:
                dict[test1[column]] = value
        for infos in mdoc('.app-detail__section-card.app-detail__warp').items():
            if 'data-v-07d6a776' in str(infos):
                for info in infos('main .info-form__item').items():
                    if info.find('.paragraph-m14-w14.gray-06.info-form__item__label').text() in ['网络', 'Network']:
                        dict['network'] = info.find('.paragraph-m14-w14.gray-08.info-form__item__value').text()
                        break
        db = Game('gamedb', 'detail').input(dict)
        i=i+1

test1={'开发':'yanfa','发行':'faxing','厂商':'changshang','下载':'taptap_downloads','关注':'taptap_follow','预约':'taptap_reserve','android':'taptap_android','ios':'taptap_ios'}
if __name__ == '__main__':
    print('TAPTAP热门榜-----------------------------------------------------')
    run('https://www.taptap.com/top/download')
    print('TAPTAP预约榜-----------------------------------------------------')
    run('https://www.taptap.com/top/reserve')
    print('TAPTAP新品榜-----------------------------------------------------')
    run('https://www.taptap.com/top/new')
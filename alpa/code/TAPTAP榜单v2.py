from pyquery import PyQuery as pq
from selenium import webdriver
import time
from alpa.model.TaptapDetail import TDetail

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
    browser.get(url)
    time.sleep(3)
    refresh(browser)
    doc=pq(browser.page_source)
    browser.close()
    gamemain=doc('.tap-list.list-content__list .game-card.flex-center--y')
    gameByDay=gamemain.items()
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
        TDetail().loadUrl('https://www.taptap.com'+day.find('.tap-row-card__contents.flex-1.x-start-y-center a').attr('href'))

if __name__ == '__main__':
    print('TAPTAP热门榜-----------------------------------------------------')
    run('https://www.taptap.com/top/download')
    print('TAPTAP预约榜-----------------------------------------------------')
    run('https://www.taptap.com/top/reserve')
    print('TAPTAP新品榜-----------------------------------------------------')
    run('https://www.taptap.com/top/new')
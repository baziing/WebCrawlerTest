import requests
from pyquery import PyQuery as pq
from selenium import webdriver
import time
import numpy as np
import pandas as pd

def main():
    # 1手动刷新
    browser = webdriver.Chrome()
    browser.get('https://www.taptap.com/top/download')
    time.sleep(10)
    # 自动下拉
    jsCode = "var q=document.documentElement.scrollTop=100000"
    for i in range(0, 5):
        browser.execute_script(jsCode)
        time.sleep(3)
    browser.execute_script(jsCode)
    time.sleep(3)
    print("拖动滑动条到底部...")
    doc=pq(browser.page_source)
    browser.close()
    # doc = pq(filename='test.html', parser='html')   # 2本地文件
    # doc=pq(url='https://www.gameres.com/newgame')   # 3在线
    gamemain=doc('.tap-list.list-content__list .game-card.flex-center--y')
    print(gamemain)
    gameByDay=gamemain.items()
    for day in gameByDay:
        print(day.find('.tap-row-card__left a').attr('href'))
    # i=0
    # for day in gameByDay:
    #     # print(i,day.attr('id'))
    #     games=day('.gamelist a').items()
    #     for game in games:
    #         # 研发和发行判断
    #         test=game.find('.item .subdiv.rightside .info_mark div span').text().replace(u'\xa0','')
    #         if '|' in test:
    #             yanfa=test[test.rfind(':')+1:]
    #             faxing=test[test.rfind(':')+1:]
    #         else:
    #             yanfa=test[test.rfind('研发')+3:len(test) if test.rfind('发行')==-1 else test.rfind('发行')]
    #             faxing=test[len(test) if test.rfind('发行')==-1 else test.rfind('发行')+3:]
    #
    #         # 平台判断
    #         platforms=''
    #         for icon in game('.item .subdiv.rightside .plat_icon img').items():
    #             if platforms!='':
    #                 platforms=platforms+','+icon.attr('src')[icon.attr('src').rfind('/')+1:-4]
    #             else:
    #                 platforms=icon.attr('src')[icon.attr('src').rfind('/')+1:-4]
    #
    #         # 写入表格
    #         df.loc[i]=['GameRes',
    #                    day.attr('id'),
    #                    game.find('.item .subdiv.rightside .titlename').text(),
    #                    game.find('.item .subdiv.rightside em').text(),
    #                    platforms,
    #                    yanfa,
    #                    faxing,
    #                    game.find('.item .subdiv.rightside .mark_tag').text(),
    #                    game.attr('href')]
    #         i=i+1

df = pd.DataFrame(columns=['来源', '测试时间','产品名称', '品类','测试平台','开发公司','发行公司','状态','链接'])
main()
# 输出
# df.to_csv('tmp.csv')
from pyquery import PyQuery as pq
from selenium import webdriver
import time
import pandas as pd
from alpa.model.TestDB import GameTest

def main():
    # 1手动刷新
    browser = webdriver.Chrome()
    browser.get('https://www.699h5.com/newgame')
    time.sleep(3)
    #
    jsCode = "var q=document.documentElement.scrollTop=100000"
    # target=browser.find_element_by_class_name('pagediv nextpage')
    # while True:
    #     browser.execute_script(jsCode)
    #     time.sleep(3)
    #     try:
    #         print(browser.execute_script("arguments[0].scrollIntoView();", target)
    # 自动下拉
    for i in range(0,5):
        browser.execute_script(jsCode)
        # print(browser.execute_script("arguments[0].scrollIntoView();", target))
        time.sleep(3)
    target=browser.find_element_by_css_selector("[class='pagediv nextpage']")
    print(target.text)
    # print(browser.execute_script("arguments[0].scrollIntoView();", target))
    browser.execute_script(jsCode)
    time.sleep(10)
    print("拖动滑动条到底部...")

    time.sleep(10)
    doc=pq(browser.page_source)
    browser.close()
    print('close')
    # doc = pq(filename='test.html', parser='html')   # 2本地文件
    # doc=pq(url='https://www.gameres.com/newgame')   # 3在线
    gamemain=doc('#gamemain .one_day_div')
    gameByDay=gamemain.items()
    i=0
    for day in gameByDay:
        # print(i,day.attr('id'))
        games=day('.gamelist a').items()
        for game in games:
            dictA={}
            dictB={}
            dictA['input_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
            dictA['update_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
            dictA['source'] = 'GameRes'
            dictA['name']=game.find('.item .subdiv.rightside .titlename').text()
            dictA['label']=game.find('.item .subdiv.rightside em').text()
            dictA['href']=game.attr('href')
            x=str(game.attr('href'))
            dictA['gameres_id']=int(x[x.rfind('/')+1:x.rfind('.')])

            dictB['input_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
            dictB['update_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
            dictB['source'] = 'GameRes'
            dictB['test_time']=str(day.attr('id')).replace('-','/')
            dictB['name'] = game.find('.item .subdiv.rightside .titlename').text()
            dictB['label'] = game.find('.item .subdiv.rightside em').text()
            dictB['test_name']=game.find('.item .subdiv.rightside .mark_tag').text()

            # 研发和发行判断
            test=game.find('.item .subdiv.rightside .info_mark div span').text().replace(u'\xa0','')
            if '|' in test:
                yanfa=test[test.rfind(':')+1:]
                faxing=test[test.rfind(':')+1:]
                dictA['yanfa']=yanfa
                dictA['faxing']=faxing
            else:
                yanfa=test[test.rfind('研发')+3:len(test) if test.rfind('发行')==-1 else test.rfind('发行')]
                faxing=test[len(test) if test.rfind('发行')==-1 else test.rfind('发行')+3:]
                dictA['yanfa'] = yanfa
                dictA['faxing'] = faxing

            # 平台判断
            platforms=''
            for icon in game('.item .subdiv.rightside .plat_icon img').items():
                if platforms!='':
                    platforms=platforms+','+icon.attr('src')[icon.attr('src').rfind('/')+1:-4]
                else:
                    platforms=icon.attr('src')[icon.attr('src').rfind('/')+1:-4]
            dictB['platform']=platforms
            GameTest('gamedb', 'test').input(dictB)
            i=i+1

df = pd.DataFrame(columns=['来源', '测试时间','产品名称', '品类','测试平台','开发公司','发行公司','状态','链接'])
main()
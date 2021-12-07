from pyquery import PyQuery as pq
import time
from selenium import webdriver
from alpa.TestDB import GameTest
from alpa.GameDB import Game

def intodate(datestr):
    month=datestr[:datestr.find('月')]
    day=datestr[datestr.find('月')+1:datestr.find('日')]
    if int(month)<int(time.strftime('%m', time.localtime(time.time())))-3:
        year=int(time.strftime('%Y', time.localtime(time.time())))+1
    else:
        year=int(time.strftime('%Y', time.localtime(time.time())))
    return str(year)+'/'+str(month)+'/'+str(day)


def getRemark(remark):
    if '（' in remark and '）' in remark:
        remark=remark[remark.find('（')+1:remark.find('）')]
    else:
        remark=''
    return remark

def input():
    # doc = pq(url='http://9game.cn/kc')
    mbrowser = webdriver.Chrome()
    mbrowser.get('http://9game.cn/kc')
    # time.sleep(3 + random.random() * 2)
    doc = pq(mbrowser.page_source)
    mbrowser.close()

    # 今日开测
    today=doc('.today-server-list li').items()
    for game in today:
        dictA={}
        dictA['input_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dictA['update_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dictA['test_time']=time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dictA['source']='九游'
        dictA['name']=game.find('.name').attr('title')
        for span in game('.type .type-con').items():
            if '状态' in span.text():
                dictA['test_name']=span.find('.na').text()
            if '类型' in span.text():
                dictA['label']=span.text().lstrip('类型：').lstrip(' ')
        dictA['platform']=game.find('.tit span').attr('class')
        dictA['remark']=getRemark(game.find('.name').text())
        GameTest('gamedb','test').input(dictA)
        li=['test_time','test_name','platform']
        for col in li:
            dictA.pop(col,404)
        Game('gamedb', 'detail').input(dictA)



    # 即将开测
    coming=doc('.box.open-test-con').items()
    for gameTest in coming:
        for day in gameTest('.des-table1').items():
            for game in day('tr').items():
                dictA={}
                dictA['input_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
                dictA['update_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
                dictA['test_time'] = intodate(day.find('.day').text())
                dictA['source'] = '九游'
                dictA['name'] = game.find('.nametr .name').attr('title')
                dictA['test_name'] = game.find('.stattr').text()
                dictA['label'] = game.find('.typetr').text()
                dictA['platform'] = 'android'
                dictA['remark'] = getRemark(game.find('.name').text())
                GameTest('gamedb', 'test').input(dictA)
                li = ['test_time', 'test_name', 'platform']
                for col in li:
                    dictA.pop(col, 404)
                Game('gamedb', 'detail').input(dictA)


def main():
    input()
    return

if __name__ == '__main__':
    print('9Game开测表-----------------------------------------------------')
    main()
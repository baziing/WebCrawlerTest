from pyquery import PyQuery as pq
import time
from alpa.main import Game

def input(url):
    doc = pq(url=url)
    gameList = doc('.box-text tr').items()
    for game in gameList:
        dictA = {}
        if game.find('.num').text() == '排名':
            continue
        dictA['input_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dictA['update_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dictA['source'] = '九游'
        dictA['name'] = game.find('.name a').text()
        dictA['href'] = 'https://www.9game.cn' + game.find('.name a').attr('href')
        dictA['label'] = game.find('.type').text()
        Game('gamedb', 'detail').input(dictA)

def main():
    input('https://www.9game.cn/xyrb/') # 新游
    # 预约
    for page in range(1, 8):
        print(page,'-----------------------------------------------------')
        input('https://www.9game.cn/xyqdb/' + str(page) + '_0/')

if __name__ == '__main__':
    print('9Game预约榜-----------------------------------------------------')
    main()
import pandas as pd
from model.TaptapDetail import *
from model.GameDB import Game
from model.TestDB import GameTest
import sys
import os

class Logger(object):
  def __init__(self, filename="Default.log"):
    self.terminal = sys.stdout
    self.log = open(filename, "a")
  def write(self, message):
    self.terminal.write(message)
    try:
        self.log.write(message)
    except Exception as e:
        print('error')
  def flush(self):
    pass

path = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
sys.stdout = Logger('log.txt')

def updateGameStatusByName(path):
    df = pd.read_csv(path, encoding='gbk')
    gamelist = df['name'].values.tolist()
    Game('gamedb', 'detail').outputfollow('name', gamelist).to_csv(time.strftime('%Y%m%d', time.localtime(time.time()))+'跟进状态更新-name.csv')

def updateGameStatusById(idList):
    Game('gamedb', 'detail').outputfollow('taptap_id',idList).to_csv(time.strftime('%Y%m%d', time.localtime(time.time()))+'跟进状态更新-id.csv')

def outputGameAdd(path):
    df = Game('gamedb', 'detail').output('input_time', '2021/10/01',path)
    df['label'] = df['label'].apply(lambda x: x.replace('\n', ' '))
    for i in range(0,2):
        print(i,df.loc[i,'name'])
        TDetail().loadName(df.loc[i,'name'])
    df = Game('gamedb', 'detail').output('input_time', '2021/10/01', path)
    df['label']=df['label'].apply(lambda x:x.replace('\n',' '))
    df.to_csv(time.strftime('%Y%m%d', time.localtime(time.time()))+'新增产品列表.csv',index=False)

def outputTestAdd(date):
    GameTest('gamedb', 'test').output('input_time', date).to_csv(time.strftime('%Y%m%d', time.localtime(time.time()))+'测试时间.csv', encoding='gbk', index=False)

if __name__ == '__main__':
    os.system("python ./code/TAPTAP发现v2.py")
    os.system("python ./code/TAPTAP榜单v2.py")
    os.system("python ./code/GameRes90天榜单.py")
    os.system("python ./code/GameRes开测表.py")

    # 输出新增产品
    print('输出新增产品列表-----------------------------------------------------')
    outputGameAdd('已入库.csv')
    # 输出测试时间
    print('输出新增测试表-----------------------------------------------------')
    outputTestAdd(str(time.strftime('%Y/%m/%d', time.localtime(time.time()))))
    # 更新根据产品的状态
    print('更新跟进游戏状态-----------------------------------------------------')
    updateGameStatusByName('跟进游戏列表.csv')






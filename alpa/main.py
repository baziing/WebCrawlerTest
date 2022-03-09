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
sys.stdout = Logger('更新失败.txt')

def updateGameStatusByName(path):
    df = pd.read_csv(path, encoding='gbk')
    gamelist = df['name'].values.tolist()
    Game('gamedb', 'detail').outputfollow('name', gamelist).to_csv(time.strftime('%Y%m%d', time.localtime(time.time()))+'跟进状态更新-name.csv')

def updateGameStatusById(idList):
    Game('gamedb', 'detail').outputfollow('taptap_id',idList).to_csv(time.strftime('%Y%m%d', time.localtime(time.time()))+'跟进状态更新-id.csv')

def outputGameAdd(path):
    # df = Game('gamedb', 'detail').output('input_time', '2021/10/01',path)
    # df['label'] = df['label'].apply(lambda x: x.replace('\n', ' '))
    # for i in range(0,df.shape[0]):
    #     print(i,df.shape[0],df.loc[i,'name'])
    #     if df.loc[i,'来源']!='TAPTAP':
    #         TDetail().loadName(df.loc[i, 'name'])
    #     elif 'tap' in df.loc[i,'href']:
    #         TDetail().loadUrl(df.loc[i, 'href'])
    df = Game('gamedb', 'detail').output('input_time', '2021/10/01', path)
    df['label']=df['label'].apply(lambda x:x.replace('\n',' '))
    df.to_csv(time.strftime('%Y%m%d', time.localtime(time.time()))+'新增产品列表.csv',index=False)
    df0= pd.read_csv(path).append(df[['name','href']],ignore_index=True)
    print(df0)
    df0.to_csv(time.strftime('%Y%m%d', time.localtime(time.time()))+'已入库.csv',index=False)


def outputTestAdd(date):
    GameTest('gamedb', 'test').output('input_time', date).to_csv(time.strftime('%Y%m%d', time.localtime(time.time()))+'测试时间.csv', encoding='gbk', index=False)

def updateAll():
    results=Game('gamedb','detail').outputAll('input_time','2021/01/01','update_time','2022/02/01','已入库.csv')

    # print(results)
    # for result in results:
    #     print(result['name'],result['input_time'],result['update_time'])
    i=0
    for result in results:

        print(i,results.count(),result['name'])
        if 'href' in result.keys() and 'tap' in result['href']:
            print('update')
            TDetail().loadUrl(result['href'])
        else:
            print('add')
            TDetail().loadName(result['name'])
        i=i+1


if __name__ == '__main__':
    # os.system("python ./code/TAPTAP发现v2.py")
    # os.system("python ./code/TAPTAP榜单v2.py")
    # os.system("python ./code/GameRes90天榜单.py")
    # os.system("python ./code/GameRes开测表v2.py")

    # 输出新增产品
    print('输出新增产品列表-----------------------------------------------------')
    # outputGameAdd('20220216已入库.csv')
    # 输出测试时间
    print('输出新增测试表-----------------------------------------------------')
    # outputTestAdd(str(time.strftime('%Y/%m/%d', time.localtime(time.time()))))
    # 更新根据产品的状态
    print('更新跟进游戏状态-----------------------------------------------------')
    # updateGameStatusByName('跟进游戏列表.csv')
    # updateGameStatusById([157487,158067,159368,191342])
    # updateAll()
    # TDetail().loadUrl('https://www.taptap.com/app/227514')
    # print(str.replace('（测试服）', ''))

    # TDetail().loadUrl('https://www.taptap.com/app/10569')

    TDetail().loadJson(18356)






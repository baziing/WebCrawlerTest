import requests
import random
from bs4 import BeautifulSoup
from alpa.model.GameDB import Game
import time
import json
import datetime
from alpa.model.TestDB import GameTest

null=''
uas = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",\
       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",\
       "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"]
colDict={'gameid':'gameres_id','gamename':'name','gameplay':'label','gamecompany':'yanfa','gamepublisher':'faxing','companys':'changshang',
         'taptapurl':'href','taptap_id':'taptap_id','review_rate':'gameres_score'}

def get_soup(url):
    headers = {'user-agent':get_ua()}
    res = requests.get(url,headers = headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    return soup

def get_ua():
    au = random.choice(uas)
    return au

def run():
    delta = datetime.timedelta(days=10)
    murl='https://www.16p.com/gamecenter/api/test_game_1?date='+str(datetime.date.today()-delta)
    msoup = str(get_soup(murl))
    msoup=str(msoup)[:str(msoup).rfind('}') + 1].replace('\\','').replace('\"bbcode-paragraph-br\"','').replace('\'\"','').replace('\"\'','').replace(' ','')\
        .replace('\",\"','|,?,?,|').replace('\":\"','|?,?,?|').replace('\"','\'')\
        .replace('|,?,?,|','\",\"').replace('|?,?,?|','\":\"').replace(',\'',',\"').replace('{\'','{\"').replace('\'}','\"}')\
        .replace('\':null','\":null').replace('\':{','\":{').replace('\':[','\":[').replace('\':','\":')
    try:
        mjson = json.loads(msoup, strict=False)
    except Exception as e:
        return
    dates=mjson['dates']
    for date in dates:
        for game in dates[date]:
            if game['game']['area']=='STEAM':
                continue
            input(game)
    return

def input(dictB):
    dictA = {}
    dictA['input_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
    dictA['update_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
    dictA['source'] = 'GameRes'
    dictA['test_time'] = dictB['testdate'].replace('-', '/')
    dictA['name']=dictB['game']['gamename']
    dictA['label']=dictB['game']['gameplay']
    dictA['test_name']=dictB['testtype']
    GameTest('gamedb', 'test').input(dictA)

    dictA = {}
    dictA['input_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
    dictA['update_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
    dictA['source'] = 'GameRes'
    dictA['name']=dictB['game']['gamename']
    dictA['label'] = dictB['game']['gameplay']
    dictA['yanfa']=dictB['game']['gamecompany']
    dictA['faxing']=dictB['game']['gamepublisher']
    dictA['changshang']=dictB['game']['companys'][0]['name']
    dictA['taptap_id']=int(dictB['game']['taptap_id'])
    dictA['href']='https://www.16p.com/'+dictB['game']['gameid']+'.html'
    Game('gamedb', 'detail').input(dictA)




if __name__ == '__main__':
    run()
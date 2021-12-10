import pandas as pd
from alpa.model.TaptapDetail import *
import requests
from bs4 import BeautifulSoup
import random
from alpa.model.GameDB import Game

df=pd.read_csv('跟进游戏列表.csv',encoding='gbk')
gamelist=df['name'].values.tolist()
# Game('gamedb', 'detail').addfollow('name',gamelist)
# Game('gamedb', 'detail').outputfollow('name',['关于我转生变成史莱姆这档事'])
Game('gamedb', 'detail').outputfollow('taptap_id',[191342])

# TDetail().loadUrl('https://www.taptap.com/app/227586')

# Game('gamedb', 'detail_copy1').output('input_time','2021/11/01').to_csv('ab.csv')


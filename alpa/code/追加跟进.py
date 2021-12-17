import pandas as pd
from alpa.model.TaptapDetail import *
import requests
from bs4 import BeautifulSoup
import random
from alpa.model.GameDB import Game

# df=pd.read_csv('跟进游戏列表.csv',encoding='gbk')
# gamelist=df['name'].values.tolist()
# Game('gamedb', 'detail').outputfollow('name',gamelist).to_csv('ab.csv')
# # Game('gamedb', 'detail').outputfollow('name',['关于我转生变成史莱姆这档事'])
# Game('gamedb', 'detail').outputfollow('taptap_id',[191342,157487]).to_csv('abb.csv')

# TDetail().loadUrl('https://www.taptap.com/app/227586')

# Game('gamedb', 'detail').output('input_time','2021/12/01').to_csv('输出.csv',encoding='gbk',index=False)

TDetail().loadName('绝对')

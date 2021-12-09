import pandas as pd
from alpa.model.TaptapUpdate import *

df=pd.read_csv('跟进游戏列表.csv',encoding='gbk')
gamelist=df['name'].values.tolist()
# Game('gamedb', 'detail').addfollow('name',gamelist)
# Game('gamedb', 'detail').outputfollow('name',gamelist).to_csv('abb.csv')

TUpdate().loadUrl('https://www.taptap.com/app/205597')

# Game('gamedb', 'detail_copy1').output('input_time','2021/11/01').to_csv('ab.csv')


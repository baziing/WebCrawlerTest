from alpa.main import *
from alpa.main import Game

# 跟进更新
# df=pd.read_csv('跟进游戏列表.csv',encoding='gbk')
# gamelist=df['name'].values.tolist()
# Game('gamedb', 'detail').outputfollow('name',gamelist).to_csv('跟进状态更新.csv')
# Game('gamedb', 'detail').outputfollow('name',['关于我转生变成史莱姆这档事'])
# Game('gamedb', 'detail').outputfollow('taptap_id',[191342,157487]).to_csv('跟进状态更新-id.csv')

# TDetail().loadUrl('https://www.taptap.com/app/227586')

# Game('gamedb', 'detail').output('input_time','2021/12/01').to_csv('输出.csv',encoding='gbk',index=False)

# TDetail().loadName('绝对')

# # 输出测试时间
# GameTest('gamedb', 'test').output('input_time','2021/12/01').to_csv('测试时间.csv',encoding='gbk',index=False)
# # 输出产品列表
# df=Game('gamedb', 'detail').output('input_time','2021/10/01')
# df['label']=df['label'].apply(lambda x:x.replace('\n',' '))
# df.to_csv('产品列表.csv',index=False)
# for i in range(126,df.shape[0]):
#     print(i,df.loc[i,'name'])
#     TDetail().loadName(df.loc[i,'name'])
# df=Game('gamedb', 'detail').output('input_time','2021/10/01')
# df['label']=df['label'].apply(lambda x:x.replace('\n',' '))
# df.to_csv('产品列表2.csv',index=False)

# 获取对应list的数据
df=pd.read_csv('../跟进游戏列表.csv', encoding='gbk')
gamelist=df['name'].values.tolist()
# print(gamelist)
df=Game('gamedb', 'detail').output('name',['2047'])
df['label']=df['label'].apply(lambda x:x.replace('\n',' '))
df.to_csv('完善1.csv')
# gamelist=df['name'].values.tolist()
# for i in range(0,df.shape[0]):
#     print(i,df.loc[i,'name'])
#     TDetail().loadName(df.loc[i, 'name'])

# TDetail().loadUrl('https://www.taptap.com/app/223137')
import os
import requests
import pandas as pd
import time

curtime=time.strftime('%Y%m%d',time.localtime(time.time()))

# 自动获取最近一次的表更新
dir='D:/neo/PYTHON/WebCrawlerTest'
files=os.listdir(dir)
filesList=files[:]
for file in files:
    if '汇率更新.csv' not in file or curtime in file:
        filesList.remove(file)
try:
    file=filesList[-1]
    print('上次更新文件：' + file)
except KeyError as ke:
    print(ke)

# 获取货币种类
path_currency='D:/neo/对账/汇率更新/谷歌货币.xlsx'
path_standard='基准汇率表.csv'
path_previous='基准汇率表.csv'
df_currency=pd.read_excel(path_currency)
df_standard=pd.read_csv(path_standard)
df_previous=pd.read_csv(path_previous).rename(columns={'rate':'rate_previous'})

# 获取汇率
url = 'https://v6.exchangerate-api.com/v6/7ee07e43eae90730744d24c7/latest/USD'
response = requests.get(url)
data = response.json()
dict_currency=data['conversion_rates']
df_currency['rate_now']=df_currency['currency'].apply(lambda x:dict_currency[x])

# 与标准的偏差值
df=pd.merge(df_standard,df_currency,on=['country','currency'])
df['偏差值']=(df['rate_now']/df['rate']-1)*100
df['偏差值']=df['偏差值'].apply(lambda x:str(x)+'%')

# 与上次结果的偏差值
df=pd.merge(df,df_previous,on=['country','currency'])
df['上期环比']=(df['rate_now']/df['rate_previous']-1)*100
df['上期环比']=df['上期环比'].apply(lambda x:str(x)+'%')
try:
    df.drop(columns='rate_previous')
except KeyError as ke:
    print(ke)

# 生成文档
df.to_csv(str(curtime)+'汇率更新.csv',index=False)
print('本次输出文件：'+str(curtime)+'汇率更新.csv')
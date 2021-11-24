import pandas as pd
import os
import requests
import time

path='C:/Users/NEO/Desktop/谷歌定价模版99.xlsx'

# 获取汇率
url = 'https://v6.exchangerate-api.com/v6/7ee07e43eae90730744d24c7/latest/USD'
response = requests.get(url)
data = response.json()
dict_currency=data['conversion_rates']

def getCol(x):
    if '%' in x:
        return '税'
    elif 'Existing price' in x:
        return '之前价格'
    elif '.' in x or ',' in x:
        return '更新价格'
    else:
        return '国家'

def getCurrency(x):
    if '%' in x:
        x=x[x.find('(')+1:x.rfind(')')].lstrip(' ').rstrip(' ')
        return x[:x.rfind(' ')]
    elif '.' in x or ',' in x:
        return x[:x.rfind(' ')].lstrip(' ').rstrip(' ')

def getAmount(x):
    if pd.isna(x):
        return
    if '.' in x or ',' in x:
        x=str(x)
        print(x)
        x=x[x.find(' ')+1:]
        print(x)
        return float(x.replace(',',''))
    return float(0)

def getRate(x):
    if pd.isna(x):
        return '-'
    if '%' in x:
        x=x[:x.find('%')+1]
        return x
    return '-'

def getTax(x):
    if pd.isna(x):
        return float(0)
    if '%' in x:
        x=x[x.find('(')+1:x.rfind(')')].lstrip(' ').rstrip(' ')
        return float(x[x.find(' '):].lstrip(' ').rstrip(' ').replace(',',''))
    return float(0)

def getNowRate(x):
    return dict_currency[x]*100

df=pd.DataFrame(pd.read_excel(path)['Local prices'])
df=df[~df['Local prices'].isin(['-'])].dropna()[5:].reset_index(drop=True)
df['col']=df['Local prices'].apply(lambda x:getCol(x))
df['Local prices']=df['Local prices'].apply(lambda x: x.lstrip('Existing price').lstrip(' ') if 'Existing price' in x else x)
df['币种']=df['Local prices'].apply(lambda x: getCurrency(x)).fillna(method='bfill')
result=pd.DataFrame(columns=['国家','币种','之前价格','更新价格','税率','税','税后价'])

j=0
currency=df.loc[0,'币种']
for i in range(0,df.shape[0]):
    if currency!=df.loc[i,'币种'] and df.loc[i,'col']=='国家':
        currency=df.loc[i,'币种']
        j=j+1
    if df.loc[i,'col']=='国家':
        result.loc[j,'币种']=df.loc[i,'币种']
    result.loc[j,df.loc[i,'col']]=df.loc[i,'Local prices']

result['之前价格']=result['之前价格'].apply(lambda x:getAmount(x))
result['更新价格']=result['更新价格'].apply(lambda x:getAmount(x))
result['税率']=result['税'].apply(lambda x:getRate(x))
result['税']=result['税'].apply(lambda x:getTax(x))
result['实时汇率']=result['币种'].apply(lambda x:getNowRate(x))
result['税后价']=round(result['更新价格']-result['税'],2)

result.to_csv('a.csv',index=False,encoding='gbk')
print(result)

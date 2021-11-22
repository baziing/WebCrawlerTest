import pymongo
import pandas as pd
import numpy as np

# detail={
#     'input_time':'2021/11/18',
#     'update_time':'2021/11/18',
#     'source':'TAPTAP',
#     'name':'1234ik',
#     'label':'音游',
#     'yanfa':'ndsadf',
#     'faxing':'edsadasda',
#     'changshang':'odasfafa',
#     'taptap_id':1234345,
#     'taptap_score':8.5,
#     'taptap_downloads':12366,
#     'taptap_follow':98,
#     'taptap_reserve':765,
#     'taptap_android':'下载',
#     'taptap_ios':'预约',
#     'gameres_id':12345,
#     'gameres_score':5.5,
#     'href':'www',
#     'remark':'接触'
# }
collectionsList=['input_time','update_time','source','name','label','yanfa','faxing','changshang',
                 'taptap_id','taptap_score','taptap_downloads','taptap_follow','taptap_reserve','taptap_android','taptap_ios'
                 'gameres_id','gameres_score','href','remark']
priorityDict={'TAPTAP':1,'GameRes':2,'九游':3}
list=[]

def dbconnect():
    client = pymongo.MongoClient(host='localhost')
    dblist = client.list_database_names()
    gamedb = client['gamedb']
    gamedetail = gamedb['detail']
    gametest = gamedb['test']
    return gamedb,gamedetail,gametest

def isExisting(cursor,query):
    # print(cursor.count_documents(dict))
    # doc =cursor.find(query)
    # for x in doc:
    #     print(x['input_time'])
    if 'name' not in query.keys():
        return -1
    if 'source' not in query.keys() or query['source'] not in priorityDict.keys():
        return -1
    query={'name':query['name']}
    return int(cursor.count_documents(query))

def update(cursor,dict):
    query={'name':dict['name']}
    x=cursor.find(query)[0]
    for key in dict:
        if priorityDict[x['source']]>priorityDict[dict['source']]:
            newquery = {'$set': {'source': dict['source']}}
            # print(newquery)
            cursor.update_one(query, newquery)
        if dict[key]!=x[key]:
            if x[key]==None or x[key]==0:
                newquery = {'$set': {key: dict[key]}}
                # print(newquery)
                cursor.update_one(query, newquery)
            elif x[key]!='' and dict[key]!='':
                # print(type(x[key]),x[key])
                if priorityDict[x['source']]>=priorityDict[dict['source']]:
                    newquery={'$set': {key: dict[key]}}
                    cursor.update_one(query, newquery)
    return

def printDetail():
    return

def main(i,detail):
    gamedb, gamedetail, gametest=dbconnect()
    # isExisting(gamedetail, {'$or':[{'taptap_id':1234},{'taptap_id':1234345}]})  # 多条件查询
    # dict={'taptap_id':1234,'label':'音游','name':'你别说','source':'GameRes'}    # 获取要录入的数据
    dict=detail
    if isExisting(gamedetail,dict)==0:
        gamedetail.insert_one(detail)
        print(i,'添加', dict['name'])
    elif isExisting(gamedetail,dict)==1:
        update(gamedetail,dict)
        print(i,'更新', dict['name'])
    elif isExisting(gamedetail,dict)==-1:
        print(i,'命名不规范',dict['name'])
        list.append(dict['name'])
    else:
        print(i,'多重命名输出，输出要存入的数据',dict['name'])
        list.append(dict['name'])


if __name__ == '__main__':
    df=pd.read_excel('/Volumes/通用/TAPTAP新品榜.xlsx')
    # print(df.shape[0])
    df['下载']=df['下载'].fillna(0)
    df['关注'] = df['关注'].fillna(0)
    df['预约'] = df['预约'].fillna(0)
    for i in range(0,df.shape[0]):
        detail={
            'input_time': str(df.loc[i,'input']),
            'update_time': str(df.loc[i,'update']),
            'source': str(df.loc[i,'来源']),
            'name': str(df.loc[i,'name']),
            'label': str(df.loc[i,'label']),
            'yanfa': str(df.loc[i,'开发']),
            'faxing': str(df.loc[i,'发行']),
            'changshang': str(df.loc[i,'厂商']),
            'taptap_id': int(df.loc[i,'id']),
            'taptap_score': str(df.loc[i,'评分']),
            'taptap_downloads': int(df.loc[i,'下载']),
            'taptap_follow': int(df.loc[i,'关注']),
            'taptap_reserve': int(df.loc[i,'预约']),
            'taptap_android': str(df.loc[i,'android']),
            'taptap_ios': str(df.loc[i,'ios']),
            'href': str(df.loc[i,'href']),
        }
        # print(detail)
        # print(detail['changshang'],detail['taptap_downloads'],type(detail['changshang']),type(detail['taptap_downloads']))
        main(i,detail)
    # main(detail)


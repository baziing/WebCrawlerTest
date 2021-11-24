import pymongo
import pandas as pd

class Game:
    collectionsList = ['input_time', 'update_time', 'source', 'name', 'label', 'yanfa', 'faxing', 'changshang',
                       'taptap_id', 'taptap_score', 'taptap_downloads', 'taptap_follow', 'taptap_reserve',
                       'taptap_android', 'taptap_ios','gameres_id', 'gameres_score', 'href', 'remark']
    priorityDict = {'TAPTAP': 1, 'GameRes': 2, '九游': 3,'暂无':100}
    EPSINON = 0.000001

    def __init__(self,dbname,tablename):
        self.client = pymongo.MongoClient(host='localhost')
        self.cursor=self.client[dbname][tablename]

    def input(self,dict):
        self.dict=dict
        if self.isExisting()==0:
            print('添加',self.dict['name'])
            self.cursor.insert_one(dict)
            return True
        elif self.isExisting()==1:
            print('更新',self.dict['name'])
            self.update()
            return True
        elif self.isExisting()==-1:
            print('数据格式不规范')
            print(self.dict)
            return False
        else:
            print('多重命名',self.dict['name'])
            return True

    def output(self,col,begin):
        colList=['input', 'id','来源', 'name','label', '开发', '发行','href','厂商','评分', '下载', '关注','android', 'ios']
        df = pd.DataFrame(columns=colList)
        dfDict={'input':'input_time','id':'taptap_id','来源':'source','name':'name','label':'label','开发':'yanfa',
                '发行':'faxing','href':'href','厂商':'changshang','评分':'taptap_score','下载':'taptap_downloads',
                '关注':'taptap_follow','android':'taptap_android','ios':'taptap_ios'}
        query={col:{'$gte':begin}}
        results=self.cursor.find(query)
        print(results)
        i=0
        for result in  results:
            for col in colList:
                if dfDict[col] not in result.keys():
                    continue
                else:
                    df.loc[i,col]=result[dfDict[col]]
            i=i+1
        return df


    def isExisting(self):
        if 'name' not in self.dict.keys():
            return -1
        if 'source' not in self.dict.keys() or self.dict['source'] not in self.priorityDict.keys():
            return -1
        for key in self.dict:
            if key not in self.collectionsList:
                print(key)
                return -1
        return int(self.cursor.count_documents({'name':self.dict['name']}))

    def update(self):
        query={'name':self.dict['name']}
        before=self.cursor.find(query)[0]
        for key in self.dict:
            # 入库时间不改变
            if key=='input_time':
                continue
            # 原先没有的字段
            if key not in before.keys():
                newquery = {'$set': {key: self.dict[key]}}
                self.cursor.update(query, newquery)
                continue
            # 本身字段为空
            if self.dict[key]==None or self.dict[key]==0 or self.dict[key]=='nan' or self.dict[key]=='暂无':
                continue
            if key in ['taptap_score']:
                if (float(self.dict[key])>=-self.EPSINON) and (float(self.dict[key]<=self.EPSINON)):
                    continue

            if str(self.dict[key])!=str(before[key]):
                # 原字段为空
                if key in ['taptap_score']:
                    if (float(before[key]) >= -self.EPSINON) and (float(before[key] <= self.EPSINON)):
                        newquery = {'$set': {key: self.dict[key]}}
                        self.cursor.update(query, newquery)
                        continue
                if before[key]=='' or before[key]==0 or before[key]==None or before[key]=='暂无':
                    newquery={'$set':{key:self.dict[key]}}
                    self.cursor.update(query,newquery)
                # 两个字段不匹配
                elif str(before[key])!='' and str(self.dict[key])!='':
                    if self.priorityDict[before['source']]>=self.priorityDict[self.dict['source']]:
                        newquery={'$set':{key:self.dict[key]}}
                        self.cursor.update(query,newquery)
            # 更新来源
            if self.priorityDict[before['source']]>self.priorityDict[self.dict['source']]:
                newquery={'$set':{'source':self.dict['source']}}
                self.cursor.update_one(query,newquery)
        return
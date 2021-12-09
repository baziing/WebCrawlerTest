import pymongo
import pandas as pd

class GameTest:
    collectionsList=['input_time', 'update_time','test_time','source','name','test_name','label','platform','remark']
    priorityDict = {'TAPTAP': 1, 'GameRes': 2, '九游': 3, '暂无': 100}
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

    def isExisting(self):
        if 'name' not in self.dict.keys() or 'input_time' not in self.dict.keys() or 'update_time' not in self.dict.keys():
            return -1
        if 'source' not in self.dict.keys() or self.dict['source'] not in self.priorityDict.keys():
            return -1
        for key in self.dict:
            if key not in self.collectionsList:
                print(key)
                return -1
        return int(self.cursor.count_documents({'name':self.dict['name'],'test_time':self.dict['test_time']}))

    def update(self):
        query = {'name': self.dict['name'],'test_time':self.dict['test_time']}
        before = self.cursor.find(query)[0]
        for key in self.dict:
            # 入库时间不改变
            if key=='input_time':
                continue
            # 原先没有的字段
            if key not in before.keys():
                newquery = {'$set': {key: self.dict[key],'update_time':self.dict['update_time']}}
                self.cursor.update(query, newquery)
                continue
            # 本身字段为空
            if self.dict[key] == None or self.dict[key] == 0 or self.dict[key] == 'nan' or self.dict[key] == '暂无' or self.dict[key] == '':
                continue

            if str(self.dict[key])!=str(before[key]):
                # 原字段为空
                if key in ['taptap_score']:
                    if (float(before[key]) >= -self.EPSINON) and (float(before[key] <= self.EPSINON)):
                        newquery = {'$set': {key: self.dict[key],'update_time':self.dict['update_time']}}
                        self.cursor.update(query, newquery)
                        continue
                if before[key]=='' or before[key]==0 or before[key]==None or before[key]=='暂无':
                    newquery = {'$set': {key: self.dict[key],'update_time':self.dict['update_time']}}
                    self.cursor.update(query,newquery)
                # 两个字段不匹配
                elif str(before[key])!='' and str(self.dict[key])!='':
                    if self.priorityDict[before['source']]>=self.priorityDict[self.dict['source']]:
                        newquery = {'$set': {key: self.dict[key],'update_time':self.dict['update_time']}}
                        self.cursor.update(query,newquery)

            # 更新来源
            if self.priorityDict[before['source']]>self.priorityDict[self.dict['source']]:
                newquery = {'$set': {key: self.dict[key],'update_time':self.dict['update_time']}}
                self.cursor.update_one(query,newquery)
        return

    def output(self,col,begin):
        colList = ['input','测试时间','source','name','测试名字','label','platform','备注']
        df = pd.DataFrame(columns=colList)
        dfDict = {'input':'input_time','测试时间':'test_time','source':'source','name':'name','label':'label','platform':'platform','备注':'remark','测试名字':'test_name'}
        query = {col: {'$gte': begin}}
        results = self.cursor.find(query).sort('test_time',-1)
        print(results)
        i = 0
        for result in results:
            for col in colList:
                if dfDict[col] not in result.keys():
                    continue
                else:
                    df.loc[i, col] = result[dfDict[col]]
            i = i + 1
        return df
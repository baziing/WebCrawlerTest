import pymongo
import pandas as pd

# 评分
# 休闲和恐怖 5000
class Game:
    collectionsList = ['input_time', 'update_time', 'source', 'name', 'label', 'yanfa', 'faxing', 'changshang',
                       'taptap_id', 'taptap_score', 'taptap_downloads', 'taptap_follow', 'taptap_reserve',
                       'taptap_android', 'taptap_ios','gameres_id', 'gameres_score', 'href', 'remark','network']
    labelList1=['三国','西游','战国','仙侠','武侠','修仙','街机','国风']  # 5000
    labelList2=['换装','模拟','竞速','益智','文字','种田','恋爱','音游','恐怖','赛车','解谜','烧脑','女性','女性向','教育','公益','消除','乙女'] #10000
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
        colList=['input', 'id','来源', 'name','label', '开发', '发行','href','厂商','评分', '下载', '关注','android', 'ios','GameRes评分']
        df = pd.DataFrame(columns=colList)
        dfDict={'input':'input_time','id':'taptap_id','来源':'source','name':'name','label':'label','开发':'yanfa',
                '发行':'faxing','href':'href','厂商':'changshang','评分':'taptap_score','下载':'taptap_downloads',
                '关注':'taptap_follow','android':'taptap_android','ios':'taptap_ios','GameRes评分':'gameres_score'}
        query={col:{'$gte':begin},} # 大于这个的日期
        results=self.cursor.find(query)
        # print(results)
        i=0
        for result in results:
            flag=True
            if 'taptap_follow' in result.keys() and 'label' in result.keys():
                mlist=result['label'].split(',')
                follow=int(result['taptap_follow'])
                for label in mlist:
                    if label in self.labelList1 and follow<=5000:
                        flag=False
                        break
                    if label in self.labelList2 and follow<=10000:
                        flag=False
                        break
            if flag==False:
                continue
            for col in colList:
                if dfDict[col] not in result.keys():
                    continue
                else:
                    df.loc[i,col]=result[dfDict[col]]
            i=i+1
        return df


    def isExisting(self):
        if 'name' not in self.dict.keys() or 'input_time' not in self.dict.keys() or 'update_time' not in self.dict.keys():
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
                newquery = {'$set': {key: self.dict[key],'update_time':self.dict['update_time']}}
                self.cursor.update(query, newquery)
                continue
            # 本身字段为空
            if self.dict[key]==None or self.dict[key]==0 or self.dict[key]=='nan' or self.dict[key]=='暂无' or self.dict[key]=='':
                continue
            if key in ['taptap_score']:
                if (float(self.dict[key])>=-self.EPSINON) and (float(self.dict[key]<=self.EPSINON)):
                    continue

            if str(self.dict[key])!=str(before[key]):
                # 原字段为空
                if key in ['taptap_score']:
                    print(before[key],type(before[key]))
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

    def addfollow(self,col,li):
        for item in li:
            if int(self.cursor.count_documents({col:item}))<=0:
                print(item,'数据不存在')
            elif int(self.cursor.count_documents({col:item}))>1:
                print(item,'有多条数据')
                query = {col:item}
                results = self.cursor.find(query)
                for result in results:
                    print(result)
            else:
                query = {col: item}
                newquery = {'$set': {'follow': 1}}
                self.cursor.update_one(query, newquery)
                print(item,'添加关注')
        return


    def deletefollow(self,col,li):
        for item in li:
            if int(self.cursor.count_documents({col:item}))<=0:
                print(item,'数据不存在')
            elif int(self.cursor.count_documents({col:item}))>1:
                print(item,'有多条数据')
                query = {col:item}
                results = self.cursor.find(query)
                for result in results:
                    print(result)
            else:
                query = {col: item}
                newquery = {'$set': {'follow': 0}}
                self.cursor.update_one(query, newquery)
                print(item,'删除关注')
        return

    def updatefollow(self,col,li):
        query = {'follow': 1}
        newquery = {'$set': {'follow': 0}}
        self.cursor.update_one(query, newquery)
        self.addfollow(col,li)
        return
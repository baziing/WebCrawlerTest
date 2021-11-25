from pyquery import PyQuery as pq
import time

page=1
while page in range(1,8):
    doc=pq(url='https://www.9game.cn/xyqdb/'+str(page)+'_0/')
    gameList=doc('.box-text tr').items()
    for game in gameList:
        dictA={}
        if game.find('.num').text()=='排名':
            continue
        dictA['input_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dictA['update_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        dictA['source']='九游'
        dictA['name']=game.find('.name a').text()
        dictA['href']='https://www.9game.cn'+game.find('.name a').attr('href')
        dictA['label']=game.find('.type').text()
        print(dictA)
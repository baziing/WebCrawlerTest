import requests
import random
from bs4 import BeautifulSoup
from alpa.model.GameDB import Game
import time

null=''
uas = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",\
       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",\
       "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"]
colDict={'gameid':'gameres_id','gamename':'name','gameplay':'label','gamecompany':'yanfa','gamepublisher':'faxing','companys':'changshang',
         'taptapurl':'href','taptap_id':'taptap_id','review_rate':'gameres_score'}

def get_soup(url):
    headers = {'user-agent':get_ua()}
    res = requests.get(url,headers = headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    return soup

def get_ua():
    au = random.choice(uas)
    return au


def main():
    page = 0
    m=0
    j=0
    while True:
        print(page,"-----------------------------------------------------")
        url = 'https://www.16p.com/gamecenter/api/new_game_list?p=' + str(page) + '&ps=20&date_range=90'
        soup=get_soup(url)
        context=str(soup)
        if context=='[]':
            break
        list0=context.split('{"gameid":')
        for i in range(0,len(list0)):
            list0[i]='{"gameid":'+list0[i]
            if 'gamename' in list0[i]:
                try:
                    mstr=list0[i].rstrip(',').rstrip(']</a></a></a></a>').rstrip(' ').replace('"gamedescription":','"gamedescription":[').replace(',"has_same_gamename"','],"has_same_gamename"')
                    str0=mstr[mstr.find('"gamedescription"')+len('"gamedescription"')+1:mstr.find(',"has_same_gamename"')]
                    mstr=mstr.replace(str0,'""')
                    dictB=eval(mstr)
                    input(dictB)
                except Exception as e:
                    print('error', list0[i].rstrip(','), '+++++++++++++++++++++')
                    j=j+1
            m=m+1
        page=page+1


def input(dictB):
    dictA={}
    dictA['source']='GameRes'
    for key in dictB.keys():
        if key in colDict.keys():
            if colDict[key] in ['GameRes_id','taptap_id']:
                dictA[colDict[key]]=int(dictB[key])
            elif colDict[key] in ['gameres_score']:
                dictA[colDict[key]] = float(dictB[key])
            elif colDict[key] in ['changshang']:
                dictA[colDict[key]]=dictB[key][0]['name']
            else:
                dictA[colDict[key]] = dictB[key]
    if 'label' in dictA.keys():
        strlabel=''
        for label in dictA['label']:
            if strlabel!='':
                strlabel=strlabel+','
            strlabel=strlabel+label
        dictA['label']=strlabel
    if 'href' not in dictA.keys():
        dictA['href']='https://www.16p.com/'+str(dictB['gameid'])+'.html'
    elif 'href' in dictA.keys() and dictA['href']=='':
        dictA['href'] = 'https://www.16p.com/' + str(dictB['gameid']) + '.html'
    else:
        dictA['href']=dictA['href'].replace('/', '').replace('\\', '/')
    dictA['input_time']=time.strftime('%Y/%m/%d', time.localtime(time.time()))
    dictA['update_time'] = time.strftime('%Y/%m/%d', time.localtime(time.time()))
    Game('gamedb', 'detail').input(dictA)
    return dictA


if __name__ == '__main__':
    print('GameRes90天榜单-----------------------------------------------------')
    main()

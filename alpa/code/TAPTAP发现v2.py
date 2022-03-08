import requests
import random
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import pandas as pd
from alpa.model.TaptapDetail import TDetail
import sys
import time

def get_soup(url):
    # user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56'
    # cookie='_uab_collina=163697383941465721317365; locale=zh_CN; tapadid=96394516-1882-4570-bdce-528a064420b5; discover_is_old_version=0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217d310432746ef-04f60e17277db5-561a1154-2073600-17d31043275982%22%2C%22%24device_id%22%3A%2217d310432746ef-04f60e17277db5-561a1154-2073600-17d31043275982%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%2C%22%24latest_referrer_host%22%3A%22cn.bing.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; tap_theme=light; _gid=GA1.2.912548099.1646102625; apk_download_url_postfix=/seo-baidu; acw_tc=276082a116461040735868525e265848611b7894fb7df0f131b45efe4a62fc; _ga_6G9NWP07QM=GS1.1.1646102625.94.1.1646105399.0; _gat=1; _ga=GA1.1.684186635.1637134734; XSRF-TOKEN=eyJpdiI6IlFvMjdUS2IwalVtMmpiYVRSXC9tdUJ3PT0iLCJ2YWx1ZSI6IkdQbFgzMXVDeStGaUFucU9XUE42OVUySnJMNFpVQUlTXC9VVmJvVFhoVkdyY01zSE1EcElZUVV1NklNUFUrbnZOenV4a05GMUxlZG9GdUcxaVlRRWdsQT09IiwibWFjIjoiYjFmYmI0YjgwYzNiZDM3M2RiMzZjNGE5NzYwMjZkZGQ2NWRhZmZkMmI3OGVjZTRiODQ5N2E2ODAzYWY3YzIwYyJ9; tap_sess=eyJpdiI6ImFURUVTSjQ5aHBFUkhxQ3FyOFRmUnc9PSIsInZhbHVlIjoiMjR6cVA1VER4ZkF5ZXpPRW5IazhwbzduUGlnWWxPS0tRZ21YT3pRK0pnUkdVM2p2cHZSZTlvZXRPS1Q1YWM0Z21SQWZnVk1LWFJSYUNBTHN1TU82c3c9PSIsIm1hYyI6IjYwYTQ2ODUxNTlmYWFkOTcyNzQyOWU3NjFiNjQ1NzE2ZDU2Mjg2MDdlNDdmZmM2NzhmOWQ0N2RkY2QxZTI1N2MifQ%3D%3D; ssxmod_itna=Yq+xg7D=KGqCqAIx0LeObD9mReDQiDuGQS=OGx05xneGzDAxn40iDt=ov07tB=D2uwWxqh2GXa4Zj4ourQb2nmpoDU4i8DCdeP=TDem=D5xGoDPxDeDA7qGaDb4Dr0xqGpnXvHNZ7DpxGrDlKDRx07/c5DWpIqhBr8RhPh/OYDnP+Ceii8D75Dux0Hie3mDDvAmSxzRpgIRQGqDBbxRbi4R9rYtDi3EQIG440OD0F+0EphRRIznxKXTQi4EYZeZ00eijbYe0G4zeRKaB2IYmDetG=xhj0DKmhYfk=K7DDW7k4x4D; ssxmod_itna2=Yq+xg7D=KGqCqAIx0LeObD9mReDQiDuGQS=ODnK84WKDseqQDLiu/SQL=NQBIQdujeUQATBDNUGAuu0+SQbGhdheD/4Bv8ADQIbDLxiQN4D='
    # headers = {'user-agent': get_ua()}
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.30'
    headers = {'user-agent': user_agent,
               'cookie': '_uab_collina=163697383941465721317365; locale=zh_CN; tapadid=96394516-1882-4570-bdce-528a064420b5; discover_is_old_version=0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217d310432746ef-04f60e17277db5-561a1154-2073600-17d31043275982%22%2C%22%24device_id%22%3A%2217d310432746ef-04f60e17277db5-561a1154-2073600-17d31043275982%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%2C%22%24latest_referrer_host%22%3A%22cn.bing.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; tap_theme=light; _gid=GA1.2.1390872645.1646721036; acw_tc=276077de16467350672614137e06c6f3ce7061772dcb9859e7335a32d8c5f0; _gat=1; _ga_6G9NWP07QM=GS1.1.1646735082.98.1.1646735083.0; _ga=GA1.1.684186635.1637134734; ssxmod_itna=YqRxBD0QG=0Q7qWq0dD=G7Iya1xUr42Bg24rqGXd3DZDiqAPGhDC84U3O8iobnqpXK8Y0TpYef3IjrP4AbzRueDHxY=DUc7GIPTDee=D5xGoDPxDeDAiqGaDb4DrXV4GPnUpT567Dpx0YDzqDgD7j/BqDfiqeeidtLKjX4xGUK+M+diqDMD7tD/3+N1eDBDaWeUdUdueIxlDDHKB47XA47HB+KlDGWirjDqeGuDG=esqL4h16lIMdzyE4WKA+otODqIY4a8B4qYA4YB0mQoDlYlYM37YxqK7GYRtwTRB4DGfx4jFqxD=; ssxmod_itna2=YqRxBD0QG=0Q7qWq0dD=G7Iya1xUr42Bg24xA6uAPqD/U8lDFOizcPrtXE6bz9TdqRGrjbN+H/cfFeOe8cBEQH3v1xxuEUzYkr63lfr0FW+cFA1Ad0osouH8EDcUG7FptgtPfcpbdfNfFfKjAS=RfRIvn+U9WW3HIr+mbdNOBob+bkQXfkEd2S=senUY/WWplxRMtxG2R4GcDiQeeD==; acw_sc__v3=62272ef967702ac2286b767df3943679b4bc2d52; XSRF-TOKEN=eyJpdiI6IjZScklreEtmRkpKK2pIc0ZFcGRVNXc9PSIsInZhbHVlIjoicXFVTVVwSlR4SFdsNU5DbXI1Q0p3WG5mb0xqZWZ1cVk2NG9JQ01zZVpSWXg4OVhsb01aYzFmSXVpNXZzK05EWWkxVXlMUWZaN2RWTHVpRVkrR0M4Umc9PSIsIm1hYyI6IjhiYTk2NjE3NjMxMzUzYjgxY2M0MjAwMTE2MjExZjhiODUwMzhjNDZiMjg3NDhhNDgyMTJhNGY4YTZkMWZhZjMifQ%3D%3D; tap_sess=eyJpdiI6IjI3RkxMMXowbkVaclVBak0xMTdcL21nPT0iLCJ2YWx1ZSI6IjVtdCtEa201bjVYbWlcL3JMRGRIY3JhSk5qcmdBZjY5blRmcmZKSjh6VU9ZQklOU201SDZiRTUxUDNHWE1qZlU4SGVQS01ENlV3ZEZiUVg4WjBQMDR6Zz09IiwibWFjIjoiYzI0YjYxMTY3NmI1NDdlZWZhMjdhMTJkZTEwN2ZjZmI0MzdmMzE0MTVkN2FmNDQ0ZThhZDdmNjY2MDM3MDYxNyJ9'}
    res = requests.get(url,headers = headers)
    print(res,url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    # print(soup)
    return soup

def get_ua():
    au = random.choice(uas)
    return au

class Logger(object):
  def __init__(self, filename="Default.log"):
    self.terminal = sys.stdout
    self.log = open(filename, "a")
  def write(self, message):
    self.terminal.write(message)
    try:
        self.log.write(message)
    except Exception as e:
        print('error')
  def flush(self):
    pass

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

df = pd.DataFrame(columns=['input','update','来源','id','name','评分','下载','关注','预约','label','开发','发行','厂商','android','ios','network','href'])
uas = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",\
       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",\
       "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"]

def run(find,page,end):
    while True:
        print('page' + str(page) + '-----------------------------------------------------')
        if find=='预约':
            if page == 0:
                murl = 'https://www.taptap.com/webapiv2/app-list/v1/detail?id=378&_trackParams=%7B%22refererLogParams%22:%7B%7D%7D&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D50%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC'
                # murl='https://www.taptap.com/webapiv2/app-top/v1/hits?type_name=reserve&platform=android&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D63%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3D28e54860-dfa0-4874-b6d0-433570e41dbe%26DT%3DPC%26OS%3DWindows%26OSV%3D10'
            else:
                murl = 'https://www.taptap.com/webapiv2/app-list/v1/detail?_trackParams=%7B%22refererLogParams%22%3A%7B%7D%7D&id=378&limit=10&from=' + str(
                    page * 10) + '&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D50%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC'
        elif find=='测试':
            if page == 0:
                murl = 'https://www.taptap.com/webapiv2/app-list/v1/detail?id=386&_trackParams=%7B%22refererLogParams%22:%7B%7D%7D&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D51%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC'
            else:
                murl = 'https://www.taptap.com/webapiv2/app-list/v1/detail?_boothInfo=%7B%22booth%22%3A%226380ff69_fdb81479%22%2C%22booth_id%22%3A%22251a4226e33e48a383b05730714b4035_6285fd916742407c8f1e9f5b8ec54911%22%2C%22booth_index%22%3A%222_8%22%7D&_trackParams=%7B%22refererLogParams%22%3A%7B%7D%2C%22rBoothInfo%22%3A%7B%22booth%22%3A%226380ff69_fdb81479%22%2C%22booth_id%22%3A%22251a4226e33e48a383b05730714b4035_6285fd916742407c8f1e9f5b8ec54911%22%2C%22booth_index%22%3A%222_8%22%7D%7D&id=386&limit=10&from=' + str(
                    page * 10) + '&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D51%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC'
        else:
            print(find,'输入格式不对')
            return
        msoup = get_soup(murl)
        mjson = json.loads(str(msoup))
        mlist = mjson['data']['list']
        if len(mlist) <= 0:
            break
        for game in mlist:
            strlabel = ''
            j = 0
            for tag in game['tags']:
                if j > 0:
                    strlabel = strlabel + ','
                strlabel = strlabel + tag['value']
                j = j + 1
            print(strlabel)
            if '单机' in strlabel:
                continue
            try:
                TDetail().loadUrl('https://www.taptap.com/app/' + str(game['id']))
            except Exception as e:
                print(e,'https://www.taptap.com/app/' + str(game['id']))
        page = page + 1
        if page>end:
            return


if __name__ == '__main__':
    sys.stdout = Logger('a.txt')
    try:
        print('TAPTAP最新预约-----------------------------------------------------')
        run('预约', 0,30)
    except Exception as e:
        options = webdriver.ChromeOptions()
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"')
        browser = webdriver.Chrome(chrome_options=options)
        browser.delete_all_cookies()
        # browser.add_cookie({'name': 'ABC', 'value': 'DEF'})
        # browser.execute_script(newwindow)
        browser.get(url='https://www.taptap.com/webapiv2/app-list/v1/detail?id=378&_trackParams=%7B%22refererLogParams%22:%7B%7D%7D&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D50%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dba0b05a1-43d9-47aa-9a41-06933353e0ad%26DT%3DPC')
        time.sleep(100)
        # # mbrowser.close()
        print(e)
        # run('预约', 0, 30)
    print('TAPTAP最新测试-----------------------------------------------------')
    run('测试',0,30)
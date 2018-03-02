'''
后续完善调转页面，等10分钟抓取等相关功能
'''

import requests
from bs4 import BeautifulSoup
import lxml
import random
import re
import sys

def userAgent():
    agent = ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
              'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
              'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)']

    kv = {}
    kv['user-agent'] = agent[random.randint(0, len(agent)-1)]
    return kv

def proxyIP():
    IP_Pool = ["https://112.250.65.222:53281",
               "https://110.52.8.155:53281",
               "https://114.113.126.82:80",
               "https://114.113.126.87:80",
               "https://121.237.139.35:3128"]
    pxyIP = {}
    pxyIP['https'] = IP_Pool[random.randint(0, len(IP_Pool)-1)]
    return pxyIP

def getHTML(url):
    try:
        kv = userAgent()
        IP = proxyIP()
        r = requests.get(url, headers=kv, timeout=30) #若是使用代理添加：proxies=proxyIP()
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        print("getHTML ERROR!")

def getRANK(url):
    if re.search('All', url,) != None:
        print('{:=^60}'.format('全部榜单'))
    elif re.search('ML',url) != None:
        print('{:=^60}'.format('内地榜单'))
    elif re.search('HT',url) != None:
        print('{:=^60}'.format('港台榜单'))
    elif re.search('US',url,) != None:
        print('{:=^60}'.format('欧美榜单'))
    elif re.search('KR',url,) != None:
        print('{:=^60}'.format('韩国榜单'))
    else:
        print('{:=^60}'.format('日本榜单'))
    matchs = []
    html = getHTML(url)
    soup = BeautifulSoup(html, 'lxml')
    rank = soup.find_all('li', class_='vitem J_li_toggle_date ')
    for li in rank:
        match = {}
        match['mvname'] = li.find(class_='mvname').text
        match['mvauthor'] = li.find(class_='special').text
        match['time'] = li.find(class_='c9').text
        match['top_num'] = li.find('div', class_='top_num').text
        if li.find('h3', class_='desc_score'):
            match['score'] = li.find('h3', class_='desc_score').text
        else:
            match['score'] = li.find('h3', class_='asc_score').text
        matchs.append(match)
        print(match)
    return matchs

def saveTXT(datas):
    with open('D:/git/code/YinYueTaiBangDan.txt', 'a', encoding='utf-8' ) as f:
        for data in datas:
            f.write('单曲名称：{} 歌手：{} 发行时间：{} 单曲排名：{} 排行榜得分：{}\n'
                    .format(data['mvname'],data['mvauthor'],data['time'],data['top_num'],data['score']))

def urlPOOL(url):
    url_pool = []
    html = getHTML(url)
    soup = BeautifulSoup(html, 'lxml')
    category = soup.find_all('a', class_=re.compile('J_area'))
    for cate in category:
        url_pool.append(cate['data-area'])
    return url_pool

def main(top_list):
    base_url = 'http://vchart.yinyuetai.com/vchart/trends'
    url_poll = urlPOOL(base_url)
    for i in url_poll:
        url = base_url + '?area=' + i
        if top_list != None:
            if top_list <= 20:
                url_add = url + '&page=1'
                rank_list = getRANK(url_add)
            elif top_list <= 40:
                url_add = url + '&page=2'
                rank_list = getRANK(url_add)
            elif top_list <= 50:
                url_add = url + '&page=3'
                print(url_add)
                rank_list = getRANK(url_add)
            else:
                continue
        else:
            rank_list = getRANK(url)
        print(url or url_add)
        saveTXT(rank_list)
    print('爬取完毕')



if __name__ == '__main__':
    top_input = int(input('请输入想关注的排名只能取整数20/40/50:'))
    main(top_input)



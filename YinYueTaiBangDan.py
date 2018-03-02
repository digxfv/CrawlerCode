import requests
from bs4 import BeautifulSoup
import lxml
import random

def userAgent():
    agent = ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
              'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
              'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)']

    kv = {}
    kv['user-agent'] = agent[random.randint(0, len(agent))]
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
    html = getHTML(url)
    soup = BeautifulSoup(html, 'lxml')
    rank = soup.find_all('li', class_='vitem J_li_toggle_date ')
    for li in rank:
        match = {}
        match
    return rank

def saveTXT():
    pass

def main():
    url = 'http://vchart.yinyuetai.com/vchart/trends'
    print(getRANK(url))


if __name__ == '__main__':
    main()


'''
爬取豆瓣网排名TOP250的电影，
并存入txt文档
版本：v1.0
'''
import requests
from bs4 import BeautifulSoup
import lxml
import re
import os

def getHTML(url):
    kv = {'user-agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=kv, timeout=30)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    #print(r.encoding)
    return r.text

def getDianying(url):
    contents = []
    html = getHTML(url)
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('div', id='content').h1.string #获取主题名称
    #获取电影名称、主演、简介、上映时间等
    wrap = soup.find_all('div',class_='info')

    for a in wrap:
        content = {}
        content['name'] = a.find('a').text.replace('\n','').replace('\xa0','').replace(' ','')
        content['intro'] = a.find('p').text.replace('\n','').replace('...','').replace(' ','')\
                           .replace('\xa0','')
        content['rating_num'] = a.find(class_='rating_num').text
        content['comment'] = a.find(text=re.compile("评价")).string
        content['dianping'] = a.find(class_='inq').text
        contents.append(content)
    #print(contents)
    return contents

    # intro =
    #intro = intro.split('\xa0')
    #print(wrap)


#将字典内容保存到TXT文件内
def saveTXT(attrs):
    if not os.path.exists('D:/git/code'):
        os.mkdir('D:/git/code')
    with open('D:/git/code/douban_TOP250.txt', 'a+', encoding='utf-8') as f:
        for txt in attrs:
            f.write('电影名称：{:<} 电影豆瓣评分：{:<} 评论人数：{:<} \n电影简述：{:<} \n电影一句话点评：{:<}\n'
                    .format(txt['name'],txt['rating_num'],txt['comment'],txt['intro'],txt['dianping']))
            print(' 抓取完毕===> 电影名称：{}\t'.format(txt['name']))


def main():
    base_url = 'https://movie.douban.com/top250'
    page = 10
    next_page =[]
    with open('D:/git/code/douban_TOP250.txt', 'w', encoding='utf-8') as f:
        f.write('{:=^60}\n'.format("豆瓣电影TOP250"))

    print("{:=^60}".format('豆瓣电影TOP250'))
    for i in range(0, page):
        next_page.append(base_url + '?start=' + str(25 * i) + '&filter= ')
    for url in next_page:
        Dianying = getDianying(url)
        saveTXT(Dianying)
    print()
    print('电影共{}部'.format('250'),'爬取完毕')

if __name__ == '__main__':
    main()


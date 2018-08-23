#! -*- coding:utf-8 -*-
# get bilibili.com offline video file urls
from __future__ import print_function
import json
import requests
import re
import argparse


class bilibili_saver:
    def __init__(self,cookie):
        self.cookie = cookie
        self.headers = {
            'Host': 'api.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
            #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            #'Referer': 'http://api.bilibili.com/',
            'Cookie': self.cookie,
            'Connection': 'keep-alive'
        }

        self.headers2 = {
            'Host': 'www.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Referer': 'http://api.bilibili.com/',
            'Cookie': self.cookie,
            'Connection': 'keep-alive'
        }
    def get_pages(self,avid):
        pageurl = 'https://www.bilibili.com/video/av' + str(avid)
        print(pageurl)
        r = requests.get(pageurl, headers=self.headers2)
        #print(r.text)
        #html = etree.HTML(source)
        #titles = html.xpath('//*[@class="list-group-item"]')
        #pages = len(titles)


    def get_url(self, aid,pages):
        urlfiles =[]
        with open(str(aid) + '_url.txt', 'w') as f:
            with open(str(aid) + '_log.txt', 'w') as f2:
                for i in range(pages):
                    url='https://api.bilibili.com/playurl?callback=cb&aid={}&page={}&platform=html5&quality=1&vtype=mp4&type=jsonp&cb=cb&_=0'.format(aid,i+1)
                    r = requests.get(url, headers=self.headers)
                    jsoncode = r.text[r.text.find('(') + 1:r.text.find(')')]
                    print(i, r.text,jsoncode)

                    jsoncode = json.loads(jsoncode)

                    durl=jsoncode['durl'][0]['url']
                    pattern = re.compile("\/(.*?\.mp4)")
                    filename = ''.join(re.findall(pattern, durl[durl.rfind('/'):]))
                    print(i+1,filename, durl)
                    f.write(durl+'\n')
                    f2.write("{},{}\n".format(i + 1, filename))
                    urlfiles.append([filename,durl])
        return  urlfiles

    def download_mp4(self,url,filename):
        print('start download....',filename,url)
        r = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(r.content)
        print('end download....')


if __name__ == '__main__':
    #填入自己截获到的cookies
    parser = argparse.ArgumentParser(description='command line for bilibili_downloader ')
    parser.add_argument('-c', '--cookie', default='', type=str, help='cookies after login the sites')
    parser.add_argument('-a', '--avid', required=True, type=int, help='the video id to be download')
    parser.add_argument('-n', '--avnums', default=1, type=int, help='the video numbers')
    parser.add_argument('-d', '--download', default=False, type=bool, help='down the mp4 file with python,may be slow,recommend use bittorrent tools such as thunder,bitcomet')

    #my cookie from F12
    c1 ='buvid3=660B5812-D5E7-4980-B7C1-91CB484AC8FD13290infoc; LIVE_BUVID=AUTO5415313161426619; rpdid=kxxkkipolqdoskokoxoww; fts=1533376654; finger=49387dad; sid=huhkto4h; DedeUserID=356354602; DedeUserID__ckMd5=499d516cee3357ef; SESSDATA=8ad2ad72%2C1536647697%2C470f3ede; bili_jct=4484433855aa2d61c92b640b67b260f5; UM_distinctid=1652cddfff611-072f10db1de971-1f2a1709-1fa400-1652cddfff81b; _dfcaptcha=4c6dc7e592fe7e7c8f262e23b4255a8d; CNZZDATA2724999=cnzz_eid%3D7504664-1534054315-https%253A%252F%252Fwww.ibilibili.com%252F%26ntime%3D1534070515'
    c2 ='buvid3=660B5812-D5E7-4980-B7C1-91CB484AC8FD13290infoc; LIVE_BUVID=AUTO5415313161426619; rpdid=kxxkkipolqdoskokoxoww; fts=1533376654; finger=49387dad; sid=huhkto4h; DedeUserID=356354602; DedeUserID__ckMd5=499d516cee3357ef; SESSDATA=8ad2ad72%2C1536647697%2C470f3ede; bili_jct=4484433855aa2d61c92b640b67b260f5; UM_distinctid=1652cddfff611-072f10db1de971-1f2a1709-1fa400-1652cddfff81b; _dfcaptcha=4c6dc7e592fe7e7c8f262e23b4255a8d'

    c3='buvid3=660B5812-D5E7-4980-B7C1-91CB484AC8FD13290infoc; LIVE_BUVID=AUTO5415313161426619; rpdid=kxxkkipolqdoskokoxoww; fts=1533376654; finger=49387dad; sid=huhkto4h; DedeUserID=356354602; DedeUserID__ckMd5=499d516cee3357ef; SESSDATA=8ad2ad72%2C1536647697%2C470f3ede; bili_jct=4484433855aa2d61c92b640b67b260f5; UM_distinctid=1652cddfff611-072f10db1de971-1f2a1709-1fa400-1652cddfff81b'

    args = parser.parse_args()

    bbd =bilibili_saver(cookie=args.cookie)

    #aid=27418372
    #aid = 24011528#fly51fly
    #aid=23316535#fly51fly
    #bbtest.get_pages(aid)


    #bbtest.get_url(24011528,10)
    #bbtest.get_url(23316535, 10)
    urls = bbd.get_url(args.avid, args.avnums)

    if args.download == True:
        for f, u in urls:
            bbd.download_mp4(u,f)
    #bbtest.get_url(17204303, 35)





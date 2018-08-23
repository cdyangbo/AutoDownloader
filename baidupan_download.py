#! -*- coding:utf-8 -*-
# 本模块用来离线下载资源到网盘
import urllib
import json
import requests




class bdsaver:
    def __init__(self,cookie):
        self.cookie = cookie
        self.headers = {
            'Host': 'pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'https://pan.baidu.com/',
            'Cookie': self.cookie,
            'Connection': 'keep-alive'
        }

    # 登录需要POST一个包，其中包含帐号信息的Cookie
    def login(self):
        self.loginurl="https://pan.baidu.com/disk/home"
        try:
            #req = urllib.request.Request(self.loginurl, headers=self.headers)
            sourcecode = requests.get(self.loginurl, headers=self.headers)#urllib.request.urlopen(req)
        except Exception as e:
            print('Error ', str(e))
        else:
            #如果出现该字眼说明登录成功
            #htmlcode=(sourcecode.read().decode())
            print(sourcecode.text)
            if(sourcecode.text.find('initPrefetch')!=-1):
                print('login OK!')
    def query(self,magneturl):
        self.magneturl=magneturl
        self.headers = {
            'Host': 'pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://pan.baidu.com/disk/home?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0',
            'Cookie': self.cookie,
            'Connection': 'keep-alive',
            'Pragma': 'no - cache',
            'Cache - Control': 'no - cache',
        }

        self.queryurl = 'https://pan.baidu.com/rest/2.0/services/cloud_dl?channel=chunlei&web=1&app_id=250528&clienttype=0'
        self.data ={
            'method': 'query_magnetinfo',
            'app_id': '250528',
            'source_url':self.magneturl ,
            'save_path': '/',
            'type': '4'
        }
        #req = urllib.request.Request(self.queryurl, headers=self.headers, data=urllib.parse.urlencode(self.data).encode(encoding='UTF8') )
        sourcecode = requests.post(self.queryurl, headers=self.headers, data=self.data)#urllib.urlencode(self.data).encode(encoding='UTF8'))#urllib.request.urlopen(req)

        result=sourcecode.text #(sourcecode.read().decode('unicode_escape'))
        print(result)
        result=json.loads(result)['magnet_info']
        print(result)
        download_list=''
        for i in range(len(result)):
            #文件大于50MB
            if (int(result[i]['size'])>1024*1024*50):
                download_list=download_list+str(i+1)+','
        if download_list!='':
            return download_list
        else:
            return '1'
    def save(self,selidx):
        # self.queryurl = 'http://pan.baidu.com/rest/2.0/services/cloud_dl?channel=chunlei&web=1&app_id=250528&bdstoken=efbd0c8c5eb658ea804bea857c9ad213&clienttype=0'
        self.queryurl = 'https://pan.baidu.com/rest/2.0/services/cloud_dl?channel=chunlei&web=1&app_id=250528&clienttype=0'
        self.data = {
            'method': 'add_task',
            'app_id': '250528',
            'save_path': '/',
            'selected_idx': selidx,
            'task_from': '1',
            'source_url':self.magneturl ,
            # 't':'1501251100480'
        }
        #req = requests(self.queryurl, headers=self.headers,
        #                             data=urllib.parse.urlencode(self.data).encode(encoding='UTF8'))
        #sourcecode = urllib.request.urlopen(req)
        sourcecode = requests.post(self.queryurl, headers=self.headers,data=self.data)
        print(sourcecode.text)



if __name__ == '__main__':
    #填入自己截获到的cookies




    bdtest = bdsaver(cookie='Cookie:PANWEB=1; BDUSS=EZyMUZqVzNpNHNZdzVQYX5ocUVtTFJlanBBYXlWNVFrblJpS3BreUJTNFJUMFphQVFBQUFBJCQAAAAAAAAAAAEAAACbCecwY2R5YW5nYm8xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABHCHloRwh5ab; BAIDUID=BF153ABE1741C52DE72A37436ADBF013:FG=1; SCRC=f487ca173eda9ff96ced7b44731092dc; STOKEN=de8950e3b3166f864893c437276709a0a84b21fe3c6bcfc17ed111c6af143a9f; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1534061429; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1534061999; cflag=15%3A3; PANPSC=10759339190935928315%3A0tGXwXye%2FVjEYIhe3fZC3aKNhhpNSelHhKI8piuds8hKu8WyLCLL4Xk2o4wklodwO1WCEUI1d7gHJi1y4oSlv5LJbanjqcxlb4g8ZGlzcSs9CJq%2BpSvvwtLup%2BRooU6XtU%2FgH9WYvpljbYml1eowNq7IJzS%2Fi2HLfbZ%2FbYW506b%2ByIluCYs1Wp2Zb97G3%2BgS')
    bdtest.login()



    dllist=bdtest.query(magneturl='magnet:?xt=urn:btih:459E0DD6DCE56845BE3C72368797481F0B8C0216&xl=3391547763&dn=%E7%94%9F%E5%8C%96%E5%8D%B1%E6%9C%BA%E7%B3%BB%E5%88%97%E4%B8%89%E9%83%A8+%E7%94%9F%E5%8C%964%E9%A2%84%E5%91%8A%E7%89%87')

    print(dllist)

    bdtest.save(dllist)


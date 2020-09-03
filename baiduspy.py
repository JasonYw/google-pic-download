from http.client import responses
from os import times
from threading import TIMEOUT_MAX
import requests
from bs4 import BeautifulSoup
import urllib
from requests.sessions import session 
import json
import urllib.request
import sys
import os
import time
import re
import threading
from queue import Queue
import socket
socket.setdefaulttimeout(5)
class Crawljson():
    def __init__(self,key,page=100):
        self.key =key
        self.page =int(page)
        self.session =requests.session()
        self.headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        }
        self.imagelist=[]
        self.path ='baidu_'+self.key+'_img'
        self.count =0
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def run(self):
        if self.page >0:
            for i in range(1,self.page+1):
                if not self.geturl(i):
                    print("无法获取多余的图像地址")
                    break
        self.imagelist =list(set(self.imagelist))
        self.totallink =len(self.imagelist)
        print('finding img_link:',self.totallink)
        if len(self.imagelist):
            for i in self.imagelist:
                self.Downloader(i)
        else:
            print('no page')
        
        '''
            add thread
        '''
        # Downloadthreadname =['Download1','Download2','Download3','Download4','Download5']
        # linkqueue =Queue()
        # junk_Downloadthreadnamelist=[]

        # for i in self.imagelist:
        #     linkqueue.put(i)
        
        # while not linkqueue.empty():
        #     for i in range(0,5):
        #         try:
        #             link =linkqueue.get(False)
        #             thread =threading.Thread(target=self.Downloader,args=(link,))
        #             thread.start()
        #             #thread.join()
        #         except Exception as e:
        #             break
    
  

    def geturl(self,page):
        print('Crawling page:',page)
        page =(page-1)*30
        queryWord =urllib.parse.urlencode({'queryWord':self.key}).upper().replace('QUERYWORD','queryWord')
        word =urllib.parse.urlencode({'word':self.key}).upper().replace('WORD','word')
        url ='https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&is=&fp=result&'+queryWord+'&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&'+word+'&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn='+str(page)+'&rn=30'
        print('linking:',url)
        response =self.session.get(url,headers=self.headers)
        time.sleep(1)
        try:
            tempimagelist =re.findall(r'"thumbURL":"\S+","middleURL"',response.text)
            print("downloadurl num:",len(tempimagelist))
            if len(tempimagelist) ==0:
                return False
            if len(tempimagelist):
                for i in tempimagelist:
                    downloadurl =i.replace('"thumbURL":"','').replace('","middleURL"','')
                    print("fining",downloadurl)
                    self.imagelist.append(downloadurl)
            print('success linking',url)
        except  Exception as e:
            print(e)
        return True
    
    def Downloader(self,url):
        path =self.path+'/'+self.key+'_'+str(self.count)+'.jpg'
        try:
            urllib.request.urlretrieve(url=url,filename=path,reporthook=self.downloadinform,data=None)
            print('downloading img',self.count+1,'/',self.totallink)
        except Exception as e:
            print(e)
        self.count =self.count+1
        

    def progressbar(self,cur):
        total =100
        percent = '{:.2%}'.format(cur / total)
        sys.stdout.write('\r')
        sys.stdout.write("[%-100s] %s" % ('=' * int(cur), percent))
        sys.stdout.flush()
    
    def downloadinform(self,blocknum, blocksize, totalsize):
        percent =int((blocknum*blocksize) / totalsize)
        if percent >1:
            percent =1.0
        percent = percent * 100
        self.progressbar(percent)


def main(key):
    if key !=None:
        Crawl =Crawljson(key,'10')
        Crawl.run()
    else:
        print('baiduspy:缺少关键字')

def readconfig():
    key_list=[]
    with open('example-config.json','r',encoding='utf-8',errors='ignore') as f:
        for line in f.readlines():
            content =json.loads(line)
            key_list.append(content['key'])
    return key_list

if __name__ =="__main__":
    pass


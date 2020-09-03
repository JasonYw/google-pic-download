import requests
import time
from bs4 import BeautifulSoup
import urllib
from requests.sessions import session 
import json

class Crawljson():
    def __init__(self,key,page):
        self.key =key
        self.session =requests.session()
        self.headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        }
        self.imagelist=[]
        self.page =int(page)
    
    def run(self):
        if self.page ==0:
            print('no page')
        if self.page ==1:
            self.getindexurl()
        if self.page >1:
            self.getindexurl()
            for i in range(2,self.page+1):
                self.geturl(i)
        for i in self.imagelist:
            print(i)

    
    def getindexurl(self):
        fmq ='fmq='+str(time.time())[:14].replace(".",'')+'_R'
        word ='word='+self.key
        url ='https://image.baidu.com/search/index?tn=baiduimage&ipn=r&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&'+'fmq+&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&sid=&'+word
        print(url)
        response =self.session.get(url=url,headers=self.headers)
        soup = BeautifulSoup(response.text,'html.parser')
        imagelist =soup.findAll('img',class_='main_img img-hover')
        print(len(imagelist))
        for img in imagelist:
            img_url =img['src']
            print(img_url)
            self.imagelist.append(img_url)

    def geturl(self,page):
        queryWord =urllib.parser.urllib({'queryWord:'+self.key})
        word =urllib.parser.urllib({'word:'+self.key})
        url ='https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&is=&fp=result&'+queryWord+'&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&'+word+'&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn='+int(page)+'&rn=30'
        response =self.session.get(url,headers=self.headers)
        jsondata =json.loads(response.text)
        try:
            data =jsondata['data']
            if len(data):
                for i in data:
                    self.imagelist.append(i)
        except  Exception as e:
            print(e)

def main():
    Crawl =Crawljson('nba','1')
    Crawl.run()

    
if __name__ =="__main__":
    main()

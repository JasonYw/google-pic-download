from functools import total_ordering
import progressbar
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup 
import urllib
import urllib.request
import os
import json
import sys

def readconfig():
    key_list=[]
    with open('example-config.json','r',encoding='utf-8',errors='ignore') as f:
        for line in f.readlines():
            content =json.loads(line)
            key_list.append(content['key'])
    return key_list

class Crawlhtml():

    def __init__(self,key):
        self.key =key
        self.filepath =self.key+'_img'
        self.filename =self.get_html()
        if not os.path.exists('google_html'):
            os.mkdir('google_html')
        if not os.path.exists(self.filename):
            print('can not find',self.filename)
        else:
            if not os.path.exists(self.filepath):
                os.mkdir(self.filepath)
 
    def run(self):
        html =self.readhtml()
        self.downloadimg(html)


    def get_html(self):
        q =urllib.parse.urlencode({'q':self.key}).upper().replace('Q=','q=')
        oq =urllib.parse.urlencode({'oq':self.key}).upper().replace('OQ=','oq=')
        htmlpath ='google_html/'+self.key+".html"
        url ='https://www.google.com.hk/search?'+q+'&tbm=isch&ved=2ahUKEwiW-aruu8rrAhWXB94KHVw0AlcQ2-cCegQIABAA&'+oq+'&gs_lcp=CgNpbWcQAzICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCABQugVYiRlggB9oAHAAeAGAAd0CiAGoDpIBBTItNi4xmAEAoAEBqgELZ3dzLXdpei1pbWewAQDAAQE&sclient=img&ei=ZY9PX9ayD5eP-Abc6Ii4BQ&bih=1089&biw=1920&safe=strict&hl=zh-CN'
        print('target:',url)
        chrome_options =Options()
        chrome_options.add_argument('--headless')
        driver =webdriver.Chrome(chrome_options=chrome_options)
        #driver =webdriver.Chrome()
        driver.get(url)
        while True:
            ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(1)
            try:
                driver.find_element_by_css_selector('[value="显示更多搜索结果"]').click()
                print('click more')
            except:
                break #测试用
                pass
            try:
                driver.find_element_by_css_selector('[data-status="3"]').click()
                print('finishing find element')
                break
            except:
                pass
            print('page down')
        html =driver.page_source
        driver.close()

        try:
            with open(htmlpath,'w',errors='ignore') as f:
                f.write(html)
            return htmlpath
        except Exception as e:
            print(e)

    def readhtml(self):
        with open(self.filename,'r',encoding='utf-8',errors='ignore') as f:
            html =f.read()
            return html

    def progressbar(self,cur):
        total =100
        percent = '{:.2%}'.format(cur / total)
        sys.stdout.write('\r')
        # sys.stdout.write("[%-50s] %s" % ('=' * int(math.floor(cur * 50 / total)),percent))
        sys.stdout.write("[%-100s] %s" % ('=' * int(cur), percent))
        sys.stdout.flush()
    
    def downloadinform(self,blocknum, blocksize, totalsize):
        percent =int((blocknum*blocksize) / totalsize)
        if percent >1:
            percent =1.0
        percent = percent * 100
        self.progressbar(percent)

    def downloadimg(self,html):
        soup =BeautifulSoup(html,'html.parser')
        imagelist =soup.findAll('img',class_='rg_i Q4LuWd')
        totallink =len(imagelist)
        print('finding img_link:',totallink)
        count =0
        for img in imagelist:
            try:
                path = self.filepath+'/'+self.key+'_'+str(count)+'.jpg'
                urllib.request.urlretrieve(url=img['src'],filename=path,reporthook=self.downloadinform,data=None)
                print('downloading img',count+1,'/',totallink)
                time.sleep(1)
                count =count+1
            except Exception as e:
                print(e)
        print('finishing download')

def main():
    keylist =readconfig()
    if len(keylist):
        for key in keylist:
            print('parseing:',key)
            crawl =Crawlhtml(key)
            crawl.run()
    else:
        print('example-config配置文件无关键词')

if __name__ == '__main__':
    main()

使用方法：
    在example-config中配置好图片关键字
    在当前目录下,cmd中输入指令setup.py运行程序
    下载好的图片会放在当前目录下
    使用google爬取图片，需要代理
    百度默认爬取前100个json数据包,以后会开放页数接口

配置文件写法：
    1.同时使用百度与google
        {'key':'关键字'}
    2.只使用百度
        {'key':'关键字','spider':'baidu'}
    3.只是用google
        {'key':'关键字','spider':'google'}

    例子
        {"key":"apple","spider":"baidu"}
        {"key":"bear","spider":"google"}
        {"key":"nab"}
        使用百度爬取关键字为apple的图片
        使用google爬取关键字为bear的图片
        使用百度与谷歌同时爬取nba的图片

配置环境：
    pip install selenium 
    pip install bs4

安装chrome无头浏览器
    根据chrome版本去找对应版本 https://chromedriver.storage.googleapis.com/index.html
    下载完成后，放在chrome根目录下，并加入环境变量

待完善
    给百度的下载器加入多线程
    自动配置环境
    开放百度页数接口
    开放配置文件接口

#延迟申请时间
import time
#用队列暂时存储信息
from queue import Queue
from core.apple_crawl import Spider
from core.tread_crawl import TreadCrawl
from conf.settings import xpath_class
from core.tread_parse import ThreadParse

class  MySpider(Spider):
    #继承自己写好的爬虫对象，方面调用共有方法
    def __init__(self):
        super(MySpider,self).__init__()

    #执行程序的代码
    def start(self):
        # 获取第二层网址:app分类网站
        html = self.get_html('https://itunes.apple.com/id/genre/ios/id36?mt=8')
        xpath = "//div[@class='grid3-column']/ul/li/a/@href"
        url_list = self.find_url(xpath, html)
        #print(url_list[0])

        # 获取第二次网站里每个app的地址
        for url in url_list:
            appQueue = self.get_queue(url)
            global appQueue

        threadcrawl = []
        crawlList = ["采集线程1号", "采集线程2号", "采集线程3号"]
        #此处写3个线程去爬每个分类中取近150个app返回三条评论
        #创建数据存储的缓冲队列
        dataQueue = Queue()
        for threadName in crawlList:
            thread = TreadCrawl(threadName, appQueue, dataQueue)
            thread.start()
            threadcrawl.append(thread)

            # 此处写3个线程去收集数据队列中的数据并存储到指定文件中
        threadparse = []
        parseList = ["解析线程1号", "解析线程2号", "解析线程3号"]
        for threadName in parseList:
            thread = ThreadParse(threadName, dataQueue)
            thread.start()
            threadparse.append(thread)

        #等待队列为空
        while not appQueue.empty():
            pass

        #如果为空了，采集线程退出循环
        for thread in threadcrawl:
            thread.kill_tread()
            thread.join()
            print(thread.threadName+"--我死了")

        while not dataQueue.empty():
            pass

        for thread in threadparse:
            thread.kill_tread()
            thread.join()
            print(thread.threadName + "--我死了")


    def get_queue(self,url):
        '''
        作用：找每个app的url,返回到队列中
        :param url:当前分类的网页地址
        :return: 该分类中app地址的队列
        '''
        html = self.get_html(url)
        xpath = "//div[@id='selectedcontent']/div/ul/li/a/@href"
        app_url_list = self.find_url(xpath,html)
        app_class = self.find_url(xpath_class,html)[1]

        #将数据添加得到队列
        appQueue = Queue()
        # count = 0
        for app in app_url_list:
            app = str(app)+'$'+app_class
            appQueue.put(app)
            # count+=1
            # if count==5:
            #     break

        return appQueue
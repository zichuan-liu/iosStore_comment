import threading
import json
#import jsonpath 效率太低，换正则
import re
import conf.settings as settings

from queue import Queue
from core.apple_crawl import Spider

class TreadCrawl(threading.Thread,Spider):

    def __init__(self,threadName,appQueue,dataQueue):
        '''
        继承线程和自己写的爬虫
        :param threadName: 线程名
        :param appQueue: 数据存储队列
        :param dataQueue: 数据
        '''
        super(TreadCrawl,self).__init__()
        self.threadName = threadName
        self.appQueue = appQueue
        self.dataQueue = dataQueue
        self.CRAWL_EXIT = False

    def run(self):
        print("启动我了" + self.threadName)
        while not self.CRAWL_EXIT:
            try:
                # 取出一个数，先进先出
                # get可选参数：block.默认为True,不会结束
                app_info = self.appQueue.get(block=False)
                url = app_info.split('$')[0]
                app_class = app_info.split('$')[1]
                id,app_name = self.__getid(url)
                print(app_class)
                #print(id)
                #发出请求：第二层页面
                page = 1

                while page <= 10:
                    url = 'https://itunes.apple.com/rss/customerreviews/page=' + str(page)+ '/id='+id+'/json'
                    #print(url)
                    app_json = self.get_html(url)

                    #将用户的评论元组（app类，app名，用户名，评论得分，题目，内容）放入队列中
                    iterator = self.__getdata(app_json)
                    for data in iterator:
                        data.insert(0,app_name)
                        data.insert(0,app_class)
                        self.clear_content(data)
                        self.dataQueue.put(data)
                    #下一页提取
                    page += 1
            except:
                pass

    def __getdata(self,js):
        #提取json中有用的评论
        users = re.findall(settings.re_user,js)
        titles = re.findall(settings.re_title,js)
        content = re.findall(settings.re_content,js)
        sroce = re.findall(settings.re_score,js)

        #组合评论
        texts = list(zip(users,sroce,titles,content))
        for text in texts:
            #强行转化为列表，方便添加数据
            text = list(text)
            #print(text)
            yield text

    def clear_content(self,data):
        '''
        ######注意，不太会清洗数据，不知道如何判断语言是否为英语#############
        :param data:
        :return:
        '''
        #删除文本内容中的\n
        str = data[-1]
        data[-1] = str.replace('\\','').replace('.','')

    def __getid(self,url):
        id = url.split('id')[-1].split('?')[0]
        app_name = url.split('app/')[-1].split('/id')[0]
        return id,app_name

    def kill_tread(self):
        self.CRAWL_EXIT = True
        print("没有可采集的数据")

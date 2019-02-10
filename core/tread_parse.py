import threading
from queue import Queue
from conf import settings
#数据处理
import json

from core.apple_crawl import Spider

class ThreadParse(threading.Thread,Spider):
    def __init__(self,threadName,dataQueue):
        super(ThreadParse,self).__init__()
        self.threadName = threadName
        self.dataQueue = dataQueue
        self.PARSE_EXIT = False

    def run(self):
        print("启动我了"+self.threadName)
        while not self.PARSE_EXIT:
            try:
                data = self.dataQueue.get(block = False)
                data = json.dumps(data)
                self.parse(data)
            except:
                pass

    def parse(self,data):
        with open(settings.filepath,'a',encoding='utf-8')as f:
            f.write(data+'\n')
    def kill_tread(self):
        self.PARSE_EXIT = True
        print("没有可写入的数据")
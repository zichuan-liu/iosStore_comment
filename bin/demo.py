#时间测试(无装饰器）
import time
#主要方法接口
from core.main_spider import MySpider

if __name__ == "__main__":
    start_time = time.time()

    ms = MySpider()
    ms.start()


    end_time = time.time()
    #测试程序的运行时间
    print(end_time-start_time)

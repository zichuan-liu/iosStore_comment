import requests
from lxml.html import etree
import conf.settings

class  Spider:
    def __init__(self):
        self.headers = conf.settings.DEFAULT_REQUEST_HEADERS

    def get_html(self,url):
        '''
        作用：获取网页的html
        :param url: 网页地址
        :return: HTML
        '''
        r = requests.get(url)
        # print(r.content)
        content = r.content.decode('utf-8')
        return content

    def find_url(self,xpath,html):
        '''
        作用：清理HTML，寻找有用的标签中url
        此处用lxml寻找，比bs4效率高
        :param xpath: 寻找条件
        :param html: 网页原代码
        :return: url地址
        '''
        html = etree.HTML(html)
        url_list = html.xpath(xpath)
        #print(url_list)
        #"//div[@class='grid3-column']/ul/li/a/@href"
        return url_list
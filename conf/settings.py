import random
#随机报头User-agent避免ip被封
ua_list = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
]

DEFAULT_REQUEST_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        "User-Agent": random.choice(ua_list)
    }

#app类别  注：列表的第二个：[1]
xpath_class = "//div[@class='intro']//li/a/text()"
# app名称：
xpath_name  = '//header/h1/text()'
# app得分：
xpath_score = "//div[@class='we-customer-ratings__averages']/span/text()"
re_score = '"im:rating":{"label":"(.*?)"}, "id"'
# 评论用户：
xpath_user = "//div[@class='l-row l-row--peek']/div/div/div/span[@class='we-truncate we-truncate--single-line ember-view we-customer-review__user']/text()"
re_user = 'name":{"label":"(.*?)"}, "label":""}'
# 评论日期：
xpath_time = "//div[@class='l-row l-row--peek']/div/div/div/time/text()"
# 评论标题：
xpath_title = "//div[@class='l-row l-row--peek']/div/div/h3/text()"
re_title = '"title":{"label":"(.*?)"},'
# 评论内容：
xpath_content = "//div[@class='l-row l-row--peek']/div/div/p//span[@class='we-clamp__contents']/text()"
re_content = '"content":{"label":"(.*?)"'

#存放的文件位置
filepath = r'C:\Users\77526\PycharmProjects\untitled\day6\ios_store\db\user_comment.txt'
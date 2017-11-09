# coding:utf-8
from lxml import etree
import requests
import gevent
from gevent import monkey
import time

monkey.patch_all()


class TiebaSpider(object):
    def __init__(self):
        self.base_url = "https://tieba.baidu.com"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        # self.headers = {
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"}
        self.tie_filter = "//div[@class = 't_con cleafix']/div/div/div/a/@href"
        self.img_filter = "//img[@class = 'BDE_Image']/@src"

    def send_request(self, url, params=None):
        "发送请求, 返回响应页面"
        try:
            html = requests.get(url, params).content
            # print html
            return html
            # print html
        except Exception as e:
            print e

    def html_filt(self, html, filter):
        '传入html文本和xpath语句 返回过滤出的列表 不会报错 可能返回空列表'
        html = etree.HTML(html)
        link_list = html.xpath(filter)
        return link_list

    def run(self):
        "只用于贴吧页面的调度器"
        tieba_name = raw_input("请输入你要获取的贴吧名")
        start_page = int(raw_input("起始页"))
        end_page = int(raw_input("结束页"))
        f_time = time.time()
        for temp in range(start_page, end_page + 1):
            data = {
                "kw": tieba_name,
                "pn": (temp - 1) * 50
            }
            url = self.base_url + "/f?"
            # 发送贴吧页的请求 获取 帖子列表
            html = self.send_request(url, data)
            # html = gevent.spawn(self.send_request, url, data)
            tiezi_link_list = self.html_filt(html, self.tie_filter)
            for temp in tiezi_link_list:
                # 发送帖子的请求 获取图片列表
                url = self.base_url + temp
                html = self.send_request(url)
                # html = gevent.spawn(self.send_request, url)
                image_link_list = self.html_filt(html, self.img_filter)
                for temp in image_link_list:
                    # 图片写入文件
                    html = self.send_request(temp)
                    file_name = "image/" + temp[-11:]
                    #async
                    # self.wirte_file(html, file_name)
                    gevent.spawn(self.wirte_file, html, file_name)
        e_time = time.time()
        print "抓取结束 欢迎再次使用, 共用时%s秒" %(e_time - f_time)

if __name__ == "__main__":
    tieba_spider = TiebaSpider()
    gevent.spawn(tieba_spider.run())

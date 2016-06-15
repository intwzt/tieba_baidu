#!/usr/bin/env python
#coding=utf-8

import requests
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import re
import json
import codecs

org_url = 'http://tieba.baidu.com/p/3522395718?pn=1'

class Spider:

    url_set = []
    start_page = 0
    numpage = 0

    def __init__(self, num):
        print 'Init spider...'
        self.geturl(org_url, num)
        print 'Init Finished!'

    def geturl(self, org_url, num):
        now_page = int(re.search('pn=(\d+)', org_url, re.S).group(1))
        self.start_page = now_page
        self.numpage = num
        for i in range(self.start_page, self.numpage+1):
            link = re.sub('pn=\d+', 'pn=%d'%i, org_url, re.S)
            self.url_set.append(link)

    def getsource(self, url):
        html = requests.get(url)
        html.encoding = 'utf-8'
        return html.text

    def writeinfo(self, item):
        f.writelines('reply_author:\t' + item['reply_author'] + '\n')
        f.writelines('reply_time:\t' + item['reply_time'] + '\n')
        f.writelines('reply_content:\t' + item['reply_content'] + '\n\n')



    def singleprocess(self, url):
        html = self.getsource(url)
        selector = etree.HTML(html)
        block = selector.xpath('//div[@class="l_post j_l_post l_post_bright  "]')
        items = {}

        for each in block:
            reply_info = json.loads(each.xpath('@data-field')[0].replace('@quot', ''))
            author = reply_info['author']['user_name']
            reply_time = reply_info['content']['date']
            reply_content = each.xpath('div[@class="d_post_content_main"]/div/cc/div[@class="d_po'
                                       'st_content j_d_post_content  clearfix"]/text()')[0]
            items['reply_author'] = author
            items['reply_time'] = reply_time
            items['reply_content'] = reply_content
            self.writeinfo(items)

    def multiprocess(self):
        print 'Start spider...'
        pool = ThreadPool(2)
        pool.map(self.singleprocess, self.url_set)
        print 'Finished!'




if __name__ == '__main__':
    tieba_spider = Spider(20)
    f = codecs.open('result.txt', 'w', 'utf-8')
    tieba_spider.multiprocess()
    f.close()



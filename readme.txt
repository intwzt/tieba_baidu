本代码用Xpath和正则表达式实现一个简易爬虫，爬取一个百度贴吧的部分内容。
起始网址是http://tieba.baidu.com/p/3522395718?pn=1，可修改"pn=1"的数字来改变爬取内容。

爬取内容是：
发帖人
发帖时间
发帖内容

代码使用multiprocessing创建多线程进行加速，实测有效果。
result.txt中是示例结果，可修改"tieba_spider = Spider(20)"中的20来修改爬取的网页数量.

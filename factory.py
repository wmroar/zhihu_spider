# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import json
import urls
from threading import Thread
from urls import urls_queue
import url_content
import time
import pickle

class Spider(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.url_prefix = 'http://www.zhihu.com'
        self.exit_flag = False
        self.start_time = time.time()

    def exit(self):
        self.exit_flag = True

    def run(self):
        while not self.exit_flag:
            url = urls_queue.get()
            if 'question' in url:
                url_content.QuestionContent(self.url_prefix + url).spider()
            elif 'people' in url:
                url_content.UserContent(self.url_prefix + url).spider()
            else:
                url_content.QuestionContent(self.url_prefix + url).parse_content_urls()

            if time.time() - self.start_time >= 300:
                self.start_time = time.time()
                with open('F:\\code\\zhihu_spider\\queue.dump','w') as a:
                    a.write(url)


def main():
    with open('F:\\code\\zhihu_spider\\queue.dump','r') as a:
        data = a.readlines()
        if data:
            urls_queue.put(data[-1])
        else:
            urls_queue.put(urls.start_url)
    tasks = []
    for i in xrange(10):
         tasks.append(Spider())

    for i in tasks:
        i.start()

if __name__ == '__main__' :
    main()

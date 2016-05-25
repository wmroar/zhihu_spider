# -*- coding:utf-8 -*-

import requests
import urls
import re
from bs4 import BeautifulSoup

class BaseContent(object):

    def __init__(self,url):
        self.url = url
        self.url_content = self._init_url_content()

    def _init_url_content(self):

        r = requests.get(self.url)
        r.encoding = 'utf-8'

        return r.content


class UserContent(BaseContent):

    def __init__(self,url):
        super(UserContent,self).__init__(url)
        self.username = ''
        self.fans_num = 0
        self.aggree_num = 0

    def parse_content_urls(self):

        bso = BeautifulSoup(self.url_content,'lxml')

        tmp = []

        for one in bso.find_all('a'):
            url = one.attrs.get('href')
            if url and re.match('/\w*/.*', url):
                if url.split('/')[1] in ['people', 'question', 'topic']:
                    tmp.append(url)

        print tmp
        for url in list(set(tmp)):
            urls.urls_queue.put(url)

    def parse_user_info(self):

        bso = BeautifulSoup(self.url_content,'lxml')
        self.aggree_num = bso.select('.zm-profile-header-user-agree')[0].select('strong')[0].text
        self.thanks_num = bso.select('.zm-profile-header-user-thanks')[0].select('strong')[0].text

if __name__ == '__main__' :

    c = UserContent(urls.start_url)
    c.parse_user_info()
# -*- coding:utf-8 -*-

import requests
import urls
import re
import dbtool
from bs4 import BeautifulSoup

class BaseContent(object):

    def __init__(self,url):
        self.url = url
        print url
        self.url_content = self._init_url_content()
        self.data = []

    def _init_url_content(self):

        r = requests.get(self.url)
        r.encoding = 'utf-8'

        return r.content

    def parse_content_urls(self):

        bso = BeautifulSoup(self.url_content,'lxml')

        tmp = []

        for one in bso.find_all('a'):
            url = one.attrs.get('href')
            if url and re.match('/\w*/.*', url):
                if url.split('/')[1] in ['people', 'question', 'topic']:
                    tmp.append(url)

        for url in list(set(tmp)):
            urls.urls_queue.put(url)


    def set_data_to_db(self):
        for data in self.data:
            dbtool.set_data_to_db(self.col, data)

    def parse_content(self):
        pass

    def spider(self):
        self.parse_content_urls()
        self.parse_content()
        self.set_data_to_db()

class UserContent(BaseContent):

    def __init__(self,url):
        super(UserContent,self).__init__(url)
        self.username = ''
        self.fans_num = 0
        self.agree_num = 0
        self.col = 'user'



    def parse_content(self):
        try:
            bso = BeautifulSoup(self.url_content,'lxml')
            self.agree_num = int(bso.select('.zm-profile-header-user-agree')[0].select('strong')[0].text)
            self.thanks_num = bso.select('.zm-profile-header-user-thanks')[0].select('strong')[0].text
            self.username = bso.select('.name')[0].text
            if int(self.agree_num) < 10000:
                return
            self.data = [{'agree_num' : self.agree_num, 'fans_num' : self.fans_num, 'username' : self.username, 'url' : self.url}]
        except:
            print 'parse user error,continue!'

class QuestionContent(BaseContent):

    def __init__(self,url):

        super(QuestionContent,self).__init__(url)
        self.username = ''
        self.aggree_num = 0
        self.thanks_num = 0
        self.title = ''
        self.col = 'answer'

    def parse_content(self):

        bso = BeautifulSoup(self.url_content,'lxml')
        final  = []
        try:
            for one in  bso.select('#zh-question-answer-wrap')[0].select('> div'):
                    answer_dict = {}
                    answer_dict['agree_num'] = int(one.select('.zm-item-vote-info')[0].attrs.get('data-votecount'))
                    if int(answer_dict['agree_num']) < 2000:
                        continue
                    answer_dict['text'] = one.find_all('div', class_=['zm-editable-content','clearfix'])[0].text
                    answer_dict['url'] = one.find_all('div', class_=['zm-item-rich-text','expandable','js-collapse-body'])[0].attrs.get('data-entry-url')
                    self.data.append(answer_dict)
        except:
            print 'parse error, continue'



if __name__ == '__main__' :
    c = QuestionContent(urls.start_url)
    c.parse_question_info()
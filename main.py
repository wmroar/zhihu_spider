# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import json
import urls

def _get_url_content(url):

    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.content

def get_bs_obj(content):

    return BeautifulSoup(content)

def get_zhihu_tag():
    pass

if __name__ == '__main__' :
    print _get_url_content(urls.start_url)
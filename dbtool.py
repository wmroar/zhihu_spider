# -*- coding : utf-8 -*-

from pymongo import MongoClient
import pymongo
import copy

client =  MongoClient("mongodb://localhost")
mongo_db = client.zhihu_spider

cols = ['user', 'answer']

def set_data_to_db(col,data):
    if col in cols is False:
        return "Invalid collections name"

    users = mongo_db[col]
    _d = {}

    if col == 'user' and data:
        _d['username'] = data.get('username','0')
    else:
        _d['url'] = data.get('url','0')

    if users.find(_d).count():
        return "data has exists in database"

    users.insert_one(data)

def get_data_from_db(col):
    if col in cols is False:
        return "Invalid collections name"

    users = mongo_db[col]

    datas = users.find({}).sort('agree_num',pymongo.DESCENDING)

    result = []

    for data in datas :

        del data['_id']
        result.append(data)

    return result

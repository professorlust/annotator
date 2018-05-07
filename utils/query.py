# !/usr/bin/python
# -*- coding:utf-8 -*-  
# Author: Shengjia Yan
# Date: 2017/3/3
# Email: sjyan@seu.edu.cn

import pymongo
from pymongo import MongoClient

ip = '10.0.5.40'
annotator = 'fengchao.wang'

def query(ip, annotator):
    conn = MongoClient(ip, 27017)
    db = conn.annotation

    for item in db.ocr_data.find({"annotator": annotator}):
        print(item["ocr_id"])

def main():
    query()

if __name__ == '__main__':
    main()
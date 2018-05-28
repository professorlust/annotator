# !/usr/bin/python
# -*- coding:utf-8 -*-  
# Author: Shengjia Yan
# Date: 2017/3/3
# Email: sjyan@seu.edu.cn

import pymongo
from pymongo import MongoClient


def find_ocr_progress(ip, annotator):
    conn = MongoClient(ip, 27017)
    db = conn.annotation

    for item in db.ocr_data.find({"annotator": annotator}):
        print(item["ocr_id"])

def main():
    ip = '10.0.5.40'
    annotator = 'fengchao.wang'
    find_ocr_progress(ip, annotator)

if __name__ == '__main__':
    main()
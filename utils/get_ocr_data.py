# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-05-24 Thursday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

import json
from bson import json_util
import pymongo
from pymongo import MongoClient

ip = '10.0.5.40'
ocr_data_filepath = '../data/ocr/ocr_data.txt'

def get_ocr_data():
    conn = MongoClient(ip, 27017)
    db = conn.annotation
    
    with open(ocr_data_filepath, 'a') as ofile:
        ofile.seek(0)
        ofile.truncate()
        for record in db.ocr_data.find({}):
            record_json = json.dumps(record, default=json_util.default)
            ofile.write(record_json + '\n')

def main():
    get_ocr_data()

if __name__ == '__main__':
    main()

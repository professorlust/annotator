# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-05-24 Thursday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

import json
from bson import json_util
import argparse
import pymongo
from pymongo import MongoClient

def parse_args():
    parser = argparse.ArgumentParser('Annotator')
    parser.add_argument('--ip', type=str, default='10.7.13.73', help='MongoDB ')
    parser.add_argument('--port', type=int, default=27017, help='MongoDB port')
    parser.add_argument('--db', type=str, default='annotation', help='MongoDB database')
    parser.add_argument('--collection', type=str, default='ocr_data', help='MongoDB collection')
    parser.add_argument('--save_path', default='../data/ocr/ocr_data.txt', help='path to save annotation data')
    return parser.parse_args()

def get_annotation_data(args):
    conn = MongoClient(args.ip, args.port)
    db = conn[args.db]
    
    with open(args.save_path, 'a') as ofile:
        print('Exporting...')
        ofile.seek(0)
        ofile.truncate()
        for record in db[args.collection].find({}):
            record_json = json.dumps(record, default=json_util.default)
            ofile.write(record_json + '\n')
    print('Done!')

def main():
    args = parse_args()
    get_annotation_data(args)

if __name__ == '__main__':
    main()

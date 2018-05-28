# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-05-28 Monday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

import json
from bson import json_util
import pymongo
from pymongo import MongoClient

ip = '10.6.2.6'
port = 47901
essay_items_info_filepath = '../data/raw/essay_items_info.txt'
essay_scandata_filepath = '../data/raw/essay_scandata.txt'
en_essay_type = [5008, 5348, 6, 7]

def get_items_info(ip, port):
    conn = MongoClient(ip, port)
    db = conn.klx_analysis
    temp_endata = db.temp_endata
    items_id_list = []

    with open(essay_items_info_filepath, 'a') as ofile:
        ofile.seek(0)
        ofile.truncate()
        for item in temp_endata.find():
            items_info = item['items_info']
            for item_id, info in items_info.items():
                prompt = {}
                type = info['type']
                if type in en_essay_type and item_id not in items_id_list:
                    items_id_list.append(item_id)

                    type_mean     = info['type_mean']
                    stem_plain    = info['stem_plain']
                    stem_plain_qs = info['stem_plain_qs']
                    
                    prompt['item_id']       = item_id
                    prompt['type']          = type
                    prompt['type_mean']     = type_mean
                    prompt['stem_plain']    = stem_plain
                    prompt['stem_plain_qs'] = stem_plain_qs

                    prompt_json = json.dumps(prompt)
                    ofile.write(prompt_json + '\n')

def get_essay_scandata(ip, port):
    # conn = MongoClient(ip, port)
    # db = conn.klx_analysis
    # temp_endata = db.temp_endata
    valid_item_id_list = []     # item id with prompt info

    with open(essay_items_info_filepath, 'r') as ifile:
        for line in ifile:
            line = line.strip()
            item_info = json.loads(line)
            if item_info['stem_plain'] != '':
                valid_item_id_list.append(item_info['item_id'])

    print(valid_item_id_list)

    # with open(essay_scandata_filepath, 'a') as ofile:
    #     ofile.seek(0)
    #     ofile.truncate()
    #     for item in temp_endata.find():
    #         answer_data = item['answer_data']







def main():
    # get_items_info(ip, port)
    get_essay_scandata(ip, port)

if __name__ == '__main__':
    main()

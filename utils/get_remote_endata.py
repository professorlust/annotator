# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-05-28 Monday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

import codecs
import json
from bson import json_util
import pymongo
from pymongo import MongoClient

ip = 'mongodb://klx_user:Lba7odZDJ(PbdY@10.6.2.5:47901,10.6.2.6:47901/admin'
port = 47901
essay_items_info_filepath = './essay_items_info.txt'
essay_scandata_filepath = './essay_scandata.txt'
en_essay_type = [5008, 5348, 6, 7]

def get_items_info():
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

def get_essay_scandata():
    conn = MongoClient(ip, port)
    db = conn.klx_analysis
    temp_endata = db.temp_endata
    valid_item_id_list = []     # item id with prompt info

    with codecs.open(essay_items_info_filepath, mode='r', encoding='ascii', errors='ignore') as ifile:
        for line in ifile:
            line = line.strip()
            item_info = json.loads(line)
            if item_info['stem_plain'] != '':
                valid_item_id_list.append(item_info['item_id'])

    with open(essay_scandata_filepath, 'a') as ofile:
        ofile.seek(0)
        ofile.truncate()
        for item in temp_endata.find():
            paper_id    = item['paper_id']
            answer_data = item['answer_data']
            for answer in answer_data:
                answer_data = {}
                item_id = answer['item_id']
                if item_id in valid_item_id_list:
                    image_url   = answer['url']
                    total_score = answer['total_score']
                    score       = answer['score']
                    number      = answer['number']

                    answer_data['paper_id']    = paper_id
                    answer_data['item_id']     = item_id
                    answer_data['image_url']   = image_url
                    answer_data['total_score'] = total_score
                    answer_data['score']       = score
                    answer_data['number']      = number

                    answer_json = json.dumps(answer_data)
                    ofile.write(answer_json + '\n')


def main():
    get_items_info()
    get_essay_scandata()

if __name__ == '__main__':
    main()

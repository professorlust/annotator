# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-06-29 Friday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.


import os
import csv
import json

ocr_data_path = '../data/ocr/batch_0/full_essay_data.txt'
export_path = '../data/essay/batch_0/essay.csv'

def export_essay_data():
    essay_list = []
    with open(ocr_data_path, 'r') as in_file:
        counter = 0
        for line in in_file:
            essay_info = {}
            counter += 1
            if (counter <= 200):
                continue
            info = json.loads(line)
            essay_info['essay'] = info['ocr_correction']
            image_id = info['image_id']
            essay_info['id'] = image_id.replace('.jpg', '')
            essay_list.append(essay_info)
    
    with open(export_path, 'w') as o_file:
        writer = csv.DictWriter(o_file, essay_list[0].keys())
        writer.writeheader()
        for row in essay_list:
            writer.writerow(row)


if __name__ == '__main__':
    export_essay_data()
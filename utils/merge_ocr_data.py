# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-05-24 Thursday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

import json

ocr_data_path = '../data/ocr/ocr_data.txt'
essay_data_path = '../data/ocr/essay_data.json'
full_essay_data_path = '../data/ocr/full_essay_data.txt'

def read_essay_data():
    with open(essay_data_path, 'r') as essay_data_file:
        essay_data = []
        for line in essay_data_file:
            line = line.strip()
            essay_json = json.loads(line)
            if essay_json['prompt'][0] != '':
                essay_data.append(essay_json)
    return essay_data

def merger():
    essay_data = read_essay_data()

    with open(full_essay_data_path, 'a') as ofile:
        ofile.seek(0)
        ofile.truncate()
        with open(ocr_data_path, 'r') as ocr_data:
            for line in ocr_data:
                line = line.strip()
                ocr_json = json.loads(line)
                image_url = ocr_json['image_url']
                image_id = image_url.replace('http://klximg.oss-cn-beijing.aliyuncs.com/scanimage/', '')
                match = next(item for item in essay_data if item["image_id"][0] == image_id)
            
                ocr_json['image_id']    = image_id
                ocr_json['total_score'] = match['total_score']
                ocr_json['prompt']      = match['prompt'][0]
                ocr_json['problem_id']  = match['problem_id']
                ocr_json['paper_id']    = match['paper_id']
                ocr_json['score']       = match['score']

                ocr_text = json.dumps(ocr_json)
                ofile.write(ocr_text + '\n')

def main():
    merger()

if __name__ == '__main__':
    main()

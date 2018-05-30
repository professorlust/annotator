# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-05-29 Tuesday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

import json

scandata_path = '../data/raw/essay_scandata.txt'
candidate_path = '../data/ocr/batch_1/ocr.txt'
scanimage_prefix = 'http://klximg.oss-cn-beijing.aliyuncs.com/scanimage/'

def convert():
    with open(candidate_path, 'a') as ofile:
        ofile.seek(0)
        ofile.truncate()
        with open(scandata_path, 'r') as ifile:
            for line in ifile:
                line = line.strip()
                record = json.loads(line)
                image_url = record['image_url']
                if len(image_url) > 0:
                    for url in image_url:
                        url = url.replace(scanimage_prefix, '')
                        ofile.write(url + '\n')

def main():
    convert()

if __name__ == '__main__':
    main()
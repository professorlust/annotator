# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-06-28 Thursday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

import os
import json

ocr_data_path = '../data/ocr/batch_0/full_essay_data.txt'
save_dir = '../data/img/'

def download_images(quantity=200):
    with open(ocr_data_path, 'r') as in_file:
        counter = 0
        for line in in_file:
            counter += 1
            if (counter > quantity):
                break
            info = json.loads(line)
            image_url = info['image_url']
            essay = info['ocr_correction']
            image_id = info['image_id']
            image_name = image_id.replace('.jpg', '')
            os.system('wget ' + image_url + ' -P ' + save_dir)
            essay_fname = save_dir + image_name + '.txt'
            os.system('touch ' + essay_fname)
            with open(essay_fname, 'w') as o_file:
                o_file.write(essay)


if __name__ == '__main__':
    download_images()






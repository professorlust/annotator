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

def download_images(quantity=2000):
    with open(ocr_data_path, 'r') as in_file:
        counter = 0
        for line in in_file:
            counter += 1
            if (counter <= 200):
                continue
            if (counter > quantity):
                break
            
            info = json.loads(line)
            image_url = info['image_url']
            essay = info['ocr_correction']
            image_id = info['image_id']
            image_name = image_id.replace('.jpg', '')
            fname = str(counter) + '_' + image_name
            essay_fname = save_dir + fname + '.txt'
            image_fname = save_dir + fname + '.jpg'
            os.system('wget ' + image_url + ' -O ' + image_fname)
            os.system('touch ' + essay_fname)
            with open(essay_fname, 'w') as o_file:
                o_file.write(essay)

def get_essay_statistics():
    with open(ocr_data_path, 'r') as in_file:
        counter = 0
        max = 21
        scores = [0] * max
        for line in in_file:
            counter += 1
            info = json.loads(line)
            score = int(info['score'])
            scores[score] += 1
        
        for i in range(max):
            print('{}: {}'.format(i, scores[i]))

def uniform_sampling():
    quota = [150] * 16
    with open(ocr_data_path, 'r') as in_file:
        counter = 0
        for line in in_file:
            counter += 1
            info = json.loads(line)
            score = int(info['score'])

            if (quota[score] <= 0):
                continue

            image_url = info['image_url']
            essay = info['ocr_correction']
            image_id = info['image_id']
            image_name = image_id.replace('.jpg', '')
            fname = str(score) + '_' + image_name
            essay_fname = save_dir + fname + '.txt'
            image_fname = save_dir + fname + '.jpg'
            os.system('wget ' + image_url + ' -O ' + image_fname)
            os.system('touch ' + essay_fname)
            with open(essay_fname, 'w') as o_file:
                o_file.write(essay)
            
            quota[score] -= 1

def main():
    uniform_sampling()

if __name__ == '__main__':
    main()






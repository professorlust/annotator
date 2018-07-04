# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-06-28 Thursday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

import os
import csv
import json
import codecs

ocr_data_path = '../data/ocr/batch_0/full_essay_data.txt'
save_dir = '../data/img/'
samples_path = '../data/samples.csv'

def download_images(quantity=2000):
    with codecs.open(ocr_data_path, 'r') as in_file:
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
    with codecs.open(ocr_data_path, 'r') as in_file:
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
    samples = []
    with codecs.open(ocr_data_path, 'r') as in_file:
        counter = 0
        for line in in_file:
            essay_dict = {}
            info = json.loads(line)
            score = int(info['score'])

            if (score > 15 or quota[score] <= 0):
                continue
            
            counter += 1
            image_url = info['image_url']
            essay = info['ocr_correction']
            image_id = info['image_id']
            image_name = image_id.replace('.jpg', '')
            essay_dict['number'] = counter
            essay_dict['id'] = image_name
            essay_dict['essay'] = essay
            samples.append(essay_dict)
            fname = str(counter) + '_' + image_name
            image_fname = save_dir + fname + '.jpg'
            os.system('wget ' + image_url + ' -O ' + image_fname)
            
            quota[score] -= 1
    
    with open(samples_path, mode='w', encoding="utf8", errors='ignore') as out_file:
        writer = csv.DictWriter(out_file, samples[0].keys())
        writer.writeheader()
        for row in samples:
            writer.writerow(row)

def main():
    uniform_sampling()

if __name__ == '__main__':
    main()






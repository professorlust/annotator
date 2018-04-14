# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Chen Dong
# @date: 2018-04-13 Friday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

import io
import sys
import json
import pprint
from time import time, localtime
from numpy import NaN
from sklearn.metrics import cohen_kappa_score
from pymongo import MongoClient
import logging
logger = logging.getLogger(__name__)

class KappaCalculator:
    def __init__(self):
        self.time_now = int(time())
        self.time_local = localtime(self.time_now)
    
    def connect_db(self):
        self.conn = MongoClient("localhost", 27017)
        self.db = self.conn.annotation
    
    def load_accounts(self):
        self.account_path = '../data/account.txt'
        self.accounts = {}  # {account: password}
        with open(self.account_path, 'r') as accounts_file:
            for line in accounts_file:
                line = line.strip()
                (account, password) = line.split('\t')
                self.accounts[account] = password
    
    def get_progress(self):
        annotation_progress = []
        essay_progress_db = db.essay_progress
        for key in accounts:
            progress = {}
            progress['annotator'] = key
            progress['progress'] = essay_progress_db.find_one({'annotator':key})['annotation_list']
            annotation_progress.append(progress)

        total_progress = set(annotation_progress[0]['progress'])
        for progress in annotation_progress:
            total_progress = set(progress['progress']) & total_progress
    
    def get_scores(self):
        essay_data_db = db.essay_data
        essay_data = {}
        for essay_id in total_progress:
            for data in essay_data_db.find({'essay_id':essay_id}):
                data_id = str(data['_id'])
                del data['_id']
                essay_data[data_id] = data
                pprint.pprint(data)
        
        # get y1 for cohen_kappa_score
        y1 = []
        for essay_id in total_progress:
            for key in essay_data:
                if essay_data[key]['essay_id'] == essay_id:
                    y1.append(essay_data[key]['content_score'])
                    y1.append(essay_data[key]['sentence_score'])
                    y1.append(essay_data[key]['structure_score'])
                    y1.append(essay_data[key]['vocabulary_score'])
                    break
            del essay_data[key]
        
        # get y2 for cohen_kappa_score
        y2 = []
        for key in essay_data:
            y2.append(essay_data[key]['content_score'])
            y2.append(essay_data[key]['sentence_score'])
            y2.append(essay_data[key]['structure_score'])
            y2.append(essay_data[key]['vocabulary_score'])
    
    def calculate_kappa(self):
        kappa_score = cohen_kappa_score(y1, y2, weights='quadratic')
        kappa = {}
        kappa['time'] = time.time()
        kappa['kappa'] = kappa_score






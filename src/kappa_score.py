import json
import pprint
import logging
import time
import sys
import io
from numpy import NaN
from sklearn.metrics import cohen_kappa_score
from pymongo import MongoClient

#log time
time_now = int(time.time())
time_local = time.localtime(time_now)
print(time.strftime("%Y-%m-%d %H:%M:%S",time_local))

#connect db
conn = MongoClient("localhost", 27017)
db = conn.annotation

#load annotator information
account_path = '../data/account.txt'
accounts = {}  # [{account: password}]
with open(account_path, 'r') as accounts_file:
    for line in accounts_file:
        line = line.strip()            
        account_dict = {}
        (account, password) = line.split('\t')
        accounts[account] = password
print('Accounts:')
print(json.dumps(accounts, indent=4, sort_keys=True))

#get annotation progress from db
annotation_progress = []
essay_progress_db = db.essay_progress
for key in accounts:
    progress = {}
    progress['annotator'] = key
    progress['progress'] = essay_progress_db.find_one({'annotator':key})['annotation_list']
    annotation_progress.append(progress)
print('Annotation progress:')
print(json.dumps(annotation_progress, indent=4, sort_keys=True))

total_progress = set(annotation_progress[0]['progress'])
for progress in annotation_progress:
    total_progress = set(progress['progress']) & total_progress 
print('Total progress:')
print(total_progress)

#get essay scores
essay_data_db = db.essay_data
essay_data = {}
for essay_id in total_progress:
    for data in essay_data_db.find({'essay_id':essay_id}):
        data_id = str(data['_id'])
        del data['_id']
        essay_data[data_id] = data
        pprint.pprint(data)
print('Essay data:')
pprint.pprint(essay_data)

#get y1 for cohen_kappa_score
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
print('y1:')
print(y1)

#get y2 for cohen_kappa_score
y2 = []
for key in essay_data:
    y2.append(essay_data[key]['content_score'])
    y2.append(essay_data[key]['sentence_score'])
    y2.append(essay_data[key]['structure_score'])
    y2.append(essay_data[key]['vocabulary_score'])
print('y2:')
print(y2)

#calculate kappa score
y3 = [2,2,2,2,2,2]
y4 = [2,2,2,2,2,2]

kappa_score = cohen_kappa_score(y3, y4,weights='quadratic')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
f = open('../data/essay/essay_kappa_score.json','a')
kappa = {}
kappa['time'] = time.time()
kappa['kappa'] = kappa_score
    
f.write(json.dumps(kappa))
f.write('\n')


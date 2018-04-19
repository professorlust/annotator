# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-13 Tuesday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

from .base import *
from time import time

class MarkHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.get_progress()
        self.get_essay()
        self.get_mark()

        self.render(
            'mark.html',
            title='Essay Grading Annotation',
            essay_id=self.application.current_essay_id,
            essay=self.application.current_essay,
            annotated_essay_quantity=self.application.annotated_essay_quantity,
            sum=self.application.essay_quantity,
            annotation_essay_ratio=self.application.annotation_essay_ratio,
            essay_annotator_mark = self.application.essay_annotator_mark
        )

    def get_progress(self):
        progress = self.application.db.essay_progress
        annotator = (self.current_user).decode('ascii')
        progress_record = progress.find_one({'annotator':annotator})
        self.application.annotated_essay_quantity = progress_record['annotated_essay_quantity']
        self.application.annotation_essay_ratio = float(100 * self.application.annotated_essay_quantity / self.application.essay_quantity)
    
    def get_essay(self):
        candidates = self.application.db.essay_candidates
        annotator = (self.current_user).decode('ascii')
        #essay_record = candidates.find_one({'annotator': {'$ne': annotator}})
        essay_record = candidates.aggregate([{'$match':{'annotator': {'$ne': annotator}}},
                                             {'$sample':{'size':1}}])
        if essay_record != None:
            for essay in essay_record:
                self.application.current_essay_id = essay['essay_id']
                self.application.current_essay = essay['essay']
        else:
            self.application.current_essay_id = self.application.essay_quantity-1
            self.application.current_essay = self.application.essays[self.application.essay_quantity-1]

    def get_mark(self):
        candidates = self.application.db.essay_candidates
        essay_id = self.application.current_essay_id
        essay_record = candidates.find_one({'essay_id':essay_id})
        if essay_record == None:
            self.application.essay_annotator_mark = 'both'
        else:
            self.application.essay_annotator_mark = essay_record['annotator']


class MarkSubmitHandler(BaseHandler):
    def post(self):
        essay_id = int(self.get_argument('essay_id'))
        overall_score = int(self.get_argument('overall_score'))
        vocabulary_score = int(self.get_argument('vocabulary_score'))
        sentence_score = int(self.get_argument('sentence_score'))
        structure_score = int(self.get_argument('structure_score'))
        content_score = int(self.get_argument('content_score'))

        mark_record = {}
        mark_record['annotator'] = (self.current_user).decode('ascii')
        mark_record['essay_id'] = essay_id
        mark_record['overall_score'] = overall_score
        mark_record['vocabulary_score'] = vocabulary_score
        mark_record['sentence_score'] = sentence_score
        mark_record['structure_score'] = structure_score
        mark_record['content_score'] = content_score
        mark_record['time'] = time()

        response = {}

        if self.application.db.essay_candidates.find_one({'essay_id':self.application.current_essay_id}) != None:
            self.write_db(mark_record)
            response['invalid_flag'] = False
        else:
            response['invalid_flag'] = True 
        self.get_essay()
        self.get_progress()
        self.get_mark()

        response['essay'] = self.application.current_essay
        response['essay_id'] = self.application.current_essay_id
        response['annotated_essay_quantity'] = self.application.annotated_essay_quantity
        response['annotation_essay_ratio'] = self.application.annotation_essay_ratio
        response['essay_annotator_mark'] = self.application.essay_annotator_mark

        # check db
        candidates = self.application.db.essay_candidates
        annotator = (self.current_user).decode('ascii')
        essay_record = candidates.find_one({'annotator': {'$ne': annotator}})
        if essay_record == None:
            response['empty_flag'] = True
        else:
            response['empty_flag'] = False
        
        self.write(response)

    def get_progress(self):
        progress = self.application.db.essay_progress
        annotator = (self.current_user).decode('ascii')
        progress_record = progress.find_one({'annotator':annotator})
        self.application.annotated_essay_quantity = progress_record['annotated_essay_quantity']
        self.application.annotation_essay_ratio = float(100 * self.application.annotated_essay_quantity / self.application.essay_quantity)
    
    def get_essay(self):
        candidates = self.application.db.essay_candidates
        annotator = (self.current_user).decode('ascii')
        essay_record = candidates.aggregate([{'$match':{'annotator': {'$ne': annotator}}},
                                             {'$sample':{'size':1}}])
        if essay_record != None:
            for essay in essay_record:
                self.application.current_essay_id = essay['essay_id']
                self.application.current_essay = essay['essay']
        else:
            self.application.current_essay_id = self.application.essay_quantity-1
            self.application.current_essay = self.application.essays[self.application.essay_quantity-1]
    
    def get_mark(self):
        candidates = self.application.db.essay_candidates
        essay_id = self.application.current_essay_id
        essay_record = candidates.find_one({'essay_id':essay_id})
        if essay_record == None:
            self.application.essay_annotator_mark = 'both'
        else:
            self.application.essay_annotator_mark = essay_record['annotator']

    def write_db(self, record):
        data = self.application.db.essay_data
        candidates = self.application.db.essay_candidates
        marked = self.application.db.essay_marked
        progress = self.application.db.essay_progress
        essay_id = record['essay_id']
        annotator = record['annotator']

        if data.find_one({'essay_id': essay_id, 'annotator':annotator}) == None:
            data.insert_one(record)

            # annotated_essay_quantity + 1
            progress.update_one(
                {
                    'annotator': annotator
                },
                {'$inc': 
                    {
                        'annotated_essay_quantity': 1
                    }
                }
            )

            # update annotation list
            progress_record = progress.find_one({'annotator':annotator})
            annotation_list = progress_record['annotation_list']
            annotation_list.append(essay_id)
            progress.update_one(
                {
                    'annotator': annotator
                },
                {'$set': 
                    {
                        'annotation_list': annotation_list
                    }
                }
            )

            # update candidates annotator
            candidates_record = candidates.find_one({'essay_id': essay_id})
            last_annotator = candidates_record['annotator']
            # if the essay has never been corrected
            if last_annotator == '':
                candidates.update_one(
                    {
                        'essay_id': essay_id
                    },
                    {'$set': 
                        {
                            'annotator': annotator
                        }
                    }
                )
            #if the essay has been corrected by the other annotator
            else:
                self.check_mark(essay_id) # check the scores of the essay marked by two persons
                candidates.delete_one({'essay_id': essay_id})
                marked.insert_one(candidates_record)

        else:
            data.update_one(
                {'essay_id': essay_id},
                {'$set': record},
                upsert=False
            )

    def check_mark(self, essay_id):
        data = self.application.db.essay_data
        unchecked = self.application.db.essay_unchecked
        check_data = []
        for d in data.find({'essay_id': essay_id}):
            check_data.append(d)
        score1 = int(check_data[0]['vocabulary_score']) + int(check_data[0]['sentence_score']) + int(check_data[0]['structure_score']) + int(check_data[0]['content_score'])
        score2 = int(check_data[1]['vocabulary_score']) + int(check_data[1]['sentence_score']) + int(check_data[1]['structure_score']) + int(check_data[1]['content_score'])
        if abs(score1 - score2) > round(0.1 * 8):
            record = {}
            record['essay_id'] = essay_id
            record['annotator1'] = check_data[0]
            record['annotator2'] = check_data[1]
            unchecked.insert_one(record)
        else:
            return

    def close_db(self):
        self.application.conn.close()


class MarkPreviousHandler(BaseHandler):
    def post(self):
        essay_id = int(self.get_argument('essay_id'))

        self.get_essay(essay_id - 1)
        self.get_mark()
        response = {}
        response['essay'] = self.application.current_essay
        response['essay_annotator_mark'] = self.application.essay_annotator_mark
        self.write(response)

    def get_essay(self, essay_id):
        essay_record = self.application.essays[essay_id]
        self.application.current_essay_id = essay_id
        self.application.current_essay = essay_record

    def get_mark(self):
        candidates = self.application.db.essay_candidates
        essay_id = self.application.current_essay_id
        essay_record = candidates.find_one({'essay_id':essay_id})
        if essay_record == None:
            self.application.essay_annotator_mark = 'both'
        else:
            self.application.essay_annotator_mark = essay_record['annotator']


class MarkNextHandler(BaseHandler):
    def post(self):
        essay_id = int(self.get_argument('essay_id'))

        self.get_essay(essay_id + 1)
        self.get_mark()
        response = {}
        response['essay'] = self.application.current_essay
        response['essay_annotator_mark'] = self.application.essay_annotator_mark
        self.write(response)

    def get_essay(self, essay_id):
        essay_record = self.application.essays[essay_id]
        self.application.current_essay_id = essay_id
        self.application.current_essay = essay_record
    
    def get_mark(self):
        candidates = self.application.db.essay_candidates
        essay_id = self.application.current_essay_id
        essay_record = candidates.find_one({'essay_id':essay_id})
        if essay_record == None:
            self.application.essay_annotator_mark = 'both'
        else:
            self.application.essay_annotator_mark = essay_record['annotator']


class MarkJumpHandler(BaseHandler):
    def post(self):
        jump_id = int(self.get_argument('jump_id'))
        self.get_essay(jump_id)
        self.get_mark()

        response = {}
        response['essay'] = self.application.current_essay
        response['essay_annotator_mark'] = self.application.essay_annotator_mark
        self.write(response)

    def get_essay(self, essay_id):
        essay_record = self.application.essays[essay_id]
        self.application.current_essay_id = essay_id
        self.application.current_essay = essay_record
    
    def get_mark(self):
        candidates = self.application.db.essay_candidates
        essay_id = self.application.current_essay_id
        essay_record = candidates.find_one({'essay_id':essay_id})
        if essay_record == None:
            self.application.essay_annotator_mark = 'both'
        else:
            self.application.essay_annotator_mark = essay_record['annotator']
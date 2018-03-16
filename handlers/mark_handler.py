# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-13 Tuesday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

import tornado.web

class MarkHandler(tornado.web.RequestHandler):
    def get(self):
        self.get_progress()
        self.get_essay()

        self.render(
            'mark.html',
            title='Essay Grading Annotation',
            homepage_url=self.application.homepage_url,
            essay_id=self.application.current_essay_id,
            essay=self.application.current_essay,
            annotated_essay_quantity=self.application.annotated_essay_quantity,
            sum=self.application.essay_quantity,
            annotation_essay_ratio=self.application.annotation_essay_ratio,
        )

    def get_progress(self):
        progress = self.application.db.essay_progress
        progress_record = progress.find_one()
        self.application.annotated_essay_quantity = progress_record['annotated_essay_quantity']
        self.application.annotation_essay_ratio = float(100 * self.application.annotated_essay_quantity / self.application.essay_quantity)

    def get_essay(self):
        candidates = self.application.db.essay_candidates
        essay_record = candidates.find_one()
        self.application.current_essay_id = essay_record['essay_id']
        self.application.current_essay = essay_record['essay']


class MarkSubmitHandler(tornado.web.RequestHandler):
    def post(self):
        essay_id = int(self.get_argument('essay_id'))
        overall_score = int(self.get_argument('overall_score'))
        vocabulary_score = int(self.get_argument('vocabulary_score'))
        sentence_score = int(self.get_argument('sentence_score'))
        structure_score = int(self.get_argument('structure_score'))
        content_score = int(self.get_argument('content_score'))

        mark_record = {}
        mark_record['annotator'] = 'sjyan'
        mark_record['essay_id'] = essay_id
        mark_record['overall_score'] = overall_score
        mark_record['vocabulary_score'] = vocabulary_score
        mark_record['sentence_score'] = sentence_score
        mark_record['structure_score'] = structure_score
        mark_record['content_score'] = content_score

        self.write_db(mark_record)
        self.get_essay()
        self.get_progress()

        response = {}
        response['essay'] = self.application.current_essay
        response['essay_id'] = self.application.current_essay_id
        response['annotated_essay_quantity'] = self.application.annotated_essay_quantity
        response['annotation_essay_ratio'] = self.application.annotation_essay_ratio

        self.write(response)

    def get_progress(self):
        progress = self.application.db.essay_progress
        progress_record = progress.find_one()
        self.application.annotated_essay_quantity = progress_record['annotated_essay_quantity']
        self.application.annotation_essay_ratio = float(100 * self.application.annotated_essay_quantity / self.application.essay_quantity)
    
    def get_essay(self):
        candidates = self.application.db.essay_candidates
        essay_record = candidates.find_one()
        self.application.current_essay_id = essay_record['essay_id']
        self.application.current_essay = essay_record['essay']

    def write_db(self, record):
        data = self.application.db.essay_data
        candidates = self.application.db.essay_candidates
        progress = self.application.db.essay_progress
        essay_id = record['essay_id']

        if data.find_one({'essay_id': essay_id}) == None:
            data.insert_one(record)

            # annotated_essay_quantity + 1
            progress.update_one(
                {},
                {'$inc': 
                    {
                        'annotated_essay_quantity': 1
                    }
                }
            )

            # update annotation list
            progress_record = progress.find_one()
            annotation_list = progress_record['annotation_list']
            annotation_list.append(essay_id)
            progress.update_one(
                {},
                {'$set': 
                    {
                        'annotation_list': annotation_list
                    }
                }
            )
        else:
            data.update_one(
                {'essay_id': essay_id},
                {'$set': record}
            )

    def close_db(self):
        self.application.conn.close()


class MarkPreviousHandler(tornado.web.RequestHandler):
    def post(self):
        essay_id = int(self.get_argument('essay_id'))

        self.get_essay(essay_id - 1)
        self.write(self.application.current_essay)

    def get_essay(self, essay_id):
        candidates = self.application.db.essay_candidates
        essay_record = candidates.find_one({"essay_id": essay_id})
        self.application.current_essay_id = essay_record['essay_id']
        self.application.current_essay = essay_record['essay']


class MarkNextHandler(tornado.web.RequestHandler):
    def post(self):
        essay_id = int(self.get_argument('essay_id'))

        self.get_essay(essay_id + 1)
        self.write(self.application.current_essay)

    def get_essay(self, essay_id):
        candidates = self.application.db.essay_candidates
        essay_record = candidates.find_one({"essay_id": essay_id})
        self.application.current_essay_id = essay_record['essay_id']
        self.application.current_essay = essay_record['essay']
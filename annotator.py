# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-02 Friday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

import datetime
import os.path
import json
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options, parse_command_line
from pprint import pprint
import pymongo
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId

define("address", default="10.200.26.84", help="run on the given address", type=str)    # 17zuoye office: 10.200.26.84
define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode", type=bool)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/mark', MarkHandler),
            (r'/mark_previous', MarkPreviousHandler),
            (r'/mark_next', MarkNextHandler),
            (r'/ocr', OCRHandler),
            (r'/ocr_previous', OCRPreviousHandler),
            (r'/ocr_next', OCRNextHandler),
        ]
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            debug=options.debug
        )
        super(Application, self).__init__(handlers, **settings)

        self.essay_path = "./data/essay.txt"
        self.essays = [line.strip() for line in open(self.essay_path)]
        self.essay_quantity = len(self.essays)
        self.annotated_quantity = 0
        self.annotation_ratio = 0.0
        self.current_essay_id = 0
        self.current_essay = 'Essay Placeholder'
        self.ocr_path = "./data/ocr.xml"

        self.connect_db()

    def connect_db(self):
        self.conn = MongoClient("localhost", 27017)
        self.db = self.conn.annotation

        if "essay_candidates" not in self.db.collection_names():
            self.db.essay_candidates
            candidates = []

            with open(self.essay_path, 'r') as essay_file:
                essay_id = 0       # essay_id == line_number
                for line in essay_file:
                    line = line.strip()
                    candidate_record = {}
                    candidate_record['essay_id'] = essay_id
                    candidate_record['essay'] = line
                    candidate_record['annotator_counter'] = 0
                    candidates.append(candidate_record)
                    essay_id += 1
                self.db.essay_candidates.insert_many(candidates)
        
        if "essay_marked" not in self.db.collection_names():
            self.db.essay_marked

        if "essay_data" not in self.db.collection_names():
            self.db.essay_data
        
        if "essay_progress" not in self.db.collection_names():
            self.db.essay_progress
            # one annotator one record
            self.db.essay_progress.insert_one({'annotator': 'sjyan', 'annotated_quantity': 0, 'annotation_list': []})



class MarkHandler(tornado.web.RequestHandler):
    def post(self):
        essay_id = int(self.get_argument('essay_id'))
        overall_score = int(self.get_argument('overall_score'))
        vocabulary_score = int(self.get_argument('vocabulary_score'))
        sentence_score = int(self.get_argument('sentence_score'))
        structure_score = int(self.get_argument('structure_score'))
        content_score = int(self.get_argument('content_score'))

        mark_record = {}
        mark_record['essay_id'] = essay_id
        mark_record['overall_score'] = overall_score
        mark_record['vocabulary_score'] = vocabulary_score
        mark_record['sentence_score'] = sentence_score
        mark_record['structure_score'] = structure_score
        mark_record['content_score'] = content_score

        self.get_essay(essay_id + 1)
        self.write_db(mark_record)
        self.update_progress()

        response = {}
        response['essay'] = self.application.current_essay
        response['annotated_quantity'] = self.application.annotated_quantity
        response['annotation_ratio'] = self.application.annotation_ratio

        self.write(response)

    def update_progress(self):
        progress = self.application.db.essay_progress
        progress_record = progress.find_one()
        self.application.annotated_quantity = progress_record['annotated_quantity']
        self.application.annotation_ratio = float(100 * self.application.annotated_quantity / self.application.essay_quantity)
    
    def get_essay(self, essay_id):
        candidate = self.application.db.essay_candidates
        essay_record = candidate.find_one({"essay_id": essay_id})
        self.application.current_essay_id = essay_record['essay_id']
        self.application.current_essay = essay_record['essay']

    def write_db(self, record):
        data = self.application.db.essay_data
        candidate = self.application.db.essay_candidates
        progress = self.application.db.essay_progress
        essay_id = record['essay_id']

        if data.find_one({'essay_id': essay_id}) == None:
            data.insert_one(record)
            progress.update_one(
                {'annotator': 'sjyan'},
                {'$inc': 
                    {
                        'annotated_quantity': 1
                    }
                }
            )

            progress_record = progress.find_one({'annotator': 'sjyan'})
            annotation_list = progress_record['annotation_list']
            annotation_list.append(essay_id)
            progress.update_one(
                {'annotator': 'sjyan'},
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


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.get_progress()
        self.get_essay()

        self.render(
            'mark.html',
            title='Essay Grading Annotation',
            essay_id=self.application.current_essay_id,
            essay=self.application.current_essay,
            annotated_quantity=self.application.annotated_quantity,
            sum=self.application.essay_quantity,
            annotation_ratio=self.application.annotation_ratio,
        )

    def get_progress(self):
        progress = self.application.db.essay_progress
        progress_record = progress.find_one()
        self.application.annotated_quantity = progress_record['annotated_quantity']
        self.application.annotation_ratio = float(100 * self.application.annotated_quantity / self.application.essay_quantity)

    def get_essay(self):
        candidate = self.application.db.essay_candidates
        essay_record = candidate.find_one()
        self.application.current_essay_id = essay_record['essay_id']
        self.application.current_essay = essay_record['essay']


class MarkPreviousHandler(tornado.web.RequestHandler):
    def post(self):
        essay_id = int(self.get_argument('essay_id'))

        self.get_essay(essay_id - 1)
        self.write(self.application.current_essay)

    def get_essay(self, essay_id):
        candidate = self.application.db.essay_candidates
        essay_record = candidate.find_one({"essay_id": essay_id})
        self.application.current_essay_id = essay_record['essay_id']
        self.application.current_essay = essay_record['essay']


class MarkNextHandler(tornado.web.RequestHandler):
    def post(self):
        essay_id = int(self.get_argument('essay_id'))

        self.get_essay(essay_id + 1)
        self.write(self.application.current_essay)

    def get_essay(self, essay_id):
        candidate = self.application.db.essay_candidates
        essay_record = candidate.find_one({"essay_id": essay_id})
        self.application.current_essay_id = essay_record['essay_id']
        self.application.current_essay = essay_record['essay']


class OCRHandler(tornado.web.RequestHandler):
    def get(self):
        print()

class OCRPreviousHandler(tornado.web.RequestHandler):
    def post(self):
        print()


class OCRNextHandler(tornado.web.RequestHandler):
    def post(self):
        print()





def main():
    print("Server Running on http://" + str(options.address) + ":" + str(options.port))
    print("Press Ctrl+C to Close")
    tornado.options.parse_command_line()
    application = Application()
    application.listen(options.port, address=options.address)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
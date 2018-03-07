# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-02 Friday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

import datetime
import os.path
import json
import base64
import requests
from requests_toolbelt import MultipartEncoder
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

define("address", default="localhost", help="run on the given address", type=str)    # 17zuoye office: 10.200.26.84
define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode", type=bool)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/previous', PreviousHandler),
            (r'/next', NextHandler),
            (r'/mark', MarkHandler),
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

        self.connect_db()

    def connect_db(self):
        self.conn = MongoClient("localhost", 27017)
        self.db = self.conn.annotation

        if "candidate" not in self.db.collection_names():
            self.db.candidate
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
                self.db.candidate.insert_many(candidates)

        if "data" not in self.db.collection_names():
            self.db.data
        
        if "progress" not in self.db.collection_names():
            self.db.progress
            self.db.progress.insert_one({'annotated_quantity': 0})


class MainHandler(tornado.web.RequestHandler):
    def get_progress(self):
        progress = self.application.db.progress
        progress_record = progress.find_one()
        self.application.annotated_quantity = progress_record['annotated_quantity']
        self.application.annotation_ratio = float(self.application.annotated_quantity / self.application.essay_quantity)

    def get(self):
        self.get_progress()

        self.render(
            'index.html',
            title='Essay Grading Annotation',
            essay_id=self.application.current_essay_id,
            essay=self.application.current_essay,
            annotated_quantity=self.application.annotated_quantity,
            sum=self.application.essay_quantity,
            annotation_ratio=self.application.annotation_ratio,
        )


class PreviousHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            'index.html',
            title='Essay Grading Annotation',
            essay_id='001',
            essay='Essay placeholder.',
            annotated_quantity=0,
            sum=60000,
            annotation_ratio=0,
        )


class NextHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            'index.html',
            title='Essay Grading Annotation',
            essay_id='001',
            essay='Essay placeholder.',
            annotated_quantity=0,
            sum=60000,
            annotation_ratio=0,
        )


class MarkHandler(tornado.web.RequestHandler):
    def post(self):
        overall_score = self.get_argument('overall_score')
        vocabulary_score = self.get_argument('vocabulary_score')
        sentence_score = self.get_argument('sentence_score')
        structure_score = self.get_argument('structure_score')
        content_score = self.get_argument('content_score')






def main():
    print("Server Running on http://" + str(options.address) + ":" + str(options.port))
    print("Press Ctrl+C to Close")
    tornado.options.parse_command_line()
    application = Application()
    application.listen(options.port, address=options.address)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
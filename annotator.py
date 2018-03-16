# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-02 Friday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

from handlers.main_handler import MainHandler
from handlers.mark_handler import MarkHandler, MarkNextHandler, MarkPreviousHandler, MarkSubmitHandler
from handlers.ocr_handler import OCRHandler, OCRNextHandler, OCRPreviousHandler, OCRSubmitHandler

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
            (r'/mark_submit', MarkSubmitHandler),
            (r'/mark_previous', MarkPreviousHandler),
            (r'/mark_next', MarkNextHandler),
            (r'/ocr', OCRHandler),
            (r'/ocr_submit', OCRSubmitHandler),
            (r'/ocr_previous', OCRPreviousHandler),
            (r'/ocr_next', OCRNextHandler),
        ]
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            debug=options.debug
        )
        super(Application, self).__init__(handlers, **settings)

        self.homepage_url = 'http://' + str(options.address) + ":" + str(options.port)

        # essay grading annotation
        self.mark_url = 'http://' + str(options.address) + ':' + str(options.port) + '/mark'
        self.essay_path = './data/essay.txt'
        self.essays = [line.strip() for line in open(self.essay_path, 'r')]
        self.essay_flag = True  # True means essay_candidates is not empty
        self.essay_quantity = len(self.essays)
        self.annotated_essay_quantity = 0
        self.annotation_essay_ratio = 0.0
        self.current_essay_id = 0
        self.current_essay = 'Essay Placeholder'

        # ocr result correction
        self.ocr_url = 'http://' + str(options.address) + ':' + str(options.port) + '/ocr'
        self.ocr_path = './data/ocr.txt'
        self.ocrs = json.load(open(self.ocr_path, 'r'))
        self.ocr_flag = True    # True means ocr_candidates is not empty
        self.ocr_quantity = len(self.ocrs)
        self.corrected_ocr_quantity = 0
        self.corrected_ocr_ratio = 0.0
        self.current_ocr_id = 0
        self.current_image_url = ''
        self.image_url_prefix = 'http://klximg.oss-cn-beijing.aliyuncs.com/scanimage/'
        self.current_ocr_essay = 'OCR Result Placeholder'

        self.connect_db()

    def connect_db(self):
        self.conn = MongoClient("localhost", 27017)
        self.db = self.conn.annotation

        # essay mark annotation
        if "essay_candidates" not in self.db.collection_names():
            self.db.essay_candidates
            essay_candidates = []
            essay_id = 0       # essay_id == line_number
            for essay in self.essays:
                candidate_record = {}
                candidate_record['essay_id'] = essay_id
                candidate_record['essay'] = essay
                candidate_record['annotator_counter'] = 0
                essay_candidates.append(candidate_record)
                essay_id += 1
            self.db.essay_candidates.insert_many(essay_candidates)
        if "essay_marked" not in self.db.collection_names():
            self.db.essay_marked
        if "essay_data" not in self.db.collection_names():
            self.db.essay_data
        if "essay_progress" not in self.db.collection_names():
            self.db.essay_progress
            self.db.essay_progress.insert_one({'annotated_essay_quantity': 0, 'annotation_list': []})

        # ocr result correction
        if "ocr_candidates" not in self.db.collection_names():
            self.db.ocr_candidates
            ocr_id = 0      # ocr_id starts from 0
            for ocr_dict in self.ocrs:
                ocr_dict['ocr_id'] = ocr_id
                ocr_id += 1
            self.db.ocr_candidates.insert_many(self.ocrs)
        if "ocr_marked" not in self.db.collection_names():
            self.db.ocr_marked
        if "ocr_data" not in self.db.collection_names():
            self.db.ocr_data
        if "ocr_progress" not in self.db.collection_names():
            self.db.ocr_progress
            self.db.ocr_progress.insert_one({'corrected_ocr_quantity': 0, 'annotation_list': []})


def main():
    print("Server Running on http://" + str(options.address) + ":" + str(options.port))
    print("Press Ctrl+C to Close")
    tornado.options.parse_command_line()
    application = Application()
    application.listen(options.port, address=options.address)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
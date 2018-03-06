# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-02 Friday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.


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
        self.conn = MongoClient("localhost", 27017)
        self.db = self.conn["definitions"]


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            'index.html',
            title='Essay Grading Annotation',
            essay_id='001',
            essay='Essay placeholder',
            annotated_quantity=0,
            sum=60000,
            annotation_ratio=0,
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
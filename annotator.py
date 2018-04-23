# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-02 Friday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

from handlers.main import MainHandler
from handlers.sign import SigninHandler, SignoutHandler
from handlers.billing import BillingHandler
from handlers.qc import QCHandler
from handlers.view import ViewHandler
from handlers.mark import MarkHandler, MarkNextHandler, MarkPreviousHandler, MarkSubmitHandler, MarkJumpHandler
from handlers.ocr import OCRHandler, OCRNextHandler, OCRPreviousHandler, OCRSubmitHandler, OCRJumpHandler
from handlers.grammar import GrammarHandler

import os.path
import json
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options, parse_command_line
import pymongo
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId

import logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] (%(asctime)s) (%(name)s) %(message)s',
    handlers=[
        logging.FileHandler('./data/log/annotator.log', encoding='utf8'),
        logging.StreamHandler()
    ])
logger = logging.getLogger(__name__)

define("address", default="localhost", help="run on the given address", type=str)    # 17zuoye office: 10.200.26.84    docker: 10.0.5.40
define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode", type=bool)
define("xsrf", default=True, help="use xsrf protection", type=bool)
define("cookie", default="8Vz8CPxFTlGl2YYqKtD0btnWEsZjDUtJklRHc7p85yA=", help="cookie secret", type=str)
define("ip", default="10.0.5.40", help="remote server ip address", type=str)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/signin', SigninHandler),
            (r'/signout', SignoutHandler),
            (r'/billing', BillingHandler),
            (r'/qc', QCHandler),
            (r'/view', ViewHandler),
            (r'/mark', MarkHandler),
            (r'/mark_submit', MarkSubmitHandler),
            (r'/mark_previous', MarkPreviousHandler),
            (r'/mark_next', MarkNextHandler),
            (r'/mark_jump', MarkJumpHandler),
            (r'/ocr', OCRHandler),
            (r'/ocr_submit', OCRSubmitHandler),
            (r'/ocr_previous', OCRPreviousHandler),
            (r'/ocr_next', OCRNextHandler),
            (r'/ocr_jump', OCRJumpHandler),
            (r'/grammar', GrammarHandler),
        ]
        settings = {
            'static_path': os.path.join(os.path.dirname(__file__), "static"),
            'template_path': os.path.join(os.path.dirname(__file__), "templates"),
            "login_url": "/signin",
            'debug': options.debug,
            'cookie_secret': options.cookie,
            # 'xsrf_cookies': options.xsrf,
        }
        super(Application, self).__init__(handlers, **settings)

        # essay grading annotation
        self.essay_path = './data/essay/essay.txt'
        self.essays = [line.strip() for line in open(self.essay_path, 'r')]
        self.essay_flag = True  # True means essay_candidates is not empty
        self.essay_quantity = len(self.essays)
        self.annotated_essay_quantity = 0
        self.annotation_essay_ratio = 0.0
        self.current_essay_id = 0
        self.current_essay = 'Essay Placeholder'
        self.essay_annotator_mark = '' # how many people have annotated this essay
        self.essay_quantity_for_billing = {}
        self.screened_essay_quantity_for_billing = {}

        # ocr result annotation
        self.ocr_path = './data/ocr/ocr.txt'
        self.ocrs = json.load(open(self.ocr_path, 'r'))
        self.ocr_flag = True    # True means ocr_candidates is not empty
        self.ocr_quantity = len(self.ocrs)
        self.corrected_ocr_quantity = 0
        self.corrected_ocr_ratio = 0.0
        self.current_ocr_id = 0
        self.current_image_url = ''
        self.image_url_prefix = 'http://klximg.oss-cn-beijing.aliyuncs.com/scanimage/'
        self.current_ocr_essay = 'OCR Result Placeholder'
        self.ocr_annotator_mark = ''
        self.ocr_quantity_for_billing = {}
        self.screened_ocr_quantity_for_billing = {}

        # grammar check annotation
        self.checked_grammar_ratio = 0.0

        self.load_accounts()
        self.connect_db()

    def load_accounts(self):
        try:
            self.account_path = './data/account.txt'
            self.accounts = {}  # [{account: password}]
            with open(self.account_path, 'r') as accounts_file:
                for line in accounts_file:
                    line = line.strip()
                    (account, password) = line.split(' ')
                    self.accounts[account] = password
            # print('Accounts:')
            # print(json.dumps(self.accounts, indent=4, sort_keys=True))
        except Exception as e:
            logger.error(e)
            raise

    def connect_db(self):
        try:
            self.conn = MongoClient(options.ip, 27017)
            self.db = self.conn.annotation
            self.init_mark_db()
            self.init_ocr_db()
            self.init_grammar_db()
        except Exception as e:
            logger.error(e)
            raise

    def init_mark_db(self):
        '''essay mark annotation'''
        if "essay_candidates" not in self.db.collection_names():
            self.db.essay_candidates
            essay_candidates = []
            essay_id = 0       # essay_id == line_number
            for essay in self.essays:
                candidate_record = {}
                candidate_record['essay_id'] = essay_id
                candidate_record['essay'] = essay
                candidate_record['annotator_counter'] = 0
                candidate_record['annotator'] = ''
                essay_candidates.append(candidate_record)
                essay_id += 1
            self.db.essay_candidates.insert_many(essay_candidates)
        if "essay_marked" not in self.db.collection_names():
            self.db.essay_marked
        if "essay_data" not in self.db.collection_names():
            self.db.essay_data
        if "essay_unchecked" not in self.db.collection_names():
            self.db.essay_unchecked
        if "essay_progress" not in self.db.collection_names():
            self.db.essay_progress
            for account in self.accounts.keys():
                self.db.essay_progress.insert_one({'annotated_essay_quantity': 0, 'annotation_list': [], 'annotator':account})
        else:
            for account in self.accounts.keys():
                if self.db.essay_progress.find_one({'annotator':account}) == None:
                    self.db.essay_progress.insert_one({'annotated_essay_quantity': 0, 'annotation_list': [], 'annotator':account})
        
    def init_ocr_db(self):
        '''ocr result correction'''
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

    def init_grammar_db(self):
        pass

def main():
    print("--------------------------------------------------------------------------------")
    print("Server Running on http://" + str(options.address) + ":" + str(options.port))
    print("Press Ctrl+C to Close")
    tornado.options.parse_command_line()
    application = Application()
    application.listen(options.port, address=options.address)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
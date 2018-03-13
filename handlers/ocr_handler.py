# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-13 Tuesday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

import tornado.web

class OCRHandler(tornado.web.RequestHandler):
    def get(self):
        self.get_progress()
        self.get_ocr()

        self.render(
            'ocr.html',
            title='OCR Result Correction',
            essay_id=self.application.current_essay_id,
            essay=self.application.current_essay,
            annotated_essay_quantity=self.application.annotated_essay_quantity,
            sum=self.application.essay_quantity,
            annotation_essay_ratio=self.application.annotation_essay_ratio,
        )


class OCRSubmitHandler(tornado.web.RequestHandler):
    def post(self):
        print()


class OCRPreviousHandler(tornado.web.RequestHandler):
    def post(self):
        print()


class OCRNextHandler(tornado.web.RequestHandler):
    def post(self):
        print()
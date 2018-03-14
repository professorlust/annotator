# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-13 Tuesday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

import tornado.web

class OCRHandler(tornado.web.RequestHandler):
    def get(self):
        # self.get_progress()
        # self.get_ocr()

        self.render(
            'ocr.html',
            title='OCR Result Correction',
            image_id=self.application.current_iamge_id,
            image_url=self.application.current_iamge_url,
            corrected_ocr_quantity=self.application.corrected_ocr_quantity,
            sum=self.application.ocr_quantity,
            corrected_ocr_ratio=self.application.corrected_ocr_ratio,
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
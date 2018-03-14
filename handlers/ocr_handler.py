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
            ocr_id=self.application.current_ocr_id,
            image_url=self.application.current_image_url,
            ocr_essay=self.application.current_ocr_essay,
            ocr_correction=self.application.current_ocr_essay,
            corrected_ocr_quantity=self.application.corrected_ocr_quantity,
            sum=self.application.ocr_quantity,
            corrected_ocr_ratio=self.application.corrected_ocr_ratio,
        )
    
    def get_progress(self):
        progress = self.application.db.ocr_progress
        progress_record = progress.find_one()
        self.application.corrected_ocr_quantity = progress_record['corrected_ocr_quantity']
        self.application.corrected_ocr_ratio = float(100 * self.application.corrected_ocr_quantity / self.application.ocr_quantity)

    def get_ocr(self):
        candidates = self.application.db.ocr_candidates
        ocr_record = candidates.find_one()
        self.application.current_ocr_id = ocr_record['ocr_id']
        self.application.current_image_url = self.application.image_url_prefix + ocr_record['image_id']
        self.application.current_ocr_essay = ocr_record['essay']


class OCRSubmitHandler(tornado.web.RequestHandler):
    def post(self):
        print()


class OCRPreviousHandler(tornado.web.RequestHandler):
    def post(self):
        essay_id = int(self.get_argument('essay_id'))

        self.get_essay(essay_id - 1)
        self.write(self.application.current_essay)

    def get_essay(self, essay_id):
        candidates = self.application.db.essay_candidates
        essay_record = candidates.find_one({"essay_id": essay_id})
        self.application.current_essay_id = essay_record['essay_id']
        self.application.current_essay = essay_record['essay']


class OCRNextHandler(tornado.web.RequestHandler):
    def post(self):
        essay_id = int(self.get_argument('essay_id'))

        self.get_essay(essay_id + 1)
        self.write(self.application.current_essay)

    def get_essay(self, essay_id):
        candidates = self.application.db.essay_candidates
        essay_record = candidates.find_one({"essay_id": essay_id})
        self.application.current_essay_id = essay_record['essay_id']
        self.application.current_essay = essay_record['essay']
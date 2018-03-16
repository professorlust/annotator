# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-13 Tuesday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.get_progress()

        self.render(
            'main.html',
            title='17zuoye NLP Annotation Platform',
            annotation_essay_ratio=self.application.annotation_essay_ratio,
            corrected_ocr_ratio=self.application.corrected_ocr_ratio,
        )
    
    def get_progress(self):
        essay_progress = self.application.db.essay_progress
        essay_progress_record = essay_progress.find_one()
        self.application.annotated_essay_quantity = essay_progress_record['annotated_essay_quantity']
        self.application.annotation_essay_ratio = float(100 * self.application.annotated_essay_quantity / self.application.essay_quantity)

        ocr_progress = self.application.db.ocr_progress
        ocr_progress_record = ocr_progress.find_one()
        self.application.corrected_ocr_quantity = ocr_progress_record['corrected_ocr_quantity']
        self.application.corrected_ocr_ratio = float(100 * self.application.corrected_ocr_quantity / self.application.ocr_quantity)
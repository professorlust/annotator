# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-19 Monday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

from .base import BaseHandler

class BillingHandler(BaseHandler):
    def get(self):
        self.get_essay_quantity()
        self.get_ocr_quantity()
        self.render(
            'billing.html',
            title='Billing System',
            annotators = self.application.accounts.keys(),
            essay_quantity_for_billing = self.application.essay_quantity_for_billing,
            ocr_quantity_for_billing = self.application.ocr_quantity_for_billing
        )
    
    def get_essay_quantity(self):
        data = self.application.db.essay_data
        annotators = self.application.accounts.keys()
        for annotator in annotators:
            self.application.essay_quantity_for_billing[annotator] = data.find({'annotator':annotator}).count()

    def get_ocr_quantity(self):
        data = self.application.db.ocr_data
        annotators = self.application.accounts.keys()
        for annotator in annotators:
            self.application.ocr_quantity_for_billing[annotator] = data.find({'annotator':annotator}).count()

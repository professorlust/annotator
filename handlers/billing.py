# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-19 Monday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

from .base import BaseHandler
import calendar
from datetime import date

class BillingHandler(BaseHandler):
    def get(self):
        self.get_essay_quantity()
        self.get_ocr_quantity()
        self.render(
            'billing.html',
            title='Billing System',
            start_date='',
            end_date='',
            annotators=self.application.accounts.keys(),
            essay_quantity_for_billing=self.application.essay_quantity_for_billing,
            ocr_quantity_for_billing=self.application.ocr_quantity_for_billing,
        )
    
    def post(self):
        start_date_str = self.get_argument('start_date')
        end_date_str = self.get_argument('end_date')
        start_date_list = start_date_str.split('/')
        end_date_list = end_date_str.split('/')

        start_d = date(int(start_date_list[0]), int(start_date_list[1]), int(start_date_list[2]))
        start_timestamp = calendar.timegm(start_d.timetuple())
        end_d = date(int(end_date_list[0]), int(end_date_list[1]), int(end_date_list[2]))
        end_timestamp = calendar.timegm(end_d.timetuple())

        self.screen_essay_quantity(start_timestamp, end_timestamp)
        self.screen_ocr_quantity(start_timestamp, end_timestamp)

        response = {}
        response['annotators'] = self.application.accounts
        response['essay_progress'] = self.application.screened_essay_quantity_for_billing
        response['ocr_progress'] = self.application.screened_ocr_quantity_for_billing
        self.write(response)
        
    
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
    
    def screen_essay_quantity(self, start, end):
        data = self.application.db.essay_data
        annotators = self.application.accounts.keys()
        for annotator in annotators:
            self.application.screened_essay_quantity_for_billing[annotator] = data.find({'annotator':annotator, "time": {"$gte": start, "$lt": end}}).count()
    
    def screen_ocr_quantity(self, start, end):
        data = self.application.db.ocr_data
        annotators = self.application.accounts.keys()
        for annotator in annotators:
            self.application.screened_ocr_quantity_for_billing[annotator] = data.find({'annotator':annotator, "time": {"$gte": start, "$lt": end}}).count()

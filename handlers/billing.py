# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-19 Monday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

from .base import BaseHandler
import time
import datetime
import calendar

class BillingHandler(BaseHandler):
    def get(self):
        a_week_ago, now = self.get_default_time()

        self.get_essay_quantity()
        self.get_ocr_quantity()
        self.render(
            'billing.html',
            title='Billing System',
            start_time=a_week_ago,
            end_time=now,
            annotators=self.application.accounts.keys(),
            essay_quantity_for_billing=self.application.essay_quantity_for_billing,
            ocr_quantity_for_billing=self.application.ocr_quantity_for_billing,
        )
    
    def post(self):
        start_str = self.get_argument('start_time')
        end_str = self.get_argument('end_time')

        start_timestamp = time.mktime(datetime.datetime.strptime(start_str, "%Y/%m/%d/%H/%M/%S").timetuple())
        end_timestamp = time.mktime(datetime.datetime.strptime(end_str, "%Y/%m/%d/%H/%M/%S").timetuple())

        self.screen_essay_quantity(start_timestamp, end_timestamp)
        self.screen_ocr_quantity(start_timestamp, end_timestamp)

        response = {}
        response['start_timestamp'] = start_timestamp
        response['end_timestamp'] = end_timestamp
        response['annotators'] = self.application.accounts
        response['essay_progress'] = self.application.screened_essay_quantity_for_billing
        response['ocr_progress'] = self.application.screened_ocr_quantity_for_billing
        self.write(response)
        
    def get_default_time(self):
        current = datetime.datetime.now()
        cur_time = str(current.year) + '/' + str(current.month) + '/' + str(current.day) + '/' + str(current.hour) + '/' + str(current.minute) + '/' + str(current.second)
        a_week_ago = current - datetime.timedelta(days=7)
        a_week_ago_time = str(a_week_ago.year) + '/' + str(a_week_ago.month) + '/' + str(a_week_ago.day) + '/' + str(a_week_ago.hour) + '/' + str(a_week_ago.minute) + '/' + str(a_week_ago.second)

        return a_week_ago_time, cur_time

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

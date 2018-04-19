# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-04-12 Thursday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

from .base import *
import calendar
import datetime
from datetime import date

class ViewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        yesterday_date, today_date = self.get_default_date()

        self.render(
            'view.html',
            title='God View',
            annotator='',
            start_date=yesterday_date,
            end_date=today_date
        )

    def post(self):
        start_date = self.get_argument('start_date')
        end_date = self.get_argument('end_date')
        start_timestamp = self.convert_date(start_date)
        end_timestamp = self.convert_date(end_date)
        annotator = self.get_argument('annotator')
        if self.is_annotator_valid(annotator):
            screen_essay_record = self.get_essay_record()
            screen_ocr_record = self.get_ocr_record()
        else:
            screen_essay_record = []
            screen_ocr_record = []

        response = {}
        response['start_timestamp'] = start_timestamp
        response['end_timestamp'] = end_timestamp
        response['screen_essay_record'] = screen_essay_record
        response['screen_ocr_record'] = screen_ocr_record
        response['essay_record_length'] = len(screen_essay_record)
        response['ocr_record_length'] = len(screen_ocr_record)
        response['annotator_valid_flag'] = self.is_annotator_valid(annotator)
        self.write(response)

    def get_default_date(self):
        today = datetime.datetime.now()
        today_date = str(today.year) + '/' + str(today.month) + '/' + str(today.day)
        yesterday = today - datetime.timedelta(days=1)
        yesterday_date = str(yesterday.year) + '/' + str(yesterday.month) + '/' + str(yesterday.day)
        return yesterday_date, today_date

    def convert_date(self, date_str):
        date_list = date_str.split('/')
        d = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        timestamp = calendar.timegm(d.timetuple())
        return timestamp

    def is_annotator_valid(self,annotator):
        if annotator in self.application.accounts.keys():
            return True               
        else:
            return False
    
    def get_essay_record(self):
        data = self.application.db.essay_data
        annotator = self.get_argument('annotator')
        essay_record = data.find({'annotator': annotator})
        if essay_record == None:
            screen_essay_record = []
        else:
            screen_essay_record = []
            for record in essay_record:
                del record['_id']
                screen_essay_record.append(record)
        print(screen_essay_record)
        return screen_essay_record
        
    def get_ocr_record(self):
        data = self.application.db.ocr_data
        annotator = self.get_argument('annotator')
        ocr_record = data.find({'annotator': annotator})
        if ocr_record == None:
            screen_ocr_record = []
        else:
            screen_ocr_record = []
            for record in ocr_record:
                del record['_id']
                screen_ocr_record.append(record)
        print(screen_ocr_record)
        return screen_ocr_record
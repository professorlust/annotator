# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-04-12 Thursday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

from .base import *
import time
import datetime
import calendar

class ViewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        yesterday_time, today_time = self.get_default_time()

        self.render(
            'view.html',
            title='God View',
            annotators=self.application.accounts.keys(),
            start_time=yesterday_time,
            end_time=today_time
        )

    def post(self):
        start_time = self.get_argument('start_time')
        end_time = self.get_argument('end_time')
        start_timestamp = self.convert_date(start_time)
        end_timestamp = self.convert_date(end_time)
        annotator = self.get_argument('annotator')
        if self.is_annotator_valid(annotator):
            screen_essay_record = self.get_essay_record(start_timestamp, end_timestamp)
            screen_ocr_record = self.get_ocr_record(start_timestamp, end_timestamp)
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
    
    def get_default_time(self):
        current = datetime.datetime.now()
        cur_time = str(current.year) + '/' + str(current.month) + '/' + str(current.day) + '/' + str(current.hour) + '/' + str(current.minute) + '/' + str(current.second)
        ago = current - datetime.timedelta(days=1)
        ago_time = str(ago.year) + '/' + str(ago.month) + '/' + str(ago.day) + '/' + str(ago.hour) + '/' + str(ago.minute) + '/' + str(ago.second)
        return ago_time, cur_time

    def convert_date(self, time_str):
        timestamp = time.mktime(datetime.datetime.strptime(time_str, "%Y/%m/%d/%H/%M/%S").timetuple())
        return timestamp

    def is_annotator_valid(self,annotator):
        if annotator in self.application.accounts.keys():
            return True               
        else:
            return False
    
    def get_essay_record(self,start,end):
        data = self.application.db.essay_data
        annotator = self.get_argument('annotator')
        essay_record = data.find({'annotator': annotator, "time": {"$gte": start, "$lt": end}})
        if essay_record == None:
            screen_essay_record = []
        else:
            screen_essay_record = []
            for record in essay_record:
                del record['_id']
                screen_essay_record.append(record)
        return screen_essay_record
        
    def get_ocr_record(self,start,end):
        data = self.application.db.ocr_data
        annotator = self.get_argument('annotator')
        ocr_record = data.find({'annotator': annotator, "time": {"$gte": start, "$lt": end}})
        if ocr_record == None:
            screen_ocr_record = []
        else:
            screen_ocr_record = []
            for record in ocr_record:
                del record['_id']
                screen_ocr_record.append(record)
        return screen_ocr_record
# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-04-13 Friday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

from .base import *
import calendar
import datetime
from datetime import date
from numpy import NaN
from sklearn.metrics import cohen_kappa_score


class QCHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        yesterday_date, today_date = self.get_default_date()
        self.render(
            'qc.html',
            title='Quality Control',
            start_date=yesterday_date,
            end_date=today_date,
            qwk=self.calculate_qwk(yesterday_date, today_date, option='default'),
        )
    
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

    def get_all_progress(self):
        progress_essay_grading = []
        essay_progress_collection = self.application.db.essay_progress
        for account in self.application.accounts:
            progress = essay_progress_collection.find_one({'annotator': account})['annotation_list']
            progress_essay_grading.append(progress)

        all_progress_essay_grading = set(progress_essay_grading[0])
        for progress in progress_essay_grading:
            all_progress_essay_grading = set(progress).intersection(all_progress_essay_grading)
        return all_progress_essay_grading

    def calculate_qwk(self, start_date, end_date, option=None):
        start_timestamp = self.convert_date(start_date)
        end_timestamp = self.convert_date(end_date)
        essay_data_collection = self.application.db.essay_data
        all_progress_essay_grading = self.get_all_progress()
        y1 = []
        y2 = []

        if option == 'default':
            pass
        else:
            pass

        qwk = cohen_kappa_score(y1, y2, weights='quadratic')
        return qwk
    

    def post(self):
        start_date_str = self.get_argument('start_date')
        end_date_str = self.get_argument('end_date')
        qwk = self.calculate_qwk(start_timestamp, end_timestamp)

        response = {}
        response['start_timestamp'] = start_timestamp
        response['end_timestamp'] = end_timestamp
        response['qwk'] = qwk
        self.write(response)


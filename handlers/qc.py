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
            vocabulary_qwk=self.calculate_qwk(option='default', dim_name='vocabulary_score'),
            vocabulary_lwk=self.calculate_lwk(option='default', dim_name='vocabulary_score'),
            sentence_qwk=self.calculate_qwk(option='default', dim_name='sentence_score'),
            sentence_lwk=self.calculate_lwk(option='default', dim_name='sentence_score'),
            structure_qwk=self.calculate_qwk(option='default', dim_name='structure_score'),
            structure_lwk=self.calculate_lwk(option='default', dim_name='structure_score'),
            content_qwk=self.calculate_qwk(option='default', dim_name='content_score'),
            content_lwk=self.calculate_lwk(option='default', dim_name='content_score'),
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

    def get_marked_essays(self):
        marked_essay_list = []
        essay_marked = self.application.db.essay_marked
        
        for record in essay_marked.find({}):
            marked_essay_list.append(record['essay_id'])
        
        return marked_essay_list

    def get_two_ratings(self, start_date=None, end_date=None, option=None, dim_name=None):
        y0 = []
        y1 = []
        marked_essay_list = self.get_marked_essays()
        essay_data = self.application.db.essay_data

        if option == 'default':
            for essay_id in marked_essay_list:
                annotations = essay_data.find({'essay_id': essay_id})
                if annotations.count() == 2:
                    annotation0 = annotations[0]
                    annotation1 = annotations[1]

                    y0.append(annotation0[dim_name])
                    y1.append(annotation1[dim_name])
        else:
            start_timestamp = self.convert_date(start_date)
            end_timestamp = self.convert_date(end_date)

            for essay_id in marked_essay_list:
                annotations = essay_data.find({'essay_id': essay_id, 'time': {'$gte': start_timestamp, '$lt': end_timestamp}})
                if annotations.count() == 2:
                    annotation0 = annotations[0]
                    annotation1 = annotations[1]

                    y0.append(annotation0[dim_name])
                    y1.append(annotation1[dim_name])

        assert(len(y0) == len(y1))
        return y0, y1

    def calculate_qwk(self, start_date=None, end_date=None, option=None, dim_name=None):
        if option == 'default':
            y0, y1 = self.get_two_ratings(option='default', dim_name=dim_name)
        else:
            y0, y1 = self.get_two_ratings(start_date, end_date, option='screen', dim_name=dim_name)
        qwk = cohen_kappa_score(y0, y1, weights='quadratic')
        return qwk
    
    def calculate_lwk(self, start_date=None, end_date=None, option=None, dim_name=None):
        if option == 'default':
            y0, y1 = self.get_two_ratings(option='default', dim_name=dim_name)
        else:
            y0, y1 = self.get_two_ratings(start_date, end_date, option='screen', dim_name=dim_name)
        lwk = cohen_kappa_score(y0, y1, weights='linear')
        return lwk
    
    def handle_NaN(self, calculate_result):
        if(calculate_result != calculate_result):
            return 'nan'
        else:
            return calculate_result

    def post(self):
        start_date = self.get_argument('start_date')
        end_date = self.get_argument('end_date')
        start_timestamp = self.convert_date(start_date)
        end_timestamp = self.convert_date(end_date)

        response = {}
        response['start_timestamp'] = start_timestamp
        response['end_timestamp'] = end_timestamp

        response['vocabulary_qwk'] = self.handle_NaN(self.calculate_qwk(start_date, end_date, option='screen',dim_name='vocabulary_score'))
        response['vocabulary_lwk'] = self.handle_NaN(self.calculate_lwk(start_date, end_date, option='screen',dim_name='vocabulary_score'))
        response['sentence_qwk'] = self.handle_NaN(self.calculate_qwk(start_date, end_date, option='screen',dim_name='sentence_score'))
        response['sentence_lwk'] = self.handle_NaN(self.calculate_lwk(start_date, end_date, option='screen',dim_name='sentence_score'))
        response['structure_qwk'] = self.handle_NaN(self.calculate_qwk(start_date, end_date, option='screen',dim_name='structure_score'))
        response['structure_lwk'] = self.handle_NaN(self.calculate_lwk(start_date, end_date, option='screen',dim_name='structure_score'))
        response['content_qwk'] = self.handle_NaN(self.calculate_qwk(start_date, end_date, option='screen',dim_name='content_score'))
        response['content_lwk'] = self.handle_NaN(self.calculate_lwk(start_date, end_date, option='screen',dim_name='content_score'))


        
        self.write(response)


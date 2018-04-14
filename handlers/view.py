# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-04-12 Thursday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

from .base import *
import datetime

class ViewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        yesterday_date, today_date = self.get_default_date()

        self.render(
            'view.html',
            title='God View',
            annotator='', 
            start_date=yesterday_date,
            end_date=today_date,
        )
    
    def get_default_date(self):
        today = datetime.datetime.now()
        today_date = str(today.year) + '/' + str(today.month) + '/' + str(today.day)
        yesterday = today - datetime.timedelta(days=1)
        yesterday_date = str(yesterday.year) + '/' + str(yesterday.month) + '/' + str(yesterday.day)

        return yesterday_date, today_date
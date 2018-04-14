# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-04-13 Friday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

from .base import *

class QCHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render(
            'qc.html',
            title='Quality Control',
            annotator='', 
            start_date='',
            end_date='',
            qwk=0.0,
        )
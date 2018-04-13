# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-04-12 Thursday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

from .base import *

class ViewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render(
            'view.html',
            title='God View',
            annotator='', 
            start_date='',
            end_date='',
        )
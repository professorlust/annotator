# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-05-08 Tuesday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.


from .base import *
from time import time

class FormulaHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render(
            'formula.html',
            title='Formula Annotation',
        )
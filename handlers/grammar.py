# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-04-10 Tuesday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.


from .base import *
from time import time

class GrammarHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render(
            'grammar.html',
            title='Grammar Error Annotation',
        )
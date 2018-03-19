# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-19 Monday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

import tornado.web

class SigninHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            'signin.html',
            title='Sign in',
        )
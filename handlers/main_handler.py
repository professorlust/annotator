# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-13 Tuesday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            'main.html',
            title='Annotation Platform',
            
        )
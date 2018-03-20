# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-19 Monday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

from .base import *

class SigninHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        incorrect = self.get_secure_cookie("incorrect")
        if incorrect and int(incorrect) > 20:
            self.write('blocked')
            return
        
        self.render(
            'signin.html',
            title='Sign in',
        )

    @tornado.gen.coroutine
    def post(self):
        incorrect = self.get_secure_cookie("incorrect")
        if incorrect and int(incorrect) > 20:
            self.write('blocked')
            return
        
        getusername = tornado.escape.xhtml_escape(self.get_argument("account"))
        getpassword = tornado.escape.xhtml_escape(self.get_argument("password"))
        
        if "demo" == getusername and "demo" == getpassword:
            self.set_secure_cookie("user", self.get_argument("account"))
            self.set_secure_cookie("incorrect", "0")
            self.redirect('/')
        else:
            incorrect = self.get_secure_cookie("incorrect") or 0
            increased = str(int(incorrect)+1)
            self.set_secure_cookie("incorrect", increased)
            self.write(
                """
                    Invalid account or password
                    <a href="/">Back</a>
                """
            )

class SignoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect('/')

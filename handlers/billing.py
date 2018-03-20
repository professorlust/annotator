# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-19 Monday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

from .base import BaseHandler

class BillingHandler(BaseHandler):
    def get(self):
        self.render(
            'billing.html',
            title='Billing System',
        )
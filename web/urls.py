#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url, include
from web.views import account

urlpatterns = [
    url(r'^register/$', account.register, name='register'),  # register
    url(r'^send/sms/$',account.send_sms,name='send_sms')
]

#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url, include
from web.views import account, home, project

urlpatterns = [
    url(r'^register/$', account.register, name='register'),  # register
    url(r'^login/sms/$', account.login_sms, name='login_sms'), # login
    url(r'^login/$',account.login, name='login'), # login
    url(r'^logout/$',account.logout, name='logout'), # logout
    url(r'^image/code/$',account.image_code, name='image_code'), # image
    url(r'^send/sms/$',account.send_sms,name='send_sms'),
    url(r'^index/$',home.index,name='index'),

    #项目管理
    url(r'^project/list/$', project.project_list, name='project_list'),
    # /project/star/my/1
    # /project/star/join/1
    url(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_star, name='project_star'),
    url(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_unstar, name='project_unstar'),
]


#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url, include
from web.views import account, home, project, manage, file, setting, issues, dashboard, statistics

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

    url(r'^manage/(?P<project_id>\d+)/', include([
        url(r'^dashboard/$', dashboard.dashboard, name='dashboard'),
        url(r'^project_info/$', dashboard.project_info, name='project_info'),
        url(r'^dashboard/issues/chart/$', dashboard.issues_chart, name='issues_chart'),

        url(r'^issues/$', issues.issues, name='issues'),
        url(r'^issues/issues_upload$', issues.wiki_upload, name='wiki_upload'),
        url(r'^issues/detail/(?P<issues_id>\d+)/$', issues.issues_detail, name='issues_detail'),
        url(r'^issues/record/(?P<issues_id>\d+)/$', issues.issues_record, name='issues_record'),
        url(r'^issues/change/(?P<issues_id>\d+)/$', issues.issues_change, name='issues_change'),
        url(r'^issues/invite/url/$', issues.invite_url, name='invite_url'),

        url(r'^statistics/$', statistics.statistics, name='statistics'),
        url(r'^statistics/priority/$', statistics.statistics_priority, name='statistics_priority'),
        url(r'^statistics/project/user/$', statistics.statistics_project_user, name='statistics_project_user'),

        url(r'^file/$', file.file, name='file'),
        url(r'^file/delete/$', file.file_delete, name='file_delete'),
        url(r'^cos/credential/$', file.cos_credential, name='cos_credential'),
        url(r'^file/post/$', file.file_post, name='file_post'),
        url(r'^file/download/(?P<file_id>\d+)/$', file.file_download, name='file_download'),

        url(r'^setting/$', setting.setting, name='setting'),
        url(r'^setting/delete/$', setting.delete, name='setting_delete'),

        url(r'^project_get/$', project.project_get, name='project_get'),

    ], None, None)),
        url(r'^invite/join/(?P<code>\w+)/$', issues.invite_join, name='invite_join'),
]


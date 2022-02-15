#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
#项目管理菜单

def dashboard(request, project_id):
    return render(request, 'dashboard.html')


def issues(request, project_id):
    return render(request, 'issues.html')


def statistics(request, project_id):
    return render(request, 'statistics.html')


def file(request, project_id):
    return render(request, 'file.html')


def wiki(request, project_id):
    return render(request, 'wiki.html')


def setting(request, project_id):
    return render(request, 'setting.html')

#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
#项目管理菜单

def dashboard(request, project_id):
    return render(request, 'dashboard.html')

def statistics(request, project_id):
    return render(request, 'statistics.html')


def file(request, project_id):
    return render(request, 'file.html')



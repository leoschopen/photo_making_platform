#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from xpinyin import Pinyin

from utils.location import get_distance, gpstoWebMercator, get_core
from web.forms.project import ProjectModelForm
from web import models

from utils.tencent.cos import create_bucket


def project_list(request):
    """ 项目列表 """

    # GET请求查看项目列表
    """
    1. 从数据库中获取两部分数据
        我创建的所有项目：已星标、未星标
        我参与的所有项目：已星标、未星标
    2. 提取已星标
        列表 = 循环 [我创建的所有项目] + [我参与的所有项目] 把已星标的数据提取

    得到三个列表：星标、创建、参与
    """
    #管理员页面展示的数据
    project_dict = {'star': [], 'my': [], 'join': []}
    #用户页面展示的数据
    all_project_dict = {'project': [], 'my': []}
    all_project_list = models.Project.objects.filter().exclude(creator=request.tracer.user)


    for row in all_project_list:
        user_coordinate = []
        user_coordinate.append([request.tracer.user.latitude, request.tracer.user.longitude])
        user_lat, user_lon = gpstoWebMercator(user_coordinate)

        coordinate = []
        coordinate.append([row.latitude,row.longitude])
        lat, lon = gpstoWebMercator(coordinate)

        distance = get_distance(user_lat, user_lon, lat, lon)
        row.distance = distance
        all_project_dict['project'].append(row)

    my_project_list = models.Project.objects.filter(creator=request.tracer.user)
    for row in my_project_list:
        if row.star:
            project_dict['star'].append({"value": row, 'type': 'my'})
        else:
            project_dict['my'].append(row)


    join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)
    for item in join_project_list:
        if item.star:
            project_dict['star'].append({"value": item.project, 'type': 'join'})
        else:
            project_dict['join'].append(item.project)
    form = ProjectModelForm(request)


    if request.method == "GET" and request.session['user_category'] == 1:
        return render(request, 'project_list.html', {'form': form, 'project_dict': project_dict})
    elif request.method == "GET" and request.session['user_category'] == 2:
        return render(request, 'project_user_list.html', {'form': form, 'all_project_dict': all_project_dict, 'project_dict': project_dict})
    else:
        # POST，对话框的ajax添加项目。
        form = ProjectModelForm(request, data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            p = Pinyin()
            name_pinyin = p.get_pinyin(name)
            # 1. 为项目创建一个桶
            bucket = "{}-{}-{}-1301633315".format(name_pinyin,request.tracer.user.mobile_phone, str(int(time.time())))
            region = 'ap-chongqing'
            create_bucket(bucket, region)

            # 验证通过：项目名、颜色、描述 + creator谁创建的项目？instance为当前的modelform对象
            form.instance.bucket = bucket
            form.instance.region = region
            form.instance.creator = request.tracer.user
            # 创建项目
            form.save()
            return JsonResponse({'status': True})

        return JsonResponse({'status': False, 'error': form.errors})


def project_star(request, project_type, project_id):
    """ 星标项目 """
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=True)
        return redirect('project_list')

    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=True)
        return redirect('project_list')

    return HttpResponse('请求错误')


def project_unstar(request, project_type, project_id):
    """ 取消星标 """
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=False)
        return redirect('project_list')

    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=False)
        return redirect('project_list')

    return HttpResponse('请求错误')

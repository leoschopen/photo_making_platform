#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from xpinyin import Pinyin

from utils.location import CalDistance, get_price
from utils.map import getcode
from web.forms.project import ProjectModelForm
from web import models

from utils.tencent.cos import create_bucket


def get_task_price(request,task_lon,task_lat,lat,lon,hard,grow):
    return get_price(request,task_lon,task_lat,lat,lon,hard,grow)

def project_list(request):
    """ 项目列表 """

    # GET请求查看项目列表
    """
    管理员查看的列表
    1. 从数据库中获取两部分数据
        所有项目：已星标、未星标
    
    会员查看的列表
    2. 可选择的+已选择的（这两个加起来应该是所有的项目）
    
    每个列表的每一项要包括任务的名称，简要介绍，距离本用户的距离，价格
    """
    #管理员页面展示的数据
    project_dict = {'star': [], 'nostar': [] , 'all':[]}


    #用户页面展示的数据,分为待选择，已选择，已完成
    all_project_dict = {'select': [], 'selected': [], 'already': []}
    # 用户参加的项目要在已选择的projectuser里面查找
    all_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)


    user_lat, user_lon = request.tracer.user.latitude, request.tracer.user.longitude
    #会员selected，为马上要展示的用户已参加任务添加距离当前用户的距离
    for row in all_project_list:
        lat, lon = row.project.latitude,row.project.longitude
        distance = CalDistance(user_lon, user_lat, lon, lat)
        row.project.distance = distance
        all_project_dict['selected'].append(row.project)

    #会员already
    already_project_list = models.ProjectUser.objects.filter(Q(user=request.tracer.user)&Q(already=True))
    for row in already_project_list:
        all_project_dict['already'].append(row.project)

   #管理员应该显示全部的任务
    my_project_list = models.Project.objects.all()
    for row in my_project_list:
        lat, lon = row.latitude, row.longitude
        distance = CalDistance(user_lon, user_lat, lon, lat)
        row.distance = distance
        row.task_price = get_task_price(request, float(lon), float(lat), user_lon, user_lat, row.hard, row.grow)
        project_dict['all'].append(row)
        if row.star:
            project_dict['star'].append({"value": row, 'type': 'star'})
        else:
            project_dict['nostar'].append(row)

    #会员select应该是project全部的任务除去projectuser已经选择的任务,去除已经完成的任务
    all_project_dict['select'] = [item for item in project_dict['all'] if item not in set(all_project_dict['selected'])]
    all_project_dict['select'] = [item for item in all_project_dict['select'] if item not in set(all_project_dict['already'])]
    all_project_dict['selected'] = [item for item in all_project_dict['selected'] if
                                  item not in set(all_project_dict['already'])]
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
            address = form.cleaned_data['location']
            grow = form.cleaned_data['grow']
            hard = form.cleaned_data['hard']

            p = Pinyin()
            name_pinyin = p.get_pinyin(name)[:10]
            # 1. 为项目创建一个桶
            bucket = "{}-{}-1301633315".format(name_pinyin, str(int(time.time())))
            region = 'ap-chongqing'
            create_bucket(bucket, region)

            #为项目添加价格
            city = ''
            my_location = getcode(address, city)
            task_lon, task_lat = my_location.split(',')[0],my_location.split(',')[1]

            # 验证通过：项目名、颜色、描述 + creator谁创建的项目？instance为当前的modelform对象
            form.instance.bucket = bucket
            form.instance.region = region
            form.instance.creator = request.tracer.user
            form.instance.longitude = task_lon
            form.instance.latitude = task_lat

            # 创建项目
            form.save()
            return JsonResponse({'status': True})

        return JsonResponse({'status': False, 'error': form.errors})


def project_star(request, project_type, project_id):
    """ 星标项目 """
    if project_type != 'star':
        models.Project.objects.filter(id=project_id).update(star=True)
        return redirect('project_list')
    return HttpResponse('请求错误')


def project_unstar(request, project_type, project_id):
    """ 取消星标 """
    if project_type == 'star':
        models.Project.objects.filter(id=project_id).update(star=False)
        return redirect('project_list')
    return HttpResponse('请求错误')


# 用来抢单的逻辑
def project_get(request, project_id):
    project_object = models.Project.objects.filter(id=project_id).first()

    # ####### 问题1： 最多允许的成员(要进入的项目的创建者的限制）#######
    # max_member = request.tracer.price_policy.project_member # 当前登录用户他限制
    max_member = project_object.user_count

    # 目前所有成员(创建者&参与者）
    current_member = project_object.join_count
    current_member = current_member + 1
    if current_member >= max_member:
        return render(request, 'invite_join.html', {'error': '项目成员超限'})

    user_lat, user_lon = request.tracer.user.latitude, request.tracer.user.longitude
    task_lon, task_lat = project_object.longitude, project_object.latitude
    task_price = get_task_price(request, float(task_lon), float(task_lat), user_lon, user_lat, project_object.hard, project_object.grow)

    models.ProjectUser.objects.create(user=request.tracer.user, project=project_object, task_price=task_price)

    # ####### 问题2： 更新项目参与成员 #######
    project_object.join_count += 1
    project_object.save()

    return render(request, 'invite_join.html', {'project': project_object})
    return HttpResponse('请求错误')

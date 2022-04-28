import django
import os
import sys

from pip._internal import locations
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)  # 将项目的路径加入到sys.path这样django启动之后就可以知道路径了
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "bug_manage.settings")
django.setup()

from pyproj import Transformer
from web import models
from sklearn.datasets import make_blobs
from matplotlib import pyplot
import random

# -*- coding: utf-8 -*-
# @Author  : lin

from sklearn.datasets import make_blobs
from matplotlib import pyplot
import numpy as np
import random

from math import cos, sin, atan2, sqrt, pi, radians, degrees, asin

"""
本工具包实现对于和价格相关五个因子的计算
实际使用的时候需要对实时的数据进行聚类，包括会员的位置和任务的位置，这里为了简化计算就直接用已经得到的聚类位置进行计算
包括4个任务聚类中心和两个会员聚类中心
"""

"""
归一化用值
"""
credit_max = 51150.38941
credit_min = 2.788123892



def sigmoid(x):
    return 1.0/(1+np.exp(-float(x)))

#haversine公式求两点之间的距离
def CalDistance(lon1, lat1, lon2, lat2):
    dlat = abs(lat1 / 180.0 * pi - lat2 / 180.0 * pi)
    dlon = abs(lon1 / 180.0 * pi - lon2 / 180.0 * pi)
    a = sin(dlat / 2) * sin(dlat / 2) + cos(lat1 / 180.0 * pi) * cos(lat2 / 180.0 * pi) * sin(dlon / 2) * sin(dlon / 2)
    dist = 2 * 6378.137 * asin(sqrt(a))
    return round(dist, 2)


# 任务中心7km内统计会员的个数，得出会员的聚集度
# 获取数据库中所有的会员的经纬度信息，统计和数据中心的距离
def user_aggre_degree(request,task_lon, task_lat):
    user_object = request.tracer.all_user
    count = 0
    for project in user_object:
        dist = CalDistance(project.longitude,project.latitude,task_lon,task_lat)
        if (dist < 7000):
            count = count + 1
    return count


def task_aggre_degree(request,task_lon, task_lat):
    task_project = request.tracer.all_task
    count = 0
    for project in task_project:
        dist = CalDistance(project.longitude,project.latitude,task_lon,task_lat)
        if (dist < 7000):
            count = count + 1
    return count


#影响因子1，供求比,任务周围7km范围内用户数除以任务数
def get_p(request,task_lon, task_lat):
    res = user_aggre_degree(request,task_lon, task_lat)/task_aggre_degree(request,task_lon, task_lat)*20
    if res>20:
        res = 20
    return round(res, 2)


#影响因子2，任务周围7km的会员平均信誉值
def get_credit(request,task_lon, task_lat):
    user_object = request.tracer.all_user
    credit = 0
    num = 1
    for project in user_object:
        dist = CalDistance(project.longitude,project.latitude,task_lon,task_lat)
        if (dist < 7000):
            credit = credit + project.reputation
            num = num+1
    credit = credit/num
    credit = (credit-credit_min)/(credit_max-credit_min)
    return round(credit,2)

#影响因子3，任务距离会员距离,直接调用caldistance即可

#影响因子4，经济发展水平
#创建任务的时候由发布方确定

#影响因子5，任务难度
#创建任务的时候由发布方确定


def get_price(request,task_lon,task_lat,lon,lat,hard,grow):
    p = get_p(request,task_lon, task_lat)
    l = CalDistance(task_lon,task_lat,lon,lat)
    l=sigmoid(l)*20
    if l>20:
        l=20
    credit = get_credit(request,task_lon,task_lat)
    price = 65 + 0.4783 * p + 0.2218 * hard + 0.1061 * grow + 0.0589 * l + 0.1349*credit
    return round(price,2)



if __name__ == '__main__':
    pass
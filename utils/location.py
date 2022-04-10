import django
import os
import sys

from pip._internal import locations

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)#将项目的路径加入到sys.path这样django启动之后就可以知道路径了
os.environ.setdefault('DJANGO_SETTINGS_MODULE',"bug_manage.settings")
django.setup()

from pyproj import Transformer
from web import models
import numpy as np
from sklearn.datasets import make_blobs
from matplotlib import pyplot
import random

# -*- coding: utf-8 -*-
# @Time    : 18-12-6
# @Author  : lin

from sklearn.datasets import make_blobs
from matplotlib import pyplot
import numpy as np
import random

from math import cos, sin, atan2, sqrt, pi, radians, degrees


def center_geolocation(geolocations):
    x = 0
    y = 0
    z = 0
    lenth = len(geolocations)
    for lon, lat in geolocations:
        lon = radians(float(lon))
        lat = radians(float(lat))
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)

    x = float(x / lenth)
    y = float(y / lenth)
    z = float(z / lenth)
    coordinate = []
    coordinate.append([degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y)))])
    return coordinate



# 如果希望轴的顺序总是按 x、y 或 lon、lat 的顺序排列，你可以在创建转换器时使用 always_xy 选项。
# 将gps坐标转化为平面坐标
def gpstoWebMercator(coordinate):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    x, y = transformer.transform(coordinate[0][0], coordinate[0][1])
    return x, y

#获取任务的中心坐标
def get_core():
    task_project = models.Project.objects.all()
    for project in task_project:
        locations = []
        locations.append([project.latitude,project.longitude])
    coordinate = center_geolocation(locations)
    return coordinate

def get_distance(m, n, p, q):
    a = np.array((m, n))
    b = np.array((p, q))
    dist = np.linalg.norm(a - b)/1000
    return format(dist,'.5f')

#经纬度坐标转直角坐标
def wgs84_to_xy(core_lon, core_lat, project_lon, project_lat):
    user_coordinate = []
    user_coordinate.append([core_lon, core_lat])
    user_lat, user_lon = gpstoWebMercator(user_coordinate)

    coordinate = []
    coordinate.append([project_lon, project_lat])
    lat, lon = gpstoWebMercator(coordinate)

    distance = get_distance(user_lat, user_lon, lat, lon)/1000
    return format(distance,'.5f')
# 任务中心5km内统计会员的个数，得出会员的聚集度
# 获取数据库中所有的会员的经纬度信息，统计和数据中心的距离
def user_aggre_degree():
    user_object = models.UserInfo.objects.all()
    count = 0
    core_lon, core_lat = gpstoWebMercator(get_core())
    for project in user_object:
        coordinate = []
        coordinate.append([project.latitude, project.longitude])

        lat, lon = gpstoWebMercator(coordinate)
        dist = get_distance(core_lon, core_lat, lat, lon)
        if(dist<5000):
            count = count + 1
    if count < 0:
        count = 1
    else:
        count = 20 - (count-1)/2
    return count

def task_aggre_degree():
    task_project = models.Project.objects.all()
    count = 0
    for project in task_project:
        core_lon, core_lat = gpstoWebMercator(get_core())
        coordinate = []
        coordinate.append([project.latitude, project.longitude])
        lat, lon = gpstoWebMercator(coordinate)
        dist = get_distance(core_lon, core_lat, lat, lon)
        if (dist < 5000):
            count = count + 1

    if count >= 0 and count<=15:
        count = 5
    elif count >= 16 and count<=30:
        count = 10
    elif count >30:
        count = 20
    return count

def task_hard(price,latitude,longitude):
    core_lon, core_lat = gpstoWebMercator(get_core())
    coordinate = []
    coordinate.append([latitude, longitude])
    lat, lon = gpstoWebMercator(coordinate)
    dist = get_distance(core_lon, core_lat, lat, lon)
    if price >=75 and price <=85 and dist >= 10000:
        return 20
    elif price >=75 and price <=85 and dist < 10000:
        return 10
    elif price <=75 and dist < 5000:
        return 5


def get_price(origin_price,x,y,h,t):
    p = origin_price + 0.10899*x + 0.10899*y +0.48519*h +0.29682*t
    return p





if __name__ == '__main__':
    print(gpstoWebMercator(22.102,123.110))


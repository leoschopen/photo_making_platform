#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from django.shortcuts import render, redirect

from utils.location import gpstoWebMercator
from web import models


def index(request):
    return render(request, 'index.html')


def price(request):
    """ 套餐 """
    # 获取套餐
    policy_list = models.PricePolicy.objects.filter(category=2)
    return render(request, 'price.html', {'policy_list': policy_list})


def payment(request, policy_id):
    """ 支付页面"""
    # 1. 价格策略（套餐）policy_id
    policy_object = models.PricePolicy.objects.filter(id=policy_id, category=2).first()
    if not policy_object:
        return redirect('price')

    # 2. 要购买的数量
    number = request.GET.get('number', '')
    if not number or not number.isdecimal():
        return redirect('price')
    number = int(number)
    if number < 1:
        return redirect('price')

    # 3. 计算原价
    origin_price = number * policy_object.price

    # 4.之前购买过套餐(之前掏钱买过）
    balance = 0
    _object = None
    if request.tracer.price_policy.category == 2:
        # 找到之前订单：总支付费用 、 开始~结束时间、剩余天数 = 抵扣的钱
        _object = models.Transaction.objects.filter(user=request.tracer.user, status=2).order_by('-id').first()
        total_timedelta = _object.end_datetime - _object.start_datetime
        balance_timedelta = _object.end_datetime - datetime.datetime.now()
        if total_timedelta.days == balance_timedelta.days:
            balance = _object.price / total_timedelta.days * (balance_timedelta.days - 1)
        else:
            balance = _object.price / total_timedelta.days * balance_timedelta.days

    if balance >= origin_price:
        return redirect('price')

    context = {'policy_id': policy_object.id, 'number': number, 'origin_price': origin_price,
               'balance': round(balance, 2), 'total_price': origin_price - round(balance, 2),
               'policy_object': policy_object, 'transaction': _object}

    return render(request, 'payment.html', context)

def price(request):
    task_project = models.Project.objects.all();
    for project in task_project:
        core_lon,core_lat = gpstoWebMercator(19,19);
        lat,lon = gpstoWebMercator(project.latitude, project.longitude)
        import numpy as np
        a = np.array((core_lon,core_lat))
        b = np.array((lat,lon))

        dist = np.linalg.norm(a - b)
        print(dist)

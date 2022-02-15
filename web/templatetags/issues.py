#!/usr/bin/env python
# -*- coding:utf-8 -*-
# !/usr/bin/env python
# -*- coding:utf-8 -*-
from django.template import Library
from django.urls import reverse
from web import models

register = Library()


@register.simple_tag
def string_just(num):
    if num < 100:
        num = str(num).rjust(3, "0")
    return "#{}".format(num)

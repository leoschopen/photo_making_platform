#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib
import uuid

from django.conf import settings


def md5(string):
    """ MD5加密 """
    hash_object = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))#加盐
    hash_object.update(string.encode('utf-8'))
    return hash_object.hexdigest()

def uid(string):
    data = "{}-{}".format(str(uuid.uuid4()), string)
    return md5(data)
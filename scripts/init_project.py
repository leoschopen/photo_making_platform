import time

import django
import os
import sys
import numpy as np
import pandas as pd

from utils import encrypt
from utils.tencent.cos import create_bucket, delete_bucket

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)#将项目的路径加入到sys.path这样django启动之后就可以知道路径了
os.environ.setdefault('DJANGO_SETTINGS_MODULE',"bug_manage.settings")
django.setup()


from web import models
user_object = models.UserInfo.objects.filter(id=7).first()
user = user_object
dataset = pd.read_excel('input_django.xls')
# for row in dataset.values:
#     bucket = '1-18727010216-1650092661-1301633315'
#     region = 'ap-chongqing'
#     models.Project.objects.create(name=row[0], task_price=row[4], color=5, desc=row[0], use_space=0, star=False, latitude=row[2], longitude=row[3], join_count=0,user_count=5,creator=user, bucket=bucket,region='ap-chongqing')
num = 1650092784
for i in range(88,100):
    num = num+1
    num2 = num-1
    bucket = "{}-{}-{}-1301633315".format(i,18727010216, num)
    bucket2 = "{}-{}-{}-1301633315".format(i,18727010216, num2)
    region = 'ap-chongqing'
    delete_bucket(bucket, region)
    delete_bucket(bucket2, region)
    # print(bucket,bucket2)


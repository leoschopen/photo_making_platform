
import django
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)#将项目的路径加入到sys.path这样django启动之后就可以知道路径了
os.environ.setdefault('DJANGO_SETTINGS_MODULE',"bug_manage.settings")
django.setup()


from web import models
# 往数据库添加数据：链接数据库、操作、关闭链接
models.UserInfo.objects.create(username='陈硕', email='chengshuo@live.com', mobile_phone='13838383838', password='123123')
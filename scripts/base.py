import django
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)#将项目的路径加入到sys.path这样django启动之后就可以知道路径了
os.environ.setdefault('DJANGO_SETTINGS_MODULE',"bug_manage.settings")
django.setup()

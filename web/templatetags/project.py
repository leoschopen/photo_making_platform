from django.http import request
from django.template import Library

from web import models

register = Library()


@register.inclusion_tag('inclusion/all_project_list.html')
def all_project_list():
    #获取我创建的项目
    my_project_list = models.Project.objects.filter(creator=request.tracer.user)
    #获取我参与的项目
    join_project_list = models.Project.objects.filter(user=request.tracer.user)
    return {'name': 'leo'}

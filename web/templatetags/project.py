from django.http import request
from django.template import Library
from django.urls import reverse

from web import models

register = Library()


@register.inclusion_tag('inclusion/all_project_list.html')
def all_project_list(request):
    # 1. 获我创建的所有项目
    my_project_list = models.Project.objects.filter(creator=request.tracer.user)

    # 2. 获我参与的所有项目
    join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)

    #3. 获取除了我之外的所有项目
    all_project_list = models.Project.objects.filter().exclude(creator=request.tracer.user)

    return {'my': my_project_list, 'join': join_project_list, 'project':all_project_list}


@register.inclusion_tag('inclusion/manage_menu_list.html')
def manage_menu_list(request):
    if request.tracer.user == 1 :
        data_list = [
            {'title': '概览', 'url': reverse("dashboard", kwargs={'project_id': request.tracer.project.id})},
            {'title': '交流', 'url': reverse("issues", kwargs={'project_id': request.tracer.project.id})},
            {'title': '统计', 'url': reverse("statistics", kwargs={'project_id': request.tracer.project.id})},
            {'title': '文件', 'url': reverse("file", kwargs={'project_id': request.tracer.project.id})},
            {'title': '个人中心', 'url': reverse("setting", kwargs={'project_id': request.tracer.project.id})},
        ]
    else:
        data_list = [
            {'title': '交流', 'url': reverse("issues", kwargs={'project_id': request.tracer.project.id})},
            {'title': '文件', 'url': reverse("file", kwargs={'project_id': request.tracer.project.id})},
            {'title': '个人中心', 'url': reverse("setting", kwargs={'project_id': request.tracer.project.id})},
        ]
    for item in data_list:
        # 当前用户访问的URL：request.path_info:  /manage/4/issues/xxx/add/
        if request.path_info.startswith(item['url']):
            item['class'] = 'active'

    return {'data_list': data_list}

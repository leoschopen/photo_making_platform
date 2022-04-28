#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError

from web.forms.bootstrap import BootStrapForm
from web import models
from web.forms.widgets import ColorRadioSelect


class ProjectModelForm(BootStrapForm, forms.ModelForm):
    bootstrap_class_exclude = ['color']
    # desc = forms.CharField(widget=forms.Textarea(attrs={'xx': 123}))
    class Meta:
        model = models.Project
        fields = ['name', 'location', 'hard' , 'grow' ,'color', 'desc']
        #重写插件CharField变Textarea
        widgets = {
            'desc': forms.Textarea,
            'color': ColorRadioSelect(attrs={'class': 'color-radio'}),
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_name(self):
        """ 项目校验 """
        name = self.cleaned_data['name']
        # 1. 当前用户是否已创建过此项目(项目名是否已存在)？
        exists = models.Project.objects.filter(name=name, creator=self.request.tracer.user).exists()
        if exists:
            raise ValidationError('任务名已存在')

        # 2. 当前用户是否还有额度进行创建项目？
        # 最多创建N个项目
        # self.request.tracer.price_policy.project_num

        # 现在已创建多少项目？
        count = models.Project.objects.filter(creator=self.request.tracer.user).count()

#        if count >= self.request.tracer.price_policy.project_num:
 #           raise ValidationError('任务个数超限，星级等级不够')

        return name


#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
表格相关处理，验证
"""
import random
from cProfile import label

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.forms import BaseForm, PasswordInput

from utils import encrypt
from web import models
from utils.tencent.sms import send_sms_single
from django_redis import get_redis_connection

from web.forms.bootstrap import BootStrapForm


class RegisterModelForm(BootStrapForm,forms.ModelForm):
    password = forms.CharField(
        label='密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "密码长度不能小于8个字符",
            'max_length': "密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        label='重复密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "重复密码长度不能小于8个字符",
            'max_length': "重复密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput())

    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput())

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']


    def clean_username(self):
        username = self.cleaned_data['username']
        exists = models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 加密 & 返回
        return encrypt.md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')

        confirm_pwd = encrypt.md5(self.cleaned_data['confirm_password'])

        if pwd != confirm_pwd:
            raise ValidationError('两次密码不一致')

        return confirm_pwd


    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已注册')
        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data['code']

        # mobile_phone = self.cleaned_data['mobile_phone']

        mobile_phone = self.cleaned_data.get('mobile_phone')
        if not mobile_phone:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')

        redis_str_code = redis_code.decode('utf-8')

        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')

        return code


class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    #在form中想要使用视图函数里面的一些参数或者一些值可以重新init方法可以接收到
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request=request
#钩子函数，clean开头
    def clean_mobile_phone(self):
        #手机校验的钩子函数，钩子函数类似于中间拦截，进行执行
        #当系统消息触发，自动会调用
        mobile_phone = self.cleaned_data['mobile_phone']
        tpl = self.request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)


        if not template_id:
            raise ValidationError('短信模板错误')

        #检查数据库中是否已经有手机号（没注册过）
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if tpl == 'login':
            #登陆的时候要求的是手机号存在
            if not exists:
                raise ValidationError('手机号未注册')
        else:
            # 校验数据库中是否已有手机号，注册要求不存在
            if exists:
                raise ValidationError('手机号已存在')

        #发短信，写redis
        code = random.randrange(1000,9999)
        sms = send_sms_single(mobile_phone,template_id,[code,])
        #发送失败
        if sms['result'] != 0:
            raise ValidationError("短信发送失败,{}".format(sms['errmsg']))

        #将验证码写入redis
        #使用django-redis组件
        conn = get_redis_connection()
        conn.set(mobile_phone,code,ex=60)

        return mobile_phone


class LoginSMSForm(BootStrapForm, forms.Form):
    mobile_phone = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ]
    )

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput())

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        # user_object = models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        if not exists:
            raise ValidationError('手机号不存在')

        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data['code']
        mobile_phone = self.cleaned_data.get('mobile_phone')

        # 手机号不存在，则验证码无需再校验
        if not mobile_phone:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)  # 根据手机号去获取验证码
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')

        redis_str_code = redis_code.decode('utf-8')

        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')

        return code


class LoginForm(BootStrapForm,forms.Form):
    username = forms.CharField(label="邮箱或手机号")
    password = forms.CharField(label="密码",widget=PasswordInput(render_value=True))
    code = forms.CharField(label="图片验证码")

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 加密 & 返回
        return encrypt.md5(pwd)

    def clean_code(self):
        """ 钩子 图片验证码是否正确？ """
        # 读取用户输入的验证码
        code = self.cleaned_data['code']

        # 去session获取自己的验证码
        session_code = self.request.session.get('image_code')
        if not session_code:
            raise ValidationError('验证码已过期，请重新获取')

        if code.strip().upper() != session_code.strip().upper():
            raise ValidationError('验证码输入错误')

        return code


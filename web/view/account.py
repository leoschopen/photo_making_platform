"""
用户注册，短信，登录，注销
"""
from django.core.validators import RegexValidator
from django.shortcuts import render
from django import forms

from web import models


# class RegisterModelForm(forms.ModelForm):
#     """如果原来的modelform原来定义得有，重复则重写，否则添加"""
#     #手机号验证
#     mobile_phone = forms.CharField(
#         label='手机号',
#         validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$','手机号格式错误'),])#正则表达式
#     #密码密文展示,并确定标签的属性
#     password = forms.CharField(
#         label='密码',
#         widget=forms.PasswordInput())
#     #重复输入密码
#     confirm_password = forms.CharField(
#         label='重复密码',
#         widget=forms.PasswordInput())
#     #验证码
#     code = forms.CharField(
#         label='验证码',
#         widget=forms.TextInput())
#     class Meta:
#         model = models.UserInfo
#         fields = ['username','email','password','confirm_password','mobile_phone','code']
#     #重写init函数每个标签的class都设置为form—control
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#         for name,field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
#             field.widget.attrs['placeholder'] = '请输入%s' % field.label

def register(request):
    return render(request, 'web/register.html')
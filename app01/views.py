from django.shortcuts import render,HttpResponse
import random
#Create your views here.
from utils.tencent.sms import send_sms_single
from django.conf import settings

def send_sms(request):
    """send message"""
    """
    tpl = request.GET.get('tpl')
    template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    if not template_id:
        return HttpResponse('模板不存在')"""
    code =random.randrange(1000,9999)
    res = send_sms_single('15707200703',1270874,[code,])
    if res['result'] ==0:
        return HttpResponse('成功')
    else:
        return HttpResponse(res['errmsg'])

from django import forms
from app01 import models
from django.core.validators import RegexValidator

class RegisterModelForm(forms.ModelForm):
    """如果原来的modelform原来定义得有，重复则重写，否则添加"""
    #手机号验证
    mobile_phone = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$','手机号格式错误'),])#正则表达式
    #密码密文展示,并确定标签的属性
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput())
    #重复输入密码
    confirm_password = forms.CharField(
        label='重复密码',
        widget=forms.PasswordInput())
    #验证码
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput())
    class Meta:
        model = models.UserInfo
        fields = ['username','email','password','confirm_password','mobile_phone','code']
    #重写init函数每个标签的class都设置为form—control
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % field.label

def register(request):
    form = RegisterModelForm()
    return render(request, 'web/register.html', {'form':form})

from django.shortcuts import HttpResponse
from django_redis import get_redis_connection
def index(request):
    # 去连接池中获取一个连接
    conn = get_redis_connection("default")
    conn.set('nickname', "武沛齐", ex=10)
    value = conn.get('nickname')
    print(value)
    return HttpResponse("OK")
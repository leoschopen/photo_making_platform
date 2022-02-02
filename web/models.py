from django.db import models


class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32, db_index=True) # db_index=True 索引
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    mobile_phone = models.CharField(verbose_name='手机号', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    #注册成功默认为空，如果购买套餐后将policy放在这里，以免后面进行对支付记录进行排序
    # price_policy = models.ForeignKey(verbose_name='价格策略', to='PricePolicy', null=True, blank=True)

class PricePolicy(models.Model):
    """ 价格策略 """
    category_choices = (
        (1, '免费版'),
        (2, '收费版'),
        (3, '其他'),
    )
    category = models.SmallIntegerField(verbose_name='收费类型', default=2, choices=category_choices)
    title = models.CharField(verbose_name='标题', max_length=32)
    price = models.PositiveIntegerField(verbose_name='价格')  # 正整数

    project_num = models.PositiveIntegerField(verbose_name='创建任务数')
    project_member = models.PositiveIntegerField(verbose_name='任务参与人数')
    project_space = models.PositiveIntegerField(verbose_name='单任务空间')
    per_file_size = models.PositiveIntegerField(verbose_name='单文件上传大小')

    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Transaction(models.Model):
    """ 交易记录 """
    status_choice = (
        (1, '未支付'),
        (2, '已支付')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice)

    order = models.CharField(verbose_name='订单号', max_length=64, unique=True)  # 唯一索引

    user = models.ForeignKey(verbose_name='用户', to='UserInfo',on_delete=models.CASCADE)
    price_policy = models.ForeignKey(verbose_name='价格策略', to='PricePolicy',on_delete=models.CASCADE)

    count = models.IntegerField(verbose_name='数量（年）', help_text='0表示无限期')

    price = models.IntegerField(verbose_name='实际支付价格')

    start_datetime = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    end_datetime = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)

    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Project(models.Model):
    """ 任务表 """
    COLOR_CHOICES = (
        (1, "#403137"),  # 56b8eb
        (2, "#314F49"),  # f28033
        (3, "#82501E"),  # ebc656
        (4, "#A35229"),  # a2d148
        (5, "#0D4E73"),  # #20BFA4
        (6, "#4B7A95"),  # 7461c2,
        (7, "#E87A68"),  # 20bfa3,
    )

    name = models.CharField(verbose_name='任务名', max_length=32)
    task_price = models.IntegerField(verbose_name='任务佣金')
    color = models.SmallIntegerField(verbose_name='颜色', choices=COLOR_CHOICES, default=1)
    desc = models.CharField(verbose_name='任务描述', max_length=255, null=True, blank=True)
    use_space = models.IntegerField(verbose_name='任务相关文件已使用空间', default=0)
    star = models.BooleanField(verbose_name='星标', default=False)

    join_count = models.SmallIntegerField(verbose_name='参与人数', default=1)
    creator = models.ForeignKey(verbose_name='创建者', to='UserInfo',on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class ProjectUser(models.Model):
    """ 任务领取者 """
    user = models.ForeignKey(verbose_name='领取任务者', to='UserInfo',on_delete=models.CASCADE)
    project = models.ForeignKey(verbose_name='任务', to='Project',on_delete=models.CASCADE)
    star = models.BooleanField(verbose_name='星标', default=False)

    create_datetime = models.DateTimeField(verbose_name='加入时间', auto_now_add=True)
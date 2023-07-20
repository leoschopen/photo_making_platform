from django.db import models


class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32, db_index=True)  # db_index=True 索引
    user_type = (
        (1, '任务发放者'),
        (2, '任务领取者'),
    )
    category = models.SmallIntegerField(verbose_name='用户类型', default=2, choices=user_type)
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    mobile_phone = models.CharField(verbose_name='手机号', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    asset = models.IntegerField(verbose_name='余额',default=1000)
    reputation = models.FloatField(verbose_name='信誉值',default=1000)
    latitude = models.FloatField(verbose_name='经度', default=22.000000)
    longitude = models.FloatField(verbose_name='纬度', default=22.000000)

    # price_policy = models.ForeignKey(verbose_name='价格策略', to='PricePolicy')
    # 注册成功默认为空，如果购买套餐后将policy放在这里，以免后面进行对支付记录进行排序
    # price_policy = models.ForeignKey(verbose_name='价格策略', to='PricePolicy', null=True, blank=True)


# class PricePolicy(models.Model):
#     """ 不同星级的价格策略 """
#     category_choices = (
#         (1, '一星级'),
#         (2, '二星级'),
#         (3, '三星级'),
#     )
#     category = models.SmallIntegerField(verbose_name='收费类型', default=1, choices=category_choices)
#     title = models.CharField(verbose_name='标题', max_length=32)
#
#     project_num = models.PositiveIntegerField(verbose_name='创建任务数')
#     project_member = models.PositiveIntegerField(verbose_name='任务参与人数')
#     project_space = models.PositiveIntegerField(verbose_name='单任务空间')
#     per_file_size = models.PositiveIntegerField(verbose_name='单文件上传大小')


class Transaction(models.Model):
    """ 交易记录
    主要是领取任务者在审核通过后获得相应的报酬"""
    status_choice = (
        (1, '未领取'),
        (2, '已领取')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice)

    order = models.CharField(verbose_name='订单号', max_length=64, unique=True)  # 唯一索引

    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)

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
    HARD_CHOICES = (
        (20,"困难任务"),
        (10,"一般困难任务"),
        (5,"简单任务"),
    )
    GROW_CHOICES = (
        (20,"经济发展水平高"),
        (15,"经济发展水平较高"),
        (10,"经济发展水平一般"),
        (5,"经济发展水平不高"),
    )
    name = models.CharField(verbose_name='任务名', max_length=32)
    color = models.SmallIntegerField(verbose_name='颜色', choices=COLOR_CHOICES, default=1)
    desc = models.CharField(verbose_name='任务描述', max_length=255, null=True, blank=True)
    use_space = models.IntegerField(verbose_name='任务相关文件已使用空间', default=0)
    star = models.BooleanField(verbose_name='星标', default=False)
    hard = models.IntegerField(verbose_name='任务难易程度', choices=HARD_CHOICES, default=20)
    grow = models.IntegerField(verbose_name='任务所在地区发达程度', choices=GROW_CHOICES, default=20)
    location = models.CharField(verbose_name='任务位置', max_length=255, null=True, blank=True)
    latitude = models.FloatField(verbose_name='经度', default=22.000000)
    longitude = models.FloatField(verbose_name='纬度', default=22.000000)

    join_count = models.SmallIntegerField(verbose_name='参与人数', default=1)
    user_count = models.SmallIntegerField(verbose_name='总人数', default=100)
    creator = models.ForeignKey(verbose_name='创建者', to='UserInfo', on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    bucket = models.CharField(verbose_name='cos桶', max_length=128)
    region = models.CharField(verbose_name='cos区域', max_length=32)


class ProjectUser(models.Model):
    """ 任务领取者 """
    user = models.ForeignKey(verbose_name='领取任务者', to='UserInfo', on_delete=models.CASCADE)
    project = models.ForeignKey(verbose_name='任务', to='Project', on_delete=models.CASCADE)
    star = models.BooleanField(verbose_name='星标', default=False)
    already = models.BooleanField(verbose_name='完成状态', default=False)
    task_price = models.FloatField(verbose_name='任务价格', default=65)
    create_datetime = models.DateTimeField(verbose_name='加入时间', auto_now_add=True)


class FileRepository(models.Model):
    """ 文件库 """
    project = models.ForeignKey(verbose_name='项目', to='Project', on_delete=models.CASCADE)
    file_type_choices = (
        (1, '文件'),
        (2, '文件夹')
    )
    file_type = models.SmallIntegerField(verbose_name='类型', choices=file_type_choices)
    name = models.CharField(verbose_name='文件夹名称', max_length=32, help_text="文件/文件夹名")
    key = models.CharField(verbose_name='文件储存在COS中的KEY', max_length=128, null=True, blank=True)
    file_size = models.IntegerField(verbose_name='文件大小', null=True, blank=True)
    file_path = models.CharField(verbose_name='文件路径', max_length=255, null=True,
                                 blank=True)  # https://桶.cos.ap-chengdu/....

    parent = models.ForeignKey(verbose_name='父级目录', to='self', related_name='child', null=True, blank=True, on_delete=models.CASCADE)

    update_user = models.ForeignKey(verbose_name='最近更新者', to='UserInfo', on_delete=models.CASCADE)
    update_datetime = models.DateTimeField(verbose_name='更新时间', auto_now=True)


class Issues(models.Model):
    """ 问题 """
    project = models.ForeignKey(verbose_name='项目', to='Project', on_delete=models.CASCADE)
    module = models.ForeignKey(verbose_name='阶段', to='Module', null=True, blank=True, on_delete=models.CASCADE)

    subject = models.CharField(verbose_name='主题', max_length=80)
    desc = models.TextField(verbose_name='问题描述')
    priority_choices = (
        ("danger", "高"),
        ("warning", "中"),
        ("success", "低"),
    )
    priority = models.CharField(verbose_name='优先级', max_length=12, choices=priority_choices, default='danger')

    # 新建、处理中、已解决、已忽略、待反馈、已关闭、重新打开
    status_choices = (
        (1, '新建'),
        (2, '处理中'),
        (3, '已解决'),
        (4, '已忽略'),
        (5, '待反馈'),
        (6, '已关闭'),
        (7, '重新打开'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=1)

    assign = models.ForeignKey(verbose_name='指派', to='UserInfo', related_name='task', null=True, blank=True, on_delete=models.CASCADE)

    start_date = models.DateField(verbose_name='开始时间', null=True, blank=True)
    end_date = models.DateField(verbose_name='结束时间', null=True, blank=True)

    creator = models.ForeignKey(verbose_name='创建者', to='UserInfo', related_name='create_problems', on_delete=models.CASCADE)

    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    latest_update_datetime = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)
    parent = models.ForeignKey(verbose_name='父问题', to='self', related_name='child', null=True, blank=True,
                               on_delete=models.SET_NULL)

    def __str__(self):
        return self.subject


class Module(models.Model):
    """ 模块（里程碑）,任务可以分不同的阶段"""
    project = models.ForeignKey(verbose_name='项目', to='Project', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='阶段名称', max_length=32)

    def __str__(self):
        return self.title


class IssuesReply(models.Model):
    """ 问题回复"""

    reply_type_choices = (
        (1, '修改记录'),
        (2, '回复')
    )
    reply_type = models.IntegerField(verbose_name='类型', choices=reply_type_choices)

    issues = models.ForeignKey(verbose_name='问题', to='Issues', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='描述')
    creator = models.ForeignKey(verbose_name='创建者', to='UserInfo', related_name='create_reply', on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    reply = models.ForeignKey(verbose_name='回复', to='self', null=True, blank=True, on_delete=models.CASCADE)


class ProjectInvite(models.Model):
    """ 项目邀请码 """
    project = models.ForeignKey(verbose_name='项目', to='Project', on_delete=models.CASCADE)
    code = models.CharField(verbose_name='邀请码', max_length=64, unique=True)
    count = models.PositiveIntegerField(verbose_name='限制数量', null=True, blank=True, help_text='空表示无数量限制')
    use_count = models.PositiveIntegerField(verbose_name='已邀请数量', default=0)
    period_choices = (
        (30, '30分钟'),
        (60, '1小时'),
        (300, '5小时'),
        (1440, '24小时'),
    )
    period = models.IntegerField(verbose_name='有效期', choices=period_choices, default=1440)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    creator = models.ForeignKey(verbose_name='创建者', to='UserInfo', related_name='create_invite', on_delete=models.CASCADE)

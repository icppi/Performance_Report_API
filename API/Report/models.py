from django.db import models
from django.utils import timezone


# 组别表
class GroupModel(models.Model):
    group_name = models.CharField(max_length=250, null=True, blank=None, verbose_name='组名')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='创建日期')

    class Meta:
        db_table = 'Report_Group'
        ordering = ['-id', '-date_joined']
        verbose_name = verbose_name_plural = '团队组名表'


# 成员表
class PersonModel(models.Model):
    username = models.CharField(max_length=250, null=True, blank=None, verbose_name='花名')
    actual_name = models.CharField(max_length=250, null=True, blank=None, verbose_name='真实姓名')
    group_id = models.ForeignKey(to=GroupModel, on_delete=models.CASCADE, to_field='id', verbose_name='团队组ID')
    status = models.BooleanField(null=True, blank=False, verbose_name='新老员工状态')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='创建日期')

    class Meta:
        db_table = 'Report_Person'
        ordering = ['-id', '-date_joined']
        verbose_name = verbose_name_plural = '成员表'


# 新增数据表
class DevelopmentDataModel(models.Model):
    person_id = models.ForeignKey(to=PersonModel, on_delete=models.CASCADE, to_field='id', verbose_name='成员ID')
    new_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='开发量')
    new_customer_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='新客数')
    success_opening_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='成功开场')
    business_introduction_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='业务介绍')
    answer_question_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='解答问题')
    contract_pay_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='约定付款')
    quality_error_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='质检差错数')
    data_time = models.DateField(default=timezone.now, verbose_name='数据日期')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='创建日期')

    class Meta:
        db_table = 'Report_DevelopmentData'
        ordering = ['-id', '-data_time', '-date_joined']
        verbose_name = verbose_name_plural = '新增数据表'


# 回访数据表
class ReturnDataModel(models.Model):
    person_id = models.ForeignKey(to=PersonModel, on_delete=models.CASCADE, to_field='id', verbose_name='成员ID')
    return_visit_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='回访量')
    success_opening_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='成功开场')
    business_introduction_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='业务介绍')
    answer_question_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='解答问题')
    contract_pay_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='约定付款')
    quality_error_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='质检差错数')
    data_time = models.DateField(default=timezone.now, verbose_name='数据日期')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='创建日期')

    class Meta:
        db_table = 'Report_ReturnData'
        ordering = ['-id', '-data_time', '-date_joined']
        verbose_name = verbose_name_plural = '回访数据表'


# 公海数据表
class HighSeasDataModel(models.Model):
    person_id = models.ForeignKey(to=PersonModel, on_delete=models.CASCADE, to_field='id', verbose_name='成员ID')
    high_seas_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='公海量')
    success_opening_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='成功开场')
    business_introduction_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='业务介绍')
    answer_question_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='解答问题')
    contract_pay_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='约定付款')
    quality_error_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='质检差错数')
    data_time = models.DateField(default=timezone.now, verbose_name='数据日期')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='创建日期')

    class Meta:
        db_table = 'Report_HighSeasData'
        ordering = ['-id', '-data_time', '-date_joined']
        verbose_name = verbose_name_plural = '公海数据表'


# 绩效数据表
class PerformanceDataModel(models.Model):
    person_id = models.ForeignKey(to=PersonModel, on_delete=models.CASCADE, to_field='id', verbose_name='成员ID')
    new_addition_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='新加量')
    talkable_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='可聊量')
    work_customer_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='work客户量')
    transaction_volume = models.IntegerField(null=True, blank=True, default=0, verbose_name='成交量')
    source = models.IntegerField(choices={(0, '新增成交'), (1, '回访成交'), (2, '公海成交')}, default=0, verbose_name='数据来源')
    data_time = models.DateField(default=timezone.now, verbose_name='数据日期')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='创建日期')

    class Meta:
        db_table = 'Report_PerformanceData'
        ordering = ['-id', '-data_time', '-date_joined']
        verbose_name = verbose_name_plural = '绩效数据表'

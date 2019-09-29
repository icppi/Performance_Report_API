#!/usr/bin python
# -*- coding: utf-8 -*-
# Python: 3.6
# @Time    : 2019/9/21 10:38
# @Author  : bnightning(QQ:1079056140)
# @Email   : bnightning@163.com
# @File    : serializers.py
# @Software: PyCharm
# Errors should never pass silently.
# Unless explicitly silenced.


from rest_framework import serializers
from API.Report.models import PersonModel, GroupModel, DevelopmentDataModel, ReturnDataModel, PerformanceDataModel, HighSeasDataModel


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonModel
        fields = ('username', 'actual_name', 'status', 'group_id')
        # fields = "__all__"
        # depth = 2


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupModel
        fields = "__all__"


class DevelopmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevelopmentDataModel
        fields = "__all__"
        # depth = 2


class ReturnDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnDataModel
        fields = "__all__"
        # depth = 2


class PerformanceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceDataModel
        fields = "__all__"
        # depth = 2


class HighSeasDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighSeasDataModel
        fields = "__all__"

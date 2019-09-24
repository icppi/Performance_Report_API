#!/usr/bin python
# -*- coding: utf-8 -*-
# Python: 3.6
# @Time    : 2019/9/21 11:14
# @Author  : bnightning(QQ:1079056140)
# @Email   : bnightning@163.com
# @File    : utils.py
# @Software: PyCharm
# Errors should never pass silently.
# Unless explicitly silenced.

from datetime import datetime, timedelta, timezone


def parse_ymd(time):
    # 2019-09-20 00:00:00
    # 2019-09-21 23:59:59
    ymd, hms = time.split(' ')
    year, month, day = ymd.split('-')
    hour, minute, second = hms.split(':')
    data = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    tz_utc_8 = timezone(timedelta(hours=8))
    return data.replace(tzinfo=tz_utc_8)

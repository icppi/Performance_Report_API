#!/usr/bin python
# -*- coding: utf-8 -*-
# Python: 3.6
# @Time    : 2019/9/29 11:28
# @Author  : bnightning(QQ:1079056140)
# @Email   : bnightning@163.com
# @File    : exception_logger.py
# @Software: PyCharm
# Errors should never pass silently.
# Unless explicitly silenced.

import logging


def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("example_logger")
    logger.setLevel(logging.INFO)

    # create the logging file handler
    fh = logging.FileHandler(r"./logs/performance_run.log")

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)
    return logger


logger = create_logger()

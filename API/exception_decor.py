#!/usr/bin python
# -*- coding: utf-8 -*-
# Python: 3.6
# @Time    : 2019/9/29 11:28
# @Author  : bnightning(QQ:1079056140)
# @Email   : bnightning@163.com
# @File    : exception_decor.py
# @Software: PyCharm
# Errors should never pass silently.
# Unless explicitly silenced.

import functools


def exception(logger):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param logger: The logging object
    """

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)

            # re-raise the exception
            raise

        return wrapper

    return decorator

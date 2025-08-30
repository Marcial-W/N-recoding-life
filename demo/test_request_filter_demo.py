# -*- coding: utf-8 -*-
# @Time : 2025/8/30 16:26
# @Author : Marcial
# @Project: data_filter
# @File : test_request_filter_demo.py
# @Software: PyCharm

from request_manage.request_filter import RequestFilter
from request_manage.utils import get_filter_class
from request_manage.request import Request

r1 = Request("http://www.baidu.com/s?wd=python")
r2 = Request("http://www.baidu.com/s", query={'wd':'python'})
r1.name = "r1"
r2.name = "r2"
rs = [r1, r2]

filter = get_filter_class("memory")()
request_filter = RequestFilter(filter)

for r in rs:
    if request_filter.is_exist(r):
        print("请求重复", r.name)
    else:
        fp = request_filter.mark_request(r)
        print("请求未重复", r.name, fp)

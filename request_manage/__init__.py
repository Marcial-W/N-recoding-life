# -*- coding: utf-8 -*-
# @Time : 2025/8/30 13:25
# @Author : Marcial
# @Project: data_filter
# @File : __init__.py
# @Software: PyCharm

"""
请求管理模块 - 提供HTTP请求去重和过滤功能

主要功能:
- Request: HTTP请求对象封装
- RequestFilter: 请求去重过滤器
- 支持多种存储后端: 内存、Redis、MySQL、布隆过滤器
"""

__version__ = "1.0.0"
__author__ = "Marcial"

# 导出主要类
from .request import Request
from .request_filter import RequestFilter
from .utils import get_filter_class, get_available_filters

__all__ = [
    'Request',
    'RequestFilter', 
    'get_filter_class',
    'get_available_filters'
]

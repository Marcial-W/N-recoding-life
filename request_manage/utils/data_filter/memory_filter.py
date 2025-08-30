
# -*- coding: utf-8 -*-
# @Time : 2025/8/23 14:22
# @Author : Marcial
# @File : memery_filter.py
# @Software: PyCharm

from . import BaseFilter

class MemoryFilter(BaseFilter):
    """基于python中的set数据结构实现的内存过滤器"""
    def _get_storage(self):
        return set()

    def _save_data(self, hash_value):
        """
        利用set存储数据
        :param hash_value:
        :return:
        """
        self.storage.add(hash_value)

    def _is_exist(self, hash_value):
        if hash_value in self.storage:
            return True
        return False



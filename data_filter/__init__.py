
# -*- coding: utf-8 -*-
# @Time : 2025/8/23 14:21
# @Author : Marcial
# @File : __init__.py
# @Software: PyCharm

import hashlib
import os

# 基于信息摘要算法的过滤器
class BaseFilter():
    def __init__(self, hash_method='md5'):
        # 初始化
    
        self.hash_method = getattr(hashlib, hash_method)
        self.storage = self._get_storage()

    def _get_storage(self):
        """
        返回对应的存储对象（交给子类实现）
        :return:
        """
        pass

    def _safe_data(self, data) -> bytes:
        """
        安全处理原始数据，将其转换为二进制类型
        :param data: 原始数据（str, bytes, 其他类型）
        :return: bytes 类型数据
        """
        if isinstance(data, bytes):
            return data
        elif isinstance(data, str):
            return data.encode("utf-8")
        else:
            # 统一转成字符串再编码，避免 TypeError
            return str(data).encode("utf-8")

    def _get_hash_value(self, data):
        """
        根据给定的原始数据计算出对应的指纹
        :param data:给定的原始数据：二进制类型的字符串数据
        :return:指纹值(Hash值)
        """
        hash_obj = self.hash_method()
        hash_obj.update(self._safe_data(data))
        hash_value = hash_obj.hexdigest()
        return hash_value

    def save_data(self, data):
        """
        根据data计算出对应的指纹判断后保存
        :param data:给定的原始数据：二进制类型的字符串数据
        :return:存储的结果
        """
        hash_value = self._get_hash_value(data)
        return self._save_data(hash_value)

    def _save_data(self, hash_value):
        """
        存储对应的hash值（交给子类实现）
        :param hash_value:通过信息摘要算法计算出的hash值
        :return:存储的结果
        """
        pass

    def is_exist(self, data):
        """
        判断给定的原始数据是否已经存在
        :param data:给定的原始数据：二进制类型的字符串数据
        :return:True/False
        """
        hash_value = self._get_hash_value(data)
        return self._is_exist(hash_value)

    def _is_exist(self, hash_value):
        """
        根据给定的hash值判断是否已经存在(交给子类实现)
        :param data:通过信息摘要算法计算出的hash值
        :return:True/False
        """
        pass

from . import memory_filter, redis_filter, mysql_filter
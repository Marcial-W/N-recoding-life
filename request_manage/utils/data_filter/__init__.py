
# -*- coding: utf-8 -*-
# @Time : 2025/8/23 14:21
# @Author : Marcial
# @File : __init__.py
# @Software: PyCharm

import hashlib
import os
from abc import ABC, abstractmethod # 添加抽象基类支持

# 基于信息摘要算法的过滤器
class BaseFilter(ABC): # 继承ABC抽象基类
    def __init__(self, hash_method='md5'):
        self.hash_method = getattr(hashlib, hash_method)
        self.storage = self._get_storage()

    @abstractmethod # 标记为抽象方法
    def _get_storage(self):
        """返回对应的存储对象（子类必须实现）"""
        pass

    def _safe_data(self, data) -> bytes:
        """安全处理原始数据，将其转换为二进制类型"""
        if isinstance(data, bytes):
            return data
        elif isinstance(data, str):
            return data.encode("utf-8")
        else:
            return str(data).encode("utf-8") # 统一转成字符串再编码

    def _get_hash_value(self, data):
        """根据给定的原始数据计算出对应的指纹"""
        hash_obj = self.hash_method()
        hash_obj.update(self._safe_data(data))
        return hash_obj.hexdigest() # 直接返回hexdigest

    def save_data(self, data):
        """根据data计算出对应的指纹判断后保存"""
        hash_value = self._get_hash_value(data)
        return self._save_data(hash_value)

    @abstractmethod # 标记为抽象方法
    def _save_data(self, hash_value):
        """存储对应的hash值（子类必须实现）"""
        pass

    def is_exist(self, data):
        """判断给定的原始数据是否已经存在"""
        hash_value = self._get_hash_value(data)
        return self._is_exist(hash_value)

    @abstractmethod # 标记为抽象方法
    def _is_exist(self, hash_value):
        """根据给定的hash值判断是否已经存在(子类必须实现)"""
        pass
    
    def get_stats(self):
        """获取统计信息（子类可重写）"""
        return {'total_records': 0, 'storage_type': 'unknown'}
    
    def clear_all(self):
        """清空所有数据（子类可重写）"""
        return False

from .memory_filter import MemoryFilter
from .redis_filter import RedisFilter
from .mysql_filter import MySQLFilter
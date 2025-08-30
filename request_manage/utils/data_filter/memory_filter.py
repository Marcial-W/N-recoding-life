
# -*- coding: utf-8 -*-
# @Time : 2025/8/23 14:22
# @Author : Marcial
# @File : memory_filter.py # 修复文件名注释
# @Software: PyCharm

from . import BaseFilter

class MemoryFilter(BaseFilter):
    """基于python中的set数据结构实现的内存过滤器"""
    
    def __init__(self, hash_method='md5', max_size=100000): # 添加大小限制参数
        super().__init__(hash_method)
        self.max_size = max_size
        self.storage = self._get_storage()
    
    def _get_storage(self):
        return set()

    def _save_data(self, hash_value):
        """利用set存储数据，超出大小限制时清理旧数据"""
        if len(self.storage) >= self.max_size: # 超出限制时清理
            self._cleanup_old_data()
        self.storage.add(hash_value)
        return True # 返回保存结果

    def _is_exist(self, hash_value):
        return hash_value in self.storage
    
    def _cleanup_old_data(self):
        """清理旧数据，保留最新的50%"""
        if len(self.storage) > 0:
            items = list(self.storage)
            keep_count = max(1, len(items) // 2) # 保留50%
            self.storage = set(items[-keep_count:]) # 保留最新的
    
    def get_stats(self):
        """获取统计信息"""
        return {
            'total_records': len(self.storage),
            'storage_type': 'memory_set',
            'max_size': self.max_size,
            'current_usage': f"{len(self.storage)}/{self.max_size}"
        }
    
    def clear_all(self):
        """清空所有数据"""
        self.storage.clear()
        return True



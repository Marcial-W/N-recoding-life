# -*- coding: utf-8 -*-
# @Time : 2025/8/30 13:25
# @Author : Marcial
# @Project: data_filter
# @File : __init__.py
# @Software: PyCharm

from urllib.parse import urlparse, parse_qsl, urlencode
from typing import Any, Dict, List, Tuple # 添加类型提示

class RequestFilter:
    """请求去重过滤器，支持多种存储后端"""
    
    def __init__(self, filter_obj):
        self.filter_obj = filter_obj
        self._cache = {} # 添加内存缓存提高性能

    def is_exist(self, request_obj) -> bool:
        """判断请求是否已经存在"""
        try:
            data = self._get_request_filter_data(request_obj)
            cache_key = hash(data) # 使用hash作为缓存键
            
            if cache_key in self._cache: # 检查缓存
                return self._cache[cache_key]
            
            result = self.filter_obj.is_exist(data)
            self._cache[cache_key] = result # 缓存结果
            return result
        except Exception as e:
            print(f"检查请求存在性时出错: {e}") # 错误处理
            return False

    def mark_request(self, request_obj) -> bool:
        """标记已经处理过的请求"""
        try:
            data = self._get_request_filter_data(request_obj)
            cache_key = hash(data)
            
            result = self.filter_obj.save_data(data)
            if result: # 保存成功后更新缓存
                self._cache[cache_key] = True
            return result
        except Exception as e:
            print(f"标记请求时出错: {e}") # 错误处理
            return False

    def _get_request_filter_data(self, request_obj) -> str:
        """获取请求对象中需要判断去重的字段并转换成字符串"""
        url = request_obj.url
        method = request_obj.method
        query = request_obj.query.items()
        headers = request_obj.headers
        body = request_obj.body

        parsed_url = urlparse(url)
        url_query = parse_qsl(parsed_url.query)
        url_without_query = parsed_url.scheme + "://" + parsed_url.hostname + (":" + str(parsed_url.port) if parsed_url.port else "") + parsed_url.path
        
        # 优化查询参数合并逻辑
        all_query = sorted(set(list(query) + url_query))
        url_with_query = url_without_query + "?" + urlencode(all_query) if all_query else url_without_query

        method = method.lower()
        headers_str = str(sorted(headers.items())) # 排序确保一致性
        body_str = str(sorted(body.items())) # 排序确保一致性

        return url_with_query + method + headers_str + body_str
    
    def clear_cache(self):
        """清空内存缓存"""
        self._cache.clear()
    
    def get_stats(self):
        """获取过滤器统计信息"""
        try:
            return self.filter_obj.get_stats()
        except:
            return {'error': '无法获取统计信息'}

# -*- coding: utf-8 -*-
# @Time : 2025/8/23 14:21
# @Author : Marcial
# @File : config.py
# @Software: PyCharm

import os
from typing import Optional

class Config:
    """配置类，统一管理数据库连接参数"""
    
    # MySQL配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '123456')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'data1')
    MYSQL_CHARSET = os.getenv('MYSQL_CHARSET', 'utf8')
    
    # MySQL连接池配置
    MYSQL_POOL_SIZE = int(os.getenv('MYSQL_POOL_SIZE', '10'))
    MYSQL_MAX_OVERFLOW = int(os.getenv('MYSQL_MAX_OVERFLOW', '20'))
    MYSQL_POOL_TIMEOUT = int(os.getenv('MYSQL_POOL_TIMEOUT', '30'))
    MYSQL_POOL_RECYCLE = int(os.getenv('MYSQL_POOL_RECYCLE', '3600'))
    MYSQL_ECHO = os.getenv('MYSQL_ECHO', 'False').lower() == 'true'
    
    # Redis配置
    REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB = int(os.getenv('REDIS_DB', '0'))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
    REDIS_KEY = os.getenv('REDIS_KEY', 'filter')
    REDIS_DECODE_RESPONSES = os.getenv('REDIS_DECODE_RESPONSES', 'True').lower() == 'true'
    
    # 应用配置
    HASH_METHOD = os.getenv('HASH_METHOD', 'md5')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def get_mysql_url(cls) -> str:
        """获取MySQL连接URL"""
        return f"mysql+pymysql://{cls.MYSQL_USER}:{cls.MYSQL_PASSWORD}@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DATABASE}?charset={cls.MYSQL_CHARSET}"
    
    @classmethod
    def get_mysql_pool_config(cls) -> dict:
        """获取MySQL连接池配置"""
        return {
            'pool_size': cls.MYSQL_POOL_SIZE,
            'max_overflow': cls.MYSQL_MAX_OVERFLOW,
            'pool_timeout': cls.MYSQL_POOL_TIMEOUT,
            'pool_recycle': cls.MYSQL_POOL_RECYCLE,
            'echo': cls.MYSQL_ECHO
        }
    
    @classmethod
    def get_redis_config(cls) -> dict:
        """获取Redis配置"""
        return {
            'host': cls.REDIS_HOST,
            'port': cls.REDIS_PORT,
            'db': cls.REDIS_DB,
            'password': cls.REDIS_PASSWORD,
            'decode_responses': cls.REDIS_DECODE_RESPONSES
        }
    
    @classmethod
    def print_config(cls):
        """打印当前配置（用于调试）"""
        print("=== 当前配置 ===")
        print(f"MySQL: {cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DATABASE}")
        print(f"Redis: {cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}")
        print(f"Hash方法: {cls.HASH_METHOD}")
        print("================")

# 创建全局配置实例
config = Config() 

# -*- coding: utf-8 -*-
# @Time : 2025/8/23 14:22
# @Author : Marcial
# @File : mysql_filter.py
# @Software: PyCharm

import logging
from contextlib import contextmanager
from typing import Optional

from . import BaseFilter
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# 导入配置
try:
    from config import config
except ImportError:
    # 如果配置文件不存在，使用默认配置
    class DefaultConfig:
        MYSQL_HOST = 'localhost'
        MYSQL_PORT = 3306
        MYSQL_USER = 'root'
        MYSQL_PASSWORD = '123456'
        MYSQL_DATABASE = 'data1'
        MYSQL_CHARSET = 'utf8'
        MYSQL_POOL_SIZE = 10
        MYSQL_MAX_OVERFLOW = 20
        MYSQL_POOL_TIMEOUT = 30
        MYSQL_POOL_RECYCLE = 3600
        MYSQL_ECHO = False
        
        @classmethod
        def get_mysql_url(cls) -> str:
            return f"mysql+pymysql://{cls.MYSQL_USER}:{cls.MYSQL_PASSWORD}@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DATABASE}?charset={cls.MYSQL_CHARSET}"
        
        @classmethod
        def get_mysql_pool_config(cls) -> dict:
            return {
                'pool_size': cls.MYSQL_POOL_SIZE,
                'max_overflow': cls.MYSQL_MAX_OVERFLOW,
                'pool_timeout': cls.MYSQL_POOL_TIMEOUT,
                'pool_recycle': cls.MYSQL_POOL_RECYCLE,
                'echo': cls.MYSQL_ECHO
            }
    
    config = DefaultConfig()

# 配置日志
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

Base = declarative_base()

class Filter(Base):
    # -- 定义表结构 --
    __tablename__ = 'filter'
    id = Column(Integer, primary_key=True)
    hash_value = Column(String(32), index=True, unique=True)
    created_at = Column(DateTime, default=func.now())

class MySQLFilter(BaseFilter):
    """基于MySQL的去重过滤器，使用连接池和session复用"""
    
    # 类级别的引擎和session工厂，所有实例共享
    _engine = None
    _session_factory = None
    
    def __init__(self, mysql_url: Optional[str] = None):
        """
        初始化MySQL过滤器
        :param mysql_url: MySQL连接URL，如果为None则使用配置文件中的设置
        """
        self.mysql_url = mysql_url or config.get_mysql_url()
        
        # 确保数据库连接和表结构已初始化
        self._ensure_initialized()
        
        # 调用父类初始化
        super().__init__()

    @classmethod
    def _ensure_initialized(cls):
        """确保数据库连接和表结构已初始化"""
        if cls._engine is None:
            try:
                # 获取连接池配置
                pool_config = config.get_mysql_pool_config()
                
                # 创建引擎（包含连接池）
                cls._engine = create_engine(
                    cls._get_mysql_url(),
                    **pool_config,
                    # 添加额外的连接参数
                    connect_args={
                        'charset': 'utf8mb4',
                        'autocommit': False,
                        'sql_mode': 'STRICT_TRANS_TABLES'
                    }
                )
                
                # 创建表结构
                Base.metadata.create_all(cls._engine)
                
                # 创建session工厂
                cls._session_factory = sessionmaker(bind=cls._engine)
                
                logger.info("MySQL连接池初始化成功")
                
            except Exception as e:
                logger.error(f"MySQL连接池初始化失败: {e}")
                raise
    
    @classmethod
    def _get_mysql_url(cls) -> str:
        """获取MySQL连接URL（用于类方法）"""
        return config.get_mysql_url()
    
    @contextmanager
    def _get_session(self):
        """获取数据库session的上下文管理器"""
        session = None
        try:
            session = self._session_factory()
            yield session
            session.commit()
        except Exception as e:
            if session:
                session.rollback()
            logger.error(f"数据库操作失败: {e}")
            raise
        finally:
            if session:
                session.close()

    def _get_storage(self):
        '''返回mysql的连接对象（保持兼容性，但推荐使用_get_session）'''
        return self._session_factory()

    def _save_data(self, hash_value: str) -> int:
        """
        保存哈希值到数据库
        :param hash_value: 哈希值
        :return: 1表示成功，0表示失败
        """
        try:
            with self._get_session() as session:
                # 检查是否已存在
                existing = session.query(Filter).filter_by(hash_value=hash_value).first()
                if existing:
                    logger.debug(f"哈希值已存在: {hash_value}")
                    return 0
                
                # 创建新记录
                filter_record = Filter(hash_value=hash_value)
                session.add(filter_record)
                session.commit()
                
                logger.debug(f"哈希值保存成功: {hash_value}")
                return 1
                
        except IntegrityError as e:
            # 处理唯一约束冲突（并发情况下可能发生）
            logger.warning(f"哈希值已存在（并发冲突）: {hash_value}")
            return 0
        except SQLAlchemyError as e:
            logger.error(f"保存哈希值失败: {e}")
            return 0
        except Exception as e:
            logger.error(f"保存哈希值时发生未知错误: {e}")
            return 0

    def _is_exist(self, hash_value: str) -> bool:
        """
        检查哈希值是否已存在
        :param hash_value: 哈希值
        :return: True表示存在，False表示不存在
        """
        try:
            with self._get_session() as session:
                result = session.query(Filter).filter_by(hash_value=hash_value).first()
                return result is not None
                
        except SQLAlchemyError as e:
            logger.error(f"查询哈希值失败: {e}")
            return False
        except Exception as e:
            logger.error(f"查询哈希值时发生未知错误: {e}")
            return False
    
    def get_stats(self) -> dict:
        """
        获取过滤器统计信息
        :return: 包含统计信息的字典
        """
        try:
            with self._get_session() as session:
                total_count = session.query(Filter).count()
                return {
                    'total_records': total_count,
                    'database': config.MYSQL_DATABASE,
                    'table': 'filter'
                }
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            return {'error': str(e)}
    
    def clear_all(self) -> bool:
        """
        清空所有数据（危险操作，谨慎使用）
        :return: True表示成功，False表示失败
        """
        try:
            with self._get_session() as session:
                session.query(Filter).delete()
                session.commit()
                logger.info("所有数据已清空")
                return True
        except Exception as e:
            logger.error(f"清空数据失败: {e}")
            return False
    
    @classmethod
    def close_connections(cls):
        """关闭所有数据库连接（通常在程序结束时调用）"""
        if cls._engine:
            cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None
            logger.info("MySQL连接池已关闭")
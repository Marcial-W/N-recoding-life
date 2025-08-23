# -*- coding: utf-8 -*-
# @Time : 2025/8/23 20:28
# @Author : Marcial
# @Project: data_process
# @File : demo3.py
# @Software: PyCharm

import logging
from data_filter.mysql_filter import MySQLFilter

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # 使用配置文件创建MySQL过滤器实例
        filter = MySQLFilter()
        
        # 打印配置信息
        from config import config
        config.print_config()
        
        data = ['111', '222', '111', '222', 'hello', 'world', 'python', 'is', 'awesome']

        print("开始处理数据...")
        saved_count = 0
        existing_count = 0
        
        for i in data:
            if filter.is_exist(i):
                print(f"'{i}' 已存在")
                existing_count += 1
            else:
                result = filter.save_data(i)
                if result == 1:
                    print(f"'{i}' 保存成功")
                    saved_count += 1
                else:
                    print(f"'{i}' 保存失败")
                    existing_count += 1

        print(f"\n处理完成！")
        print(f"新增数据: {saved_count} 条")
        print(f"重复数据: {existing_count} 条")
        
        # 获取统计信息
        stats = filter.get_stats()
        print(f"\n数据库统计信息: {stats}")
        
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        print(f"程序执行出错: {e}")
    finally:
        # 程序结束时关闭MySQL连接
        try:
            MySQLFilter.close_connections()
            print("MySQL连接已关闭")
        except Exception as e:
            logger.error(f"关闭MySQL连接时出错: {e}")
            print(f"关闭MySQL连接时出错: {e}")

if __name__ == "__main__":
    main()

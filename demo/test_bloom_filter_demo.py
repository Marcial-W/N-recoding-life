# -*- coding: utf-8 -*-
# @Time : 2025/8/24 15:40
# @Author : Marcial
# @Project: data_process
# @File : test_bloom_filter_demo.py
# @Software: PyCharm

import logging
from request_manage.utils.data_filter.bloomfilter import BloomFilter

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # 使用配置文件创建布隆过滤器实例
        bf = BloomFilter()
        
        # 打印配置信息
        from request_manage.utils.config import config
        config.print_config()
        
        # 测试数据
        data = ['111', '222', '111', '222', 'hello', 'world', 'python', 'is', 'awesome', 'python']

        print("开始处理数据...")
        saved_count = 0
        existing_count = 0
        
        for i in data:
            if bf.is_exist(i):
                print(f"'{i}' 已存在")
                existing_count += 1
            else:
                result = bf.save_data(i)
                if result:
                    print(f"'{i}' 保存成功")
                    saved_count += 1
                else:
                    print(f"'{i}' 保存失败")
                    existing_count += 1

        print(f"\n处理完成！")
        print(f"新增数据: {saved_count} 条")
        print(f"重复数据: {existing_count} 条")
        
        # 获取统计信息
        stats = bf.get_stats()
        print(f"\n布隆过滤器统计信息: {stats}")
        
        # 测试误判
        print("\n测试误判情况:")
        test_items = ['new_item_1', 'new_item_2', 'new_item_3']
        for item in test_items:
            if bf.is_exist(item):
                print(f"'{item}' 可能存在（可能是误判）")
            else:
                print(f"'{item}' 确定不存在")
        
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        print(f"程序执行出错: {e}")
    finally:
        # 程序结束时关闭Redis连接
        try:
            bf.close_connection()
            print("Redis连接已关闭")
        except Exception as e:
            logger.error(f"关闭Redis连接时出错: {e}")
            print(f"关闭Redis连接时出错: {e}")

if __name__ == "__main__":
    main() 
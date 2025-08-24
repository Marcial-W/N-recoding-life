# -*- coding: utf-8 -*-
# @Time : 2025/8/23 15:06
# @Author : Marcial
# @Project: data_process
# @File : test_mysql_filter.py
# @Software: PyCharm

import logging
import time
from data_filter.mysql_filter import MySQLFilter

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_mysql_connection():
    """测试MySQL连接"""
    print("=== 测试MySQL连接 ===")
    
    try:
        # 测试过滤器创建
        filter = MySQLFilter()
        print("✓ MySQLFilter创建成功")
        
        # 测试基本功能
        test_data = ['test1', 'test2', 'test1']  # 包含重复数据
        
        print("测试数据去重功能:")
        for item in test_data:
            if filter.is_exist(item):
                print(f"  '{item}' 已存在")
            else:
                result = filter.save_data(item)
                print(f"  '{item}' 已保存 (结果: {result})")
        
        # 获取统计信息
        stats = filter.get_stats()
        print(f"\n数据库统计信息: {stats}")
        
        # 清理测试数据
        filter.clear_all()
        print("✓ 清理测试数据完成")
        
        return True
        
    except Exception as e:
        print(f"✗ MySQL连接失败: {e}")
        return False

def test_connection_pool():
    """测试连接池复用"""
    print("\n=== 测试连接池复用 ===")
    
    try:
        # 创建多个实例，应该共享同一个连接池
        filter1 = MySQLFilter()
        filter2 = MySQLFilter()
        
        # 检查引擎是否相同
        if filter1._engine is filter2._engine:
            print("✓ 连接池复用成功")
        else:
            print("✗ 连接池复用失败")
        
        # 测试并发操作
        test_data = [f"concurrent_test_{i}" for i in range(10)]
        
        print("测试并发操作:")
        for item in test_data:
            filter1.save_data(item)
        
        # 验证结果
        stats = filter1.get_stats()
        print(f"并发操作后统计: {stats}")
        
        # 清理
        filter1.clear_all()
        
        return True
        
    except Exception as e:
        print(f"✗ 连接池测试失败: {e}")
        return False

def test_performance():
    """测试性能"""
    print("\n=== 测试性能 ===")
    
    try:
        filter = MySQLFilter()
        
        # 测试大量数据插入
        test_data = [f"perf_test_{i}" for i in range(100)]
        
        start_time = time.time()
        
        for item in test_data:
            filter.save_data(item)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"插入 {len(test_data)} 条数据耗时: {elapsed_time:.4f} 秒")
        print(f"平均每条数据: {elapsed_time/len(test_data)*1000:.2f} 毫秒")
        
        # 测试查询性能
        start_time = time.time()
        
        for item in test_data:
            filter.is_exist(item)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"查询 {len(test_data)} 条数据耗时: {elapsed_time:.4f} 秒")
        print(f"平均每条数据: {elapsed_time/len(test_data)*1000:.2f} 毫秒")
        
        # 清理
        filter.clear_all()
        
        print("✓ 性能测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 性能测试失败: {e}")
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n=== 测试错误处理 ===")
    
    try:
        filter = MySQLFilter()
        
        # 测试重复数据插入
        test_item = "error_test_item"
        
        # 第一次插入
        result1 = filter.save_data(test_item)
        print(f"第一次插入结果: {result1}")
        
        # 第二次插入（应该失败）
        result2 = filter.save_data(test_item)
        print(f"第二次插入结果: {result2}")
        
        # 验证存在性
        exists = filter.is_exist(test_item)
        print(f"数据存在性: {exists}")
        
        # 清理
        filter.clear_all()
        
        print("✓ 错误处理测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 错误处理测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始MySQL过滤器测试...\n")
    
    # 运行所有测试
    tests = [
        test_mysql_connection,
        test_connection_pool,
        test_performance,
        test_error_handling
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"测试执行出错: {e}")
            results.append(False)
    
    print(f"\n=== 测试结果汇总 ===")
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("❌ 部分测试失败，请检查配置")
    
    # 关闭所有连接
    try:
        MySQLFilter.close_connections()
        print("MySQL连接已关闭")
    except Exception as e:
        print(f"关闭连接时出错: {e}") 
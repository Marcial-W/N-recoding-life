# -*- coding: utf-8 -*-
# @Time : 2025/8/23 15:06
# @Author : Marcial
# @Project: data_process
# @File : test_redis_filter.py
# @Software: PyCharm

import logging
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from data_filter.redis_filter import RedisFilter
import redis

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_redis_connection():
    """测试Redis连接"""
    print("=== 测试Redis连接 ===")
    
    try:
        # 测试直接连接
        r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
        r.ping()
        print("✓ Redis服务连接成功")
        
        # 测试过滤器连接
        filter = RedisFilter()
        print("✓ RedisFilter创建成功")
        
        # 清理测试数据
        r.delete('filter')
        print("✓ 清理测试数据完成")
        
        return True
        
    except Exception as e:
        print(f"✗ Redis连接失败: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    print("\n=== 测试基本功能 ===")
    
    try:
        filter = RedisFilter()
        
        # 测试数据
        test_data = ['test1', 'test2', 'test1', 'test3']  # 包含重复数据
        
        print("测试数据去重功能:")
        saved_count = 0
        existing_count = 0
        
        for item in test_data:
            if filter.is_exist(item):
                print(f"  '{item}' 已存在")
                existing_count += 1
            else:
                result = filter.save_data(item)
                if result == 1:
                    print(f"  '{item}' 已保存")
                    saved_count += 1
                else:
                    print(f"  '{item}' 保存失败")
                    existing_count += 1
        
        print(f"新增数据: {saved_count} 条")
        print(f"重复数据: {existing_count} 条")
        
        # 验证结果
        r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
        members = r.smembers('filter')
        print(f"Redis中的实际数据: {members}")
        
        # 清理
        r.delete('filter')
        filter.close_connection()
        
        print("✓ 基本功能测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 基本功能测试失败: {e}")
        return False

def test_connection_pool():
    """测试连接池复用"""
    print("\n=== 测试连接池复用 ===")
    
    try:
        # 创建多个实例，应该共享同一个连接池
        filter1 = RedisFilter()
        filter2 = RedisFilter()
        
        # 检查连接池是否相同
        pool1 = filter1._get_connection_pool()
        pool2 = filter2._get_connection_pool()
        
        if pool1 is pool2:
            print("✓ 连接池复用成功")
        else:
            print("✗ 连接池复用失败")
        
        # 测试并发操作
        test_data = [f"pool_test_{i}" for i in range(10)]
        
        print("测试并发操作:")
        for item in test_data:
            filter1.save_data(item)
        
        # 验证结果
        stats = filter1.get_stats()
        print(f"并发操作后统计: {stats}")
        
        # 清理
        filter1.clear_all()
        filter1.close_connection()
        filter2.close_connection()
        
        return True
        
    except Exception as e:
        print(f"✗ 连接池测试失败: {e}")
        return False

def test_performance():
    """测试性能"""
    print("\n=== 测试性能 ===")
    
    try:
        filter = RedisFilter()
        
        # 测试大量数据插入
        test_data = [f"perf_test_{i}" for i in range(1000)]
        
        print("测试插入性能:")
        start_time = time.time()
        
        for item in test_data:
            filter.save_data(item)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"插入 {len(test_data)} 条数据耗时: {elapsed_time:.4f} 秒")
        print(f"平均每条数据: {elapsed_time/len(test_data)*1000:.2f} 毫秒")
        print(f"每秒处理: {len(test_data)/elapsed_time:.0f} 条")
        
        # 测试查询性能
        print("\n测试查询性能:")
        start_time = time.time()
        
        for item in test_data:
            filter.is_exist(item)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"查询 {len(test_data)} 条数据耗时: {elapsed_time:.4f} 秒")
        print(f"平均每条数据: {elapsed_time/len(test_data)*1000:.2f} 毫秒")
        print(f"每秒查询: {len(test_data)/elapsed_time:.0f} 条")
        
        # 清理
        filter.clear_all()
        filter.close_connection()
        
        print("✓ 性能测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 性能测试失败: {e}")
        return False

def test_concurrent_operations():
    """测试并发操作"""
    print("\n=== 测试并发操作 ===")
    
    try:
        filter = RedisFilter()
        
        # 准备测试数据
        test_data = [f"concurrent_test_{i}" for i in range(100)]
        
        def worker(data_chunk):
            """工作线程函数"""
            results = []
            for item in data_chunk:
                if not filter.is_exist(item):
                    result = filter.save_data(item)
                    results.append((item, result))
            return results
        
        # 将数据分成多个块
        chunk_size = 20
        data_chunks = [test_data[i:i+chunk_size] for i in range(0, len(test_data), chunk_size)]
        
        print(f"使用 {len(data_chunks)} 个线程并发处理 {len(test_data)} 条数据")
        
        start_time = time.time()
        
        # 使用线程池执行并发操作
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(worker, chunk) for chunk in data_chunks]
            results = []
            for future in as_completed(futures):
                results.extend(future.result())
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"并发处理耗时: {elapsed_time:.4f} 秒")
        print(f"成功处理: {len(results)} 条数据")
        
        # 验证结果
        stats = filter.get_stats()
        print(f"最终统计: {stats}")
        
        # 清理
        filter.clear_all()
        filter.close_connection()
        
        print("✓ 并发操作测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 并发操作测试失败: {e}")
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n=== 测试错误处理 ===")
    
    try:
        filter = RedisFilter()
        
        # 测试重复数据插入
        test_item = "error_test_item"
        
        # 第一次插入
        result1 = filter.save_data(test_item)
        print(f"第一次插入结果: {result1}")
        
        # 第二次插入（应该返回0，表示已存在）
        result2 = filter.save_data(test_item)
        print(f"第二次插入结果: {result2}")
        
        # 验证存在性
        exists = filter.is_exist(test_item)
        print(f"数据存在性: {exists}")
        
        # 测试无效数据
        print("\n测试无效数据处理:")
        invalid_data = [None, "", "   ", 123, 0, True, False]
        
        for item in invalid_data:
            try:
                result = filter.save_data(item)
                print(f"  '{item}' -> 结果: {result}")
            except Exception as e:
                print(f"  '{item}' -> 异常: {e}")
        
        # 清理
        filter.clear_all()
        filter.close_connection()
        
        print("✓ 错误处理测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 错误处理测试失败: {e}")
        return False

def test_custom_config():
    """测试自定义配置"""
    print("\n=== 测试自定义配置 ===")
    
    try:
        # 使用自定义配置创建过滤器
        custom_filter = RedisFilter(
            redis_host='127.0.0.1',
            redis_port=6379,
            redis_db=1,  # 使用不同的数据库
            redis_key='custom_filter',
            redis_decode_responses=True
        )
        
        print("✓ 自定义配置过滤器创建成功")
        
        # 测试基本功能
        test_data = ['custom1', 'custom2', 'custom1']
        
        for item in test_data:
            if custom_filter.is_exist(item):
                print(f"  '{item}' 已存在")
            else:
                result = custom_filter.save_data(item)
                print(f"  '{item}' 保存结果: {result}")
        
        # 验证数据保存在正确的key中
        r = redis.Redis(host='127.0.0.1', port=6379, db=1, decode_responses=True)
        members = r.smembers('custom_filter')
        print(f"自定义key中的数据: {members}")
        
        # 清理
        r.delete('custom_filter')
        custom_filter.close_connection()
        
        print("✓ 自定义配置测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 自定义配置测试失败: {e}")
        return False

def test_stats_and_management():
    """测试统计信息和管理功能"""
    print("\n=== 测试统计信息和管理功能 ===")
    
    try:
        filter = RedisFilter()
        
        # 添加一些测试数据
        test_data = [f"stats_test_{i}" for i in range(50)]
        
        for item in test_data:
            filter.save_data(item)
        
        # 获取统计信息
        stats = filter.get_stats()
        print(f"统计信息: {stats}")
        
        # 验证统计信息
        expected_count = len(set(test_data))  # 去重后的数量
        actual_count = stats.get('total_records', 0)
        
        if actual_count == expected_count:
            print(f"✓ 统计信息正确: {actual_count} 条记录")
        else:
            print(f"✗ 统计信息错误: 期望 {expected_count}, 实际 {actual_count}")
        
        # 测试数据清理
        print("\n测试数据清理功能:")
        clear_result = filter.clear_all()
        print(f"清理结果: {clear_result}")
        
        # 验证清理结果
        stats_after_clear = filter.get_stats()
        print(f"清理后统计: {stats_after_clear}")
        
        if stats_after_clear.get('total_records', 0) == 0:
            print("✓ 数据清理成功")
        else:
            print("✗ 数据清理失败")
        
        filter.close_connection()
        
        print("✓ 统计信息和管理功能测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 统计信息和管理功能测试失败: {e}")
        return False

def test_memory_usage():
    """测试内存使用情况"""
    print("\n=== 测试内存使用情况 ===")
    
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"初始内存使用: {initial_memory:.2f} MB")
        
        filter = RedisFilter()
        
        # 添加大量数据
        large_data = [f"memory_test_{i}" for i in range(10000)]
        
        for i, item in enumerate(large_data):
            filter.save_data(item)
            if i % 1000 == 0:
                current_memory = process.memory_info().rss / 1024 / 1024
                print(f"处理 {i} 条数据后内存: {current_memory:.2f} MB")
        
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_increase = final_memory - initial_memory
        
        print(f"最终内存使用: {final_memory:.2f} MB")
        print(f"内存增长: {memory_increase:.2f} MB")
        
        # 清理
        filter.clear_all()
        filter.close_connection()
        
        # 清理后内存
        cleanup_memory = process.memory_info().rss / 1024 / 1024
        print(f"清理后内存: {cleanup_memory:.2f} MB")
        
        print("✓ 内存使用测试完成")
        return True
        
    except ImportError:
        print("⚠️ psutil模块未安装，跳过内存测试")
        return True
    except Exception as e:
        print(f"✗ 内存使用测试失败: {e}")
        return False

def test_connection_recovery():
    """测试连接恢复"""
    print("\n=== 测试连接恢复 ===")
    
    try:
        filter = RedisFilter()
        
        # 正常操作
        filter.save_data("recovery_test_1")
        print("✓ 正常操作成功")
        
        # 模拟连接断开（通过关闭连接池）
        filter.close_connection()
        print("✓ 连接已关闭")
        
        # 重新创建过滤器（应该自动重新连接）
        new_filter = RedisFilter()
        new_filter.save_data("recovery_test_2")
        print("✓ 连接恢复成功")
        
        # 验证数据
        stats = new_filter.get_stats()
        print(f"恢复后统计: {stats}")
        
        # 清理
        new_filter.clear_all()
        new_filter.close_connection()
        
        print("✓ 连接恢复测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 连接恢复测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始Redis过滤器全面测试...\n")
    
    # 运行所有测试
    tests = [
        ("Redis连接测试", test_redis_connection),
        ("基本功能测试", test_basic_functionality),
        ("连接池测试", test_connection_pool),
        ("性能测试", test_performance),
        ("并发操作测试", test_concurrent_operations),
        ("错误处理测试", test_error_handling),
        ("自定义配置测试", test_custom_config),
        ("统计信息测试", test_stats_and_management),
        ("内存使用测试", test_memory_usage),
        ("连接恢复测试", test_connection_recovery)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"开始执行: {test_name}")
        print('='*50)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"测试执行出错: {e}")
            results.append((test_name, False))
    
    print(f"\n{'='*60}")
    print("测试结果汇总")
    print('='*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！Redis过滤器工作正常")
    else:
        print("❌ 部分测试失败，请检查Redis配置和连接")
    
    print("\n测试完成！") 
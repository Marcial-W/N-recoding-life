# -*- coding: utf-8 -*-
# @Time : 2025/8/24 15:40
# @Author : Marcial
# @Project: data_process
# @File : test_bloom_filter.py
# @Software: PyCharm

import logging
import time
from data_filter.bloomfilter import BloomFilter

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_basic_functionality():
    """测试基本功能"""
    print("=== 测试基本功能 ===")
    
    try:
        bf = BloomFilter()
        
        # 测试数据
        test_data = ['test1', 'test2', 'test1', 'test3']  # 包含重复数据
        
        print("测试数据去重功能:")
        saved_count = 0
        existing_count = 0
        
        for item in test_data:
            if bf.is_exist(item):
                print(f"  '{item}' 已存在")
                existing_count += 1
            else:
                if bf.save_data(item):
                    print(f"  '{item}' 保存成功")
                    saved_count += 1
                else:
                    print(f"  '{item}' 保存失败")
                    existing_count += 1
        
        print(f"新增数据: {saved_count} 条")
        print(f"重复数据: {existing_count} 条")
        
        # 获取统计信息
        stats = bf.get_stats()
        print(f"统计信息: {stats}")
        
        # 清理
        bf.clear_all()
        bf.close_connection()
        
        print("✓ 基本功能测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 基本功能测试失败: {e}")
        return False

def test_performance():
    """测试性能"""
    print("\n=== 测试性能 ===")
    
    try:
        bf = BloomFilter()
        
        # 测试大量数据插入
        test_data = [f"perf_test_{i}" for i in range(1000)]
        
        print("测试插入性能:")
        start_time = time.time()
        
        for item in test_data:
            if not bf.is_exist(item):
                bf.save_data(item)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"处理 {len(test_data)} 条数据耗时: {elapsed_time:.4f} 秒")
        print(f"平均每条数据: {elapsed_time/len(test_data)*1000:.2f} 毫秒")
        print(f"每秒处理: {len(test_data)/elapsed_time:.0f} 条")
        
        # 测试查询性能
        print("\n测试查询性能:")
        start_time = time.time()
        
        for item in test_data:
            bf.is_exist(item)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"查询 {len(test_data)} 条数据耗时: {elapsed_time:.4f} 秒")
        print(f"平均每条数据: {elapsed_time/len(test_data)*1000:.2f} 毫秒")
        print(f"每秒查询: {len(test_data)/elapsed_time:.0f} 条")
        
        # 清理
        bf.clear_all()
        bf.close_connection()
        
        print("✓ 性能测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 性能测试失败: {e}")
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n=== 测试错误处理 ===")
    
    try:
        bf = BloomFilter()
        
        # 测试重复数据插入
        test_item = "error_test_item"
        
        # 第一次插入
        result1 = bf.save_data(test_item)
        print(f"第一次插入结果: {result1}")
        
        # 第二次插入（应该成功，因为布隆过滤器允许重复）
        result2 = bf.save_data(test_item)
        print(f"第二次插入结果: {result2}")
        
        # 验证存在性
        exists = bf.is_exist(test_item)
        print(f"数据存在性: {exists}")
        
        # 测试无效数据
        print("\n测试无效数据处理:")
        invalid_data = [None, "", "   ", 123, 0, True, False]
        
        for item in invalid_data:
            try:
                result = bf.save_data(item)
                print(f"  '{item}' -> 结果: {result}")
            except Exception as e:
                print(f"  '{item}' -> 异常: {e}")
        
        # 清理
        bf.clear_all()
        bf.close_connection()
        
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
        custom_bf = BloomFilter(
            redis_host='127.0.0.1',
            redis_port=6379,
            redis_db=1,  # 使用不同的数据库
            redis_key='custom_bloom_filter',
            hash_salts=['salt1', 'salt2', 'salt3', 'salt4']  # 自定义盐值
        )
        
        print("✓ 自定义配置过滤器创建成功")
        
        # 测试基本功能
        test_data = ['custom1', 'custom2', 'custom1']
        
        for item in test_data:
            if custom_bf.is_exist(item):
                print(f"  '{item}' 已存在")
            else:
                result = custom_bf.save_data(item)
                print(f"  '{item}' 保存结果: {result}")
        
        # 获取统计信息
        stats = custom_bf.get_stats()
        print(f"自定义配置统计: {stats}")
        
        # 清理
        custom_bf.clear_all()
        custom_bf.close_connection()
        
        print("✓ 自定义配置测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 自定义配置测试失败: {e}")
        return False

def test_false_positive():
    """测试误判率"""
    print("\n=== 测试误判率 ===")
    
    try:
        bf = BloomFilter()
        
        # 添加一些数据
        original_data = [f"original_{i}" for i in range(100)]
        for item in original_data:
            bf.save_data(item)
        
        # 测试一些不存在的数据
        test_data = [f"test_{i}" for i in range(100)]
        false_positives = 0
        
        for item in test_data:
            if bf.is_exist(item):
                false_positives += 1
        
        false_positive_rate = false_positives / len(test_data) * 100
        print(f"误判数量: {false_positives}")
        print(f"误判率: {false_positive_rate:.2f}%")
        
        # 清理
        bf.clear_all()
        bf.close_connection()
        
        print("✓ 误判率测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 误判率测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始布隆过滤器全面测试...\n")
    
    # 运行所有测试
    tests = [
        ("基本功能测试", test_basic_functionality),
        ("性能测试", test_performance),
        ("错误处理测试", test_error_handling),
        ("自定义配置测试", test_custom_config),
        ("误判率测试", test_false_positive)
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
        print("🎉 所有测试通过！布隆过滤器工作正常")
    else:
        print("❌ 部分测试失败，请检查Redis配置和连接")
    
    print("\n测试完成！") 
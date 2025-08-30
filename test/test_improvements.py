# -*- coding: utf-8 -*-
# @Time : 2025/8/30 17:30
# @Author : Marcial
# @Project: data_process
# @File : test_improvements.py
# @Software: PyCharm

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from request_manage import Request, RequestFilter, get_filter_class, get_available_filters

def test_request_improvements():
    """测试改进后的Request类功能"""
    print("=== 测试Request类改进功能 ===")
    
    try:
        # 测试基本创建
        r1 = Request("https://test.com", "POST", {"key": "value"})
        print(f"✓ 创建请求成功: {r1}")
        
        # 测试属性访问器
        print(f"  URL: {r1.url}")
        print(f"  方法: {r1.method}")
        print(f"  查询参数: {r1.query}")
        
        # 测试添加参数
        r1.add_query_param("new_key", "new_value")
        r1.add_header("User-Agent", "TestBot")
        r1.add_body_param("data", "test_data")
        
        print(f"  添加参数后查询: {r1.query}")
        print(f"  添加参数后请求头: {r1.headers}")
        print(f"  添加参数后请求体: {r1.body}")
        
        # 测试名称设置
        r1.name = "test_request"
        print(f"  请求名称: {r1.name}")
        
        return True
        
    except Exception as e:
        print(f"✗ Request类测试失败: {e}")
        return False

def test_filter_improvements():
    """测试改进后的过滤器功能"""
    print("\n=== 测试过滤器改进功能 ===")
    
    try:
        # 测试获取可用过滤器
        available = get_available_filters()
        print(f"✓ 可用过滤器类型: {available}")
        
        # 测试内存过滤器改进
        memory_filter = get_filter_class("memory")(max_size=100)
        print(f"✓ 创建内存过滤器成功，最大大小: {memory_filter.max_size}")
        
        # 测试统计信息
        stats = memory_filter.get_stats()
        print(f"  初始统计: {stats}")
        
        # 测试数据保存和清理
        for i in range(150): # 超出大小限制
            memory_filter.save_data(f"test_data_{i}")
        
        stats = memory_filter.get_stats()
        print(f"  超出限制后统计: {stats}")
        
        # 测试清理功能
        memory_filter.clear_all()
        stats = memory_filter.get_stats()
        print(f"  清理后统计: {stats}")
        
        return True
        
    except Exception as e:
        print(f"✗ 过滤器改进测试失败: {e}")
        return False

def test_request_filter_improvements():
    """测试改进后的RequestFilter功能"""
    print("\n=== 测试RequestFilter改进功能 ===")
    
    try:
        # 创建过滤器
        memory_filter = get_filter_class("memory")()
        request_filter = RequestFilter(memory_filter)
        
        # 创建测试请求
        r1 = Request("https://test1.com", "GET", {"id": "1"})
        r2 = Request("https://test2.com", "POST", {"id": "2"})
        
        # 测试缓存功能
        print("测试缓存功能:")
        result1 = request_filter.is_exist(r1)
        result2 = request_filter.is_exist(r1) # 第二次应该使用缓存
        print(f"  第一次检查: {result1}")
        print(f"  第二次检查: {result2}")
        
        # 测试标记请求
        mark_result = request_filter.mark_request(r1)
        print(f"  标记请求结果: {mark_result}")
        
        # 测试统计信息
        stats = request_filter.get_stats()
        print(f"  过滤器统计: {stats}")
        
        # 测试清空缓存
        request_filter.clear_cache()
        print("✓ 缓存清空成功")
        
        return True
        
    except Exception as e:
        print(f"✗ RequestFilter改进测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试改进后的代码功能...\n")
    
    tests = [
        test_request_improvements,
        test_filter_improvements,
        test_request_filter_improvements
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
        print("🎉 所有改进功能测试通过！")
    else:
        print("❌ 部分改进功能测试失败，请检查代码") 
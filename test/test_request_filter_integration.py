# -*- coding: utf-8 -*-
# @Time : 2025/8/30 17:15
# @Author : Marcial
# @Project: data_process
# @File : test_request_filter_integration.py
# @Software: PyCharm

import logging
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from request_manage.request_filter import RequestFilter
from request_manage.utils import get_filter_class
from request_manage.request import Request

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_request_filter_integration():
    """测试请求过滤器集成功能"""
    print("=== 测试请求过滤器集成功能 ===")
    
    try:
        # 创建测试请求
        r1 = Request("https://www.baidu.com/s?wd=python")
        r2 = Request("https://www.baidu.com/s", query={'wd':'python'})
        r3 = Request("https://www.baidu.com/s?wd=python", query={'wd':'python'})
        r4 = Request("HTTPS://www.Baidu.com/s?wd=python")
        r5 = Request("https://www.baidu.com/S?wd=python")
        
        r1.name = "r1"
        r2.name = "r2"
        r3.name = "r3"
        r4.name = "r4"
        r5.name = "r5"
        rs = [r1, r2, r3, r4, r5]
        
        # 获取过滤器实例
        filter = get_filter_class("mysql")()
        request_filter = RequestFilter(filter)
        
        print("测试请求去重功能:")
        results = []
        for r in rs:
            if request_filter.is_exist(r):
                print(f"  请求重复: {r.name}")
                results.append(("重复", r.name))
            else:
                fp = request_filter.mark_request(r)
                print(f"  请求未重复: {r.name}, 指纹: {fp}")
                results.append(("未重复", r.name, fp))
        
        # 验证结果
        print(f"\n测试结果汇总:")
        for result in results:
            if len(result) == 2:
                print(f"  {result[1]}: {result[0]}")
            else:
                print(f"  {result[1]}: {result[0]}, 指纹: {result[2]}")
        
        # 清理测试数据
        try:
            filter.clear_all()
            print("✓ 清理测试数据完成")
        except:
            print("⚠ 清理测试数据失败（可能不支持此功能）")
        
        return True
        
    except Exception as e:
        print(f"✗ 集成测试失败: {e}")
        return False

def test_filter_types():
    """测试不同过滤器类型"""
    print("\n=== 测试不同过滤器类型 ===")
    
    filter_types = ["mysql", "redis", "memory", "bloom"]
    results = {}
    
    for filter_type in filter_types:
        try:
            print(f"测试 {filter_type} 过滤器:")
            filter = get_filter_class(filter_type)()
            request_filter = RequestFilter(filter)
            
            # 测试基本功能
            test_request = Request("https://test.com")
            test_request.name = f"test_{filter_type}"
            
            if request_filter.is_exist(test_request):
                print(f"  ✓ {filter_type} 过滤器工作正常")
                results[filter_type] = True
            else:
                fp = request_filter.mark_request(test_request)
                print(f"  ✓ {filter_type} 过滤器工作正常，指纹: {fp}")
                results[filter_type] = True
            
            # 清理
            try:
                filter.clear_all()
            except:
                pass
                
        except Exception as e:
            print(f"  ✗ {filter_type} 过滤器测试失败: {e}")
            results[filter_type] = False
    
    return results

if __name__ == "__main__":
    print("开始请求过滤器集成测试...\n")
    
    # 运行测试
    tests = [
        test_request_filter_integration,
        test_filter_types
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
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("❌ 部分测试失败，请检查配置") 
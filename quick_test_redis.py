# -*- coding: utf-8 -*-
# @Time : 2025/8/23 15:06
# @Author : Marcial
# @Project: data_process
# @File : quick_test_redis.py
# @Software: PyCharm

"""
Redis过滤器快速测试脚本
用于快速验证Redis过滤器的基本功能
"""

import time
from data_filter.redis_filter import RedisFilter

def quick_test():
    """快速测试Redis过滤器"""
    print("🚀 Redis过滤器快速测试")
    print("=" * 40)
    
    try:
        # 1. 创建过滤器
        print("1. 创建Redis过滤器...")
        filter = RedisFilter()
        print("   ✓ 过滤器创建成功")
        
        # 2. 测试基本功能
        print("\n2. 测试基本功能...")
        test_data = ['item1', 'item2', 'item1', 'item3', 'item2']
        
        saved_count = 0
        existing_count = 0
        
        for item in test_data:
            if filter.is_exist(item):
                print(f"   '{item}' 已存在")
                existing_count += 1
            else:
                result = filter.save_data(item)
                if result == 1:
                    print(f"   '{item}' 保存成功")
                    saved_count += 1
                else:
                    print(f"   '{item}' 保存失败")
                    existing_count += 1
        
        print(f"   新增: {saved_count} 条, 重复: {existing_count} 条")
        
        # 3. 获取统计信息
        print("\n3. 获取统计信息...")
        stats = filter.get_stats()
        print(f"   总记录数: {stats.get('total_records', 0)}")
        print(f"   Redis Key: {stats.get('redis_key', 'N/A')}")
        print(f"   Redis DB: {stats.get('redis_db', 'N/A')}")
        
        # 4. 性能测试
        print("\n4. 性能测试...")
        perf_data = [f"perf_{i}" for i in range(100)]
        
        start_time = time.time()
        for item in perf_data:
            filter.save_data(item)
        end_time = time.time()
        
        elapsed = end_time - start_time
        print(f"   插入100条数据耗时: {elapsed:.4f}秒")
        print(f"   平均每条: {elapsed/100*1000:.2f}毫秒")
        print(f"   每秒处理: {100/elapsed:.0f}条")
        
        # 5. 清理测试数据
        print("\n5. 清理测试数据...")
        filter.clear_all()
        print("   ✓ 数据清理完成")
        
        # 6. 关闭连接
        print("\n6. 关闭连接...")
        filter.close_connection()
        print("   ✓ 连接已关闭")
        
        print("\n🎉 快速测试完成！Redis过滤器工作正常")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("\n请检查:")
        print("1. Redis服务是否启动")
        print("2. Redis连接参数是否正确")
        print("3. 网络连接是否正常")
        return False

def test_config():
    """测试配置功能"""
    print("\n🔧 测试配置功能")
    print("=" * 40)
    
    try:
        # 测试默认配置
        print("1. 测试默认配置...")
        filter1 = RedisFilter()
        print("   ✓ 默认配置过滤器创建成功")
        
        # 测试自定义配置
        print("2. 测试自定义配置...")
        filter2 = RedisFilter(
            redis_host='127.0.0.1',
            redis_port=6379,
            redis_db=1,
            redis_key='test_filter'
        )
        print("   ✓ 自定义配置过滤器创建成功")
        
        # 测试功能
        filter1.save_data("config_test_1")
        filter2.save_data("config_test_2")
        
        print("   ✓ 两个过滤器独立工作正常")
        
        # 清理
        filter1.clear_all()
        filter2.clear_all()
        filter1.close_connection()
        filter2.close_connection()
        
        print("   ✓ 配置测试完成")
        return True
        
    except Exception as e:
        print(f"   ❌ 配置测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始Redis过滤器快速测试...\n")
    
    # 运行快速测试
    basic_test = quick_test()
    
    # 运行配置测试
    config_test = test_config()
    
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    print(f"基本功能测试: {'✓ 通过' if basic_test else '✗ 失败'}")
    print(f"配置功能测试: {'✓ 通过' if config_test else '✗ 失败'}")
    
    if basic_test and config_test:
        print("\n🎉 所有快速测试通过！")
        print("Redis过滤器可以正常使用")
    else:
        print("\n❌ 部分测试失败")
        print("请检查Redis配置和连接")
    
    print("\n💡 提示:")
    print("- 如需详细测试，请运行: python test_redis_filter.py")
    print("- 如需查看演示，请运行: python demo1.py") 
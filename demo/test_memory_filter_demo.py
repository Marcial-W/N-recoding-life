# -*- coding: utf-8 -*-
# @Time : 2025/8/23 18:39
# @Author : Marcial
# @Project: data_process
# @File : test_memory_filter_demo.py
# @Software: PyCharm

from data_filter import MemoryFilter

def main():

    filter = MemoryFilter()

    data = ['111', '222', '111', '222', 'hello', 'world', 'python', 'is', 'awesome']

    print("开始处理数据...")
    saved_count = 0
    existing_count = 0
    
    for i in data:
        if filter.is_exist(i):
            print(f"'{i}' 已存在")
            existing_count += 1
        else:
            filter.save_data(i)
            print(f"'{i}' 保存成功")
            saved_count += 1

    print(f"\n处理完成！")
    print(f"新增数据: {saved_count} 条")
    print(f"重复数据: {existing_count} 条")
    
    # 获取统计信息
    stats = filter.get_stats()
    print(f"\n内存过滤器统计信息: {stats}")

if __name__ == "__main__":
    main()


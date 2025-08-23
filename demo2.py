# -*- coding: utf-8 -*-
# @Time : 2025/8/23 18:39
# @Author : Marcial
# @Project: data_process
# @File : demo2.py
# @Software: PyCharm

from data_filter.memory_filter import MemoryFilter

def main():

    filter = MemoryFilter()

    data = ['111', '222', '111', '222', 'hello', 'world', 'python', 'is', 'awesome']

    print("开始处理数据...")
    for i in data:
        if filter.is_exist(i):
            print(f"'{i}' 已存在")
        else:
            filter.save_data(i)
            print(f"'{i}' 保存成功")

    print("\n处理完成！")

if __name__ == "__main__":
    main()


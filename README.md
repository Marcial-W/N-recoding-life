# 数据去重过滤器项目

这是一个基于Python的数据去重处理项目，支持多种存储方式实现数据过滤和去重功能。

## 功能特性

- **多种存储方式**：支持内存、Redis、MySQL三种存储方式
- **连接池优化**：MySQL和Redis都使用连接池，提高性能
- **配置管理**：统一的配置文件管理，支持环境变量
- **异常处理**：完善的错误处理和日志记录
- **统计信息**：提供数据统计和性能监控
- **向后兼容**：保持原有API的兼容性

## 项目结构

```
data_process/
├── data_filter/           # 核心过滤器模块
│   ├── __init__.py       # 基础过滤器类
│   ├── memory_filter.py  # 内存过滤器
│   ├── redis_filter.py   # Redis过滤器
│   └── mysql_filter.py   # MySQL过滤器
├── config.py             # 配置文件
├── demo1.py              # Redis过滤器演示
├── demo2.py              # 内存过滤器演示
├── demo3.py              # MySQL过滤器演示
├── test_redis_connection.py  # Redis连接测试
├── test_mysql_filter.py      # MySQL过滤器测试
├── env_example.txt       # 环境变量配置示例
└── docker_config/        # Docker配置
    ├── docker-compose.yaml
    ├── Dockerfile
    └── mysql_data/
```

## 安装依赖

```bash
pip install redis sqlalchemy pymysql
```

## 配置说明

### 1. 环境变量配置

复制 `env_example.txt` 为 `.env` 文件，并根据需要修改配置：

```bash
# MySQL配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_DATABASE=data1

# Redis配置
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0
```

### 2. 代码中使用配置

```python
from config import config

# 获取MySQL连接URL
mysql_url = config.get_mysql_url()

# 获取Redis配置
redis_config = config.get_redis_config()

# 打印当前配置
config.print_config()
```

## 使用方法

### 1. 内存过滤器（适合小数据量）

```python
from data_filter.memory_filter import MemoryFilter

filter = MemoryFilter()
data = ['111', '222', '111', '333']

for item in data:
    if filter.is_exist(item):
        print(f"'{item}' 已存在")
    else:
        filter.save_data(item)
        print(f"'{item}' 保存成功")
```

### 2. Redis过滤器（适合分布式环境）

```python
from data_filter.redis_filter import RedisFilter

# 使用配置文件
filter = RedisFilter()

# 或自定义配置
filter = RedisFilter(
    redis_host='127.0.0.1',
    redis_port=6379,
    redis_db=0,
    redis_key='my_filter'
)

data = ['111', '222', '111', '333']

for item in data:
    if filter.is_exist(item):
        print(f"'{item}' 已存在")
    else:
        result = filter.save_data(item)
        if result == 1:
            print(f"'{item}' 保存成功")

# 获取统计信息
stats = filter.get_stats()
print(f"统计信息: {stats}")

# 关闭连接
filter.close_connection()
```

### 3. MySQL过滤器（适合大数据量）

```python
from data_filter.mysql_filter import MySQLFilter

# 使用配置文件
filter = MySQLFilter()

# 或自定义配置
filter = MySQLFilter('mysql+pymysql://user:pass@host:port/db')

data = ['111', '222', '111', '333']

for item in data:
    if filter.is_exist(item):
        print(f"'{item}' 已存在")
    else:
        result = filter.save_data(item)
        if result == 1:
            print(f"'{item}' 保存成功")

# 获取统计信息
stats = filter.get_stats()
print(f"统计信息: {stats}")

# 关闭连接
MySQLFilter.close_connections()
```

## Docker部署

### 启动MySQL容器

```bash
cd docker_config
docker-compose up -d
```

### 环境变量配置

在Docker环境中，可以通过环境变量配置：

```bash
export MYSQL_HOST=mysql8
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=123456
export MYSQL_DATABASE=data1
```

## 测试

### Redis测试

```bash
python test_redis_connection.py
```

### MySQL测试

```bash
python test_mysql_filter.py
```

### 演示程序

```bash
# Redis演示
python demo1.py

# 内存演示
python demo2.py

# MySQL演示
python demo3.py
```

## 性能优化

### MySQL连接池配置

```python
# 在config.py中调整连接池参数
MYSQL_POOL_SIZE = 10          # 连接池大小
MYSQL_MAX_OVERFLOW = 20       # 最大溢出连接数
MYSQL_POOL_TIMEOUT = 30       # 连接超时时间
MYSQL_POOL_RECYCLE = 3600     # 连接回收时间
```

### Redis连接池配置

Redis连接池在代码中已优化，支持：
- 连接复用
- 超时重试
- 自动解码响应

## 新增功能

### 1. 统计信息

所有过滤器都支持获取统计信息：

```python
stats = filter.get_stats()
print(f"总记录数: {stats['total_records']}")
```

### 2. 数据清理

```python
# 清空所有数据（谨慎使用）
success = filter.clear_all()
```

### 3. 连接管理

```python
# 关闭连接
filter.close_connection()  # Redis
MySQLFilter.close_connections()  # MySQL
```

## 注意事项

1. **数据安全**：`clear_all()` 方法会清空所有数据，请谨慎使用
2. **连接管理**：程序结束时记得关闭数据库连接
3. **并发安全**：MySQL过滤器已处理并发冲突
4. **性能考虑**：大数据量建议使用MySQL，小数据量使用内存过滤器
5. **配置优先级**：代码参数 > 环境变量 > 默认配置

## 故障排除

### MySQL连接问题

1. 检查MySQL服务是否启动
2. 验证连接参数是否正确
3. 确认数据库和表是否存在
4. 检查用户权限

### Redis连接问题

1. 检查Redis服务是否启动
2. 验证端口是否正确
3. 确认防火墙设置
4. 检查Redis配置

### 性能问题

1. 调整连接池大小
2. 检查数据库索引
3. 监控连接数使用情况
4. 考虑使用批量操作

## 更新日志

### v2.0.0
- 添加配置文件管理
- 优化MySQL连接池
- 增强异常处理
- 添加统计功能
- 支持环境变量配置

### v1.0.0
- 基础过滤器功能
- 支持内存、Redis、MySQL存储
- 基本去重功能 # h

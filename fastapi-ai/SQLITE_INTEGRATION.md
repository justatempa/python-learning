# SQLite3 集成说明

本项目已集成 SQLite3 数据库支持，采用流行的实现方式，包括配置管理、连接池、数据访问层和API接口。

## 目录结构

```
project/
├── config/
│   └── config.py          # 配置文件，包含SQLite路径配置
├── database/
│   ├── __init__.py
│   └── manager.py         # 数据库连接管理器
│   └── repositories/
│       └── nav_table.py   # 数据访问层
├── schemas/
│   └── nav_table.py       # 数据模型定义
├── router/
│   └── nav_table.py       # API路由
├── scripts/
│   ├── init_db.py         # 数据库初始化脚本
│   └── test_nav.py        # 测试脚本
└── .env                   # 环境变量配置
```

## 配置说明

### .env 文件配置

```env
# SQLite3配置
SQLITE_DB_PATH=./data/nav.db
```

### config/config.py 配置

```python
# SQLite3数据库配置
SQLITE_DB_PATH: str = "./data/nav.db"
```

## 数据库初始化

### 自动初始化
项目启动时会自动初始化数据库和表结构：

```python
# 在 main.py 中
from database.manager import init_database

# 初始化数据库
init_database()
```

### 手动初始化
也可以通过脚本手动初始化：

```bash
python scripts/init_db.py
```

## API接口

### 导航表API (/api/nav)

- `POST /` - 创建导航记录
- `GET /` - 获取所有导航记录
- `GET /{nav_id}` - 根据ID获取导航记录
- `PUT /{nav_id}` - 更新导航记录
- `DELETE /{nav_id}` - 删除导航记录
- `GET /search/` - 搜索导航记录

### 请求示例

#### 创建导航记录
```bash
curl -X POST "http://localhost:8010/api/nav/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "示例网站",
    "url": "https://example.com",
    "desc": "这是一个示例网站",
    "sort": 1,
    "hide": false,
    "tags": "example,test"
  }'
```

#### 获取所有记录
```bash
curl -X GET "http://localhost:8010/api/nav/"
```

#### 搜索记录
```bash
curl -X GET "http://localhost:8010/api/nav/search/?keyword=示例"
```

## 数据模型

### NavTableCreate (创建)
```python
{
  "name": "网站名称",      # 必需
  "url": "网站URL",        # 必需
  "logo": "logo地址",      # 可选，默认使用默认图标
  "catelog": "分类",       # 可选，默认"2"
  "desc": "描述",          # 可选
  "sort": 1,              # 可选，排序
  "hide": false,          # 可选，是否隐藏
  "tags": "标签"           # 可选
}
```

### NavTableResponse (响应)
```python
{
  "id": 1,                # 自增ID
  "name": "网站名称",
  "url": "网站URL", 
  "logo": "logo地址",
  "catelog": "分类",
  "desc": "描述",
  "sort": 1,
  "hide": false,
  "tags": "标签"
}
```

## 数据库管理器特性

### 连接池管理
- 使用上下文管理器确保连接正确释放
- 支持多线程访问
- 30秒连接超时

### 错误处理
- 完整的异常捕获和日志记录
- 事务回滚机制

### 查询方法
- `execute_query()` - 执行单个查询
- `execute_many()` - 批量执行
- `fetch_one()` - 获取单条记录
- `fetch_all()` - 获取所有记录

## 测试

运行测试脚本验证功能：

```bash
python scripts/test_nav.py
```

## 表结构

```sql
CREATE TABLE "nav_table" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "name" TEXT,
  "url" TEXT,
  "logo" TEXT DEFAULT "https://nav.911250.xyz/favicon.ico",
  "catelog" TEXT DEFAULT "2",
  "desc" TEXT,
  "sort" INTEGER,
  "hide" BOOLEAN,
  "tags" TEXT DEFAULT ''
)
```

## 最佳实践

1. **配置管理**: 使用.env文件和Pydantic Settings进行配置管理
2. **连接管理**: 使用上下文管理器确保连接正确释放
3. **数据验证**: 使用Pydantic模型进行数据验证
4. **错误处理**: 完整的异常处理和日志记录
5. **API设计**: RESTful API设计，完整的CRUD操作
6. **测试**: 提供完整的测试脚本

## 扩展性

如需添加新表，可参考以下步骤：

1. 在`schemas/`目录下创建数据模型
2. 在`database/repositories/`目录下创建数据访问层
3. 在`router/`目录下创建API路由
4. 在`main.py`中注册路由

这种设计模式具有良好的扩展性和维护性。
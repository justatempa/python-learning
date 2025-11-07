# 项目概述

这是一个基于 Python 和 FastAPI 框架构建的 Web API 项目。它提供了一个结构化的起点，包含路由、配置、依赖项管理、响应处理和异常处理等功能。项目旨在快速搭建 RESTful API 服务。

## 主要技术栈

- **Python**: 项目的主要编程语言。
- **FastAPI**: 用于构建 API 的现代、快速（高性能）的 Web 框架。
- **Uvicorn**: 用于运行 FastAPI 应用的 ASGI 服务器。
- **Pydantic**: 用于数据验证和设置管理。
- **Pydantic-settings**: 用于从环境变量和配置文件中加载设置。

## 项目架构

项目遵循模块化设计，主要目录和文件如下：

- `main.py`: 项目入口文件，负责创建和启动 FastAPI 应用实例。
- `requirements.txt`: 项目依赖列表。
- `config/`: 存放项目配置，如数据库连接、密钥等。
- `router/`: 存放路由定义和路由注册逻辑。
- `api/`: 存放具体的 API 路由实现。
- `common/`: 存放通用工具和依赖项，如日志记录、权限验证等。
- `schemas/`: 存放数据模型（Pydantic models），用于请求和响应数据的验证和序列化。
- `models/`: （当前为空）通常用于存放数据库模型。
- `logs/`: 存放日志文件。

# 构建和运行

## 安装依赖

在项目根目录下运行以下命令安装所需依赖：

```bash
pip install -r requirements.txt
```

## 启动项目

项目提供了多种启动方式，适用于开发和生产环境：

### 开发环境（热重载）

推荐使用以下命令启动，它会在代码更改时自动重新加载应用：

```bash
uvicorn main:app --host=127.0.0.1 --port=8010 --reload
```

### 生产环境

#### 使用 Uvicorn 启动（多进程）

```bash
uvicorn main:app --host=127.0.0.1 --port=8010 --workers=4
```

#### 使用 Gunicorn 启动

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8020
```

## 测试

项目未包含显式的测试命令或测试框架配置。建议根据实际需求添加测试框架（如 `pytest`）并编写测试用例。

# 开发约定

## 代码风格

项目没有明确指定代码风格指南，但建议遵循 PEP 8 规范。

## 路由管理

- 路由在 `router/` 目录下进行管理。
- 使用 `APIRouter` 来组织不同的路由分组。
- 在 `router/server.py` 中注册所有路由。

## 配置管理

- 配置信息存放在 `config/config.py` 文件中。
- 使用 `pydantic-settings` 来管理配置，可以从环境变量中读取配置项。

## 依赖注入

- 依赖项存放在 `common/deps.py` 文件中。
- 使用 FastAPI 的 `Depends` 来注入依赖项。

## 异常处理

- 全局异常处理在 `router/server.py` 中注册。
- 自定义异常类存放在 `common/deps.py` 文件中。

## 响应格式

- 响应格式在 `schemas/response/resp.py` 文件中定义。
- 使用统一的响应结构，包含状态码、消息和数据。
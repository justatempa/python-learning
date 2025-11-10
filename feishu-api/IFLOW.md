# iFlow 上下文信息 (IFLOW.md)

## 项目概述

这是一个使用 Python 编写的脚本项目，旨在与飞书（Lark）的多维表格（Bitable）API 进行交互。项目提供了查询、创建、更新和删除多维表格记录的功能，并支持批量操作以提高效率。

该项目依赖于 `lark-oapi` Python SDK 来简化与飞书 API 的通信，并实现了自定义的认证、API客户端和频率控制机制。

## 核心组件

*   **`main.py`**: 项目的主要入口脚本，用于查询多维表格中的记录。
    *   从环境变量加载配置信息
    *   使用自定义的 `BitableAPI` 客户端查询记录
    *   使用 `parse_return_to_text` 函数格式化输出结果
*   **`api/bitable.py`**: 多维表格API模块，提供飞书多维表格的字段和记录操作功能。
    *   实现了字段列表、创建字段等功能
    *   实现了记录搜索、获取所有记录、批量创建、更新和删除记录等功能
*   **`api/auth.py`**: 飞书认证模块，负责获取和管理飞书访问令牌。
    *   实现了租户访问令牌的获取和缓存机制
    *   提供了认证头的生成方法
*   **`api/base.py`**: 基础网络层模块，提供HTTP请求重试机制和频率限制功能。
    *   实现了 `RateLimiter` 频率限制器
    *   实现了 `RetryableAPIClient` 可重试的API客户端
*   **`parse_return.py`**: 工具模块，用于将JSON数据解析为可读的文本格式。
    *   提供了 `parse_return_to_text` 函数，将记录数据转换为易读的文本
*   **`.env`**: 用于存储敏感配置信息的环境变量文件，避免将密钥硬编码在代码中。
    *   `app_token`: 飞书应用的访问令牌
    *   `table_id`: 要操作的多维表格的 ID
    *   `user_access_token`: 用户访问令牌，用于身份验证
    *   `view_id`: 视图 ID
    *   `app_id`: 飞书应用ID
    *   `app_secret`: 飞书应用密钥

## 运行项目

1.  **安装依赖**: 确保已安装 `lark-oapi` 和 `python-dotenv` 库。如果未安装，可以通过以下命令安装：
    ```bash
    pip install lark-oapi python-dotenv
    ```
2.  **配置环境变量**: 确保 `.env` 文件中包含正确的配置信息。
3.  **执行脚本**: 在项目根目录下运行以下命令：
    ```bash
    python main.py
    ```
    脚本将连接到飞书 API，根据 `main.py` 中定义的条件查询记录，并将结果打印到控制台。

## 开发约定

*   **依赖管理**: 项目依赖通过 `pip` 管理。主要依赖 `lark-oapi` 和 `python-dotenv`。
*   **配置管理**: 敏感信息（如 Token）存储在 `.env` 文件中，不应提交到版本控制系统。
*   **日志**: 使用 Python 内置的日志记录功能。
*   **代码结构**: 代码按照功能模块化组织，API 相关功能放在 `api` 目录下。
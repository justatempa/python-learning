# iFlow 上下文信息 (IFLOW.md)

## 项目概述

这是一个使用 Python 编写的简单脚本项目，旨在与飞书（Lark）的多维表格（Bitable）API 进行交互。其主要功能是查询指定应用表格中的记录，特别是筛选出“是否已完成”字段为“false”的待办事项。

该项目依赖于 `lark-oapi` Python SDK 来简化与飞书 API 的通信。

## 核心组件

*   **`main.py`**: 项目的核心脚本，包含了与飞书 API 交互的逻辑。
    *   使用 `lark-oapi` SDK 创建客户端。
    *   构造一个 `SearchAppTableRecordRequest` 请求，指定应用 Token、表格 ID、视图 ID，并定义查询字段和筛选条件（`是否已完成` 为 `false`）。
    *   使用用户访问令牌（User Access Token）发起请求。
    *   处理响应，打印成功结果或记录错误日志。
*   **`.env`**: 用于存储敏感配置信息的环境变量文件，避免将密钥硬编码在代码中。
    *   `app_token`: 飞书应用的访问令牌。
    *   `table_id`: 要查询的多维表格的 ID。
    *   `user_access_token`: 用户访问令牌，用于身份验证。

## 运行项目

1.  **安装依赖**: 确保已安装 `lark-oapi` 库。如果未安装，可以通过以下命令安装：
    ```bash
    pip install lark-oapi
    ```
2.  **配置环境变量**: 确保 `.env` 文件中包含正确的 `app_token`、`table_id` 和 `user_access_token`。
3.  **执行脚本**: 在项目根目录下运行以下命令：
    ```bash
    python main.py
    ```
    脚本将连接到飞书 API，根据 `main.py` 中定义的条件查询记录，并将结果打印到控制台。

## 开发约定

*   **依赖管理**: 项目依赖通过 `pip` 管理。目前主要依赖 `lark-oapi`。
*   **配置管理**: 敏感信息（如 Token）存储在 `.env` 文件中，不应提交到版本控制系统。
*   **日志**: 使用 `lark` SDK 内置的日志记录功能。
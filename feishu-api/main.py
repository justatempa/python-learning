import json

import os

import logging

import lark_oapi as lark

from lark_oapi.api.bitable.v1 import *

from dotenv import load_dotenv

import api

from parse_return import parse_return_to_text
# SDK 使用说明: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development

# 以下示例代码默认根据文档示例值填充，如果存在代码问题，请在 API 调试台填上相关必要参数后再复制代码使用
def setup_logger():
    """设置基础日志器"""
    logger = logging.getLogger()
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
def main():
    logger = setup_logger()
    # 加载 .env 文件中的环境变量
    load_dotenv()

    # 从环境变量加载配置
    app_token = os.getenv("app_token")
    table_id = os.getenv("table_id")
    user_access_token = os.getenv("user_access_token")
    view_id = os.getenv("view_id")
    app_id = os.getenv("app_id")
    app_secret = os.getenv("app_secret")

    
    # 检查必要配置是否存在
    if not all([app_token, table_id, user_access_token, view_id]):
        lark.logger.error("Missing required environment variables. Please check your .env file.")
        return

    fields  = ["待办事项", "截止日期", "是否已完成", "距离截止日", "优先级","标签", "创建时间"]

    
    auth = api.FeishuAuth(app_id, app_secret)
    api_client = api.RetryableAPIClient(
            max_retries=1,
            rate_limiter=api.RateLimiter(),
        )
    bitable_api = api.BitableAPI(auth, api_client)
    paramJson = {
        "field_names": ["待办事项", "截止日期", "是否已完成", "距离截止日", "优先级","标签", "创建时间"],
        "sort": [
    {
      "field_name": "创建时间",
      "desc": True
    }
  ],
  "filter": {
    "conjunction": "and",
    "conditions": [
      {
        "field_name": "是否已完成",
        "operator": "is",
        "value": [
          "false"
        ]
      }
    ]
  },
    }
    data,next_page_token = bitable_api.search_records(app_token, table_id, data=paramJson)

    text = parse_return_to_text(data, fields)
    print(text)

if __name__ == "__main__":
    main()
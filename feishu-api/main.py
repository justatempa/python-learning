import json

import os



import lark_oapi as lark

from lark_oapi.api.bitable.v1 import *

from dotenv import load_dotenv

from parse_return import parse_return_to_text
# SDK 使用说明: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development

# 以下示例代码默认根据文档示例值填充，如果存在代码问题，请在 API 调试台填上相关必要参数后再复制代码使用

def main():
    # 加载 .env 文件中的环境变量
    load_dotenv()

    # 从环境变量加载配置
    app_token = os.getenv("app_token")
    table_id = os.getenv("table_id")
    user_access_token = os.getenv("user_access_token")
    view_id = os.getenv("view_id")

    
    # 检查必要配置是否存在
    if not all([app_token, table_id, user_access_token, view_id]):
        lark.logger.error("Missing required environment variables. Please check your .env file.")
        return

    # 创建client
    # 使用 user_access_token 需开启 token 配置, 并在 request_option 中配置 token
    client = lark.Client.builder().enable_set_token(True).log_level(lark.LogLevel.DEBUG).build()

    fields  = ["待办事项", "截止日期", "是否已完成", "距离截止日", "优先级","标签", "创建时间"]
    # 构造请求对象
    request: SearchAppTableRecordRequest = SearchAppTableRecordRequest.builder() \
        .app_token(app_token) \
        .table_id(table_id) \
        .page_size(20) \
        .request_body(SearchAppTableRecordRequestBody.builder()
            .view_id(view_id)
            .field_names(fields)
            .filter(FilterInfo.builder()
                .conjunction("and")
                .conditions([Condition.builder()
                    .field_name("是否已完成")
                    .operator("is")
                    .value(["false"])
                    .build()
                    ])
                .build())
            .automatic_fields(False)
            .build()) \
        .build()

    # 发起请求

    option = lark.RequestOption.builder().user_access_token(user_access_token).build()

    response: SearchAppTableRecordResponse = client.bitable.v1.app_table_record.search(request, option)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.bitable.v1.app_table_record.search failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    items = lark.JSON.marshal(response.data, indent=4)
    text = parse_return_to_text(items, fields)
    print(text)


if __name__ == "__main__":
    main()
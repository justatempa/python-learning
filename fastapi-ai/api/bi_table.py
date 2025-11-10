from typing import Any

from fastapi import APIRouter, Depends

from schemas.response import resp
from common import logger
from config.config import  settings, get_bitable_api
from api.parse_return import parse_return_to_text
from models.bitable import RowAddRequest
import datetime
router = APIRouter()

@router.get("/table/list", summary="table list", name="查询表格列表", description="此API没有验证权限")
def table_list(
) -> Any:
    """
    获取用户信息 这个路由分组没有验证权限
    :param current_user:
    :return:
    """
    fields  = ["待办事项", "截止日期", "是否已完成", "距离截止日", "优先级","标签", "创建时间"]

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
    data,next_page_token = get_bitable_api().search_records(settings.APP_TOKEN, settings.TABLE_ID, data=paramJson)

    text = parse_return_to_text(data, fields)
    return resp.ok(data=text)

@router.post("/table/row/add", summary="table row add", name="添加行", description="此API没有验证权限")
def add_row(row_data: RowAddRequest) -> Any:
    """
    获取用户信息 这个路由分组没有验证权限
    :param current_user:
    :return:
    """
    fields  = ["待办事项", "截止日期", "是否已完成", "距离截止日", "优先级","标签", "创建时间"]
    # 日期是空 默认今天
    due_date = row_data.due_date
    if due_date == "":
        due_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    due_date = int(datetime.datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S").timestamp()) *1000
    paramJson =  [
        {"fields":{
                "待办事项": row_data.title,
                "截止日期": due_date,
                "优先级": get_priority_label(row_data.priority),
                "标签": row_data.tags.split("|"),
                "描述": row_data.desc
            }}
        
        ]
    

    data = get_bitable_api().batch_create_records(settings.APP_TOKEN, settings.TABLE_ID, records=paramJson)

    return resp.ok(data=data)
# 下面的枚举对应 1 2 3 4 写一个方法 入参是 1 2 3 4 返回对应的字符串。默认
# 🔵P0-重要且紧急  🟣P1-重要不紧急  🟠P2-紧急不重要 ⚪P3-不重要不紧急
def get_priority_label(priority: int) -> str:
    priority_map = {
        1: "🔵P0-重要且紧急",
        2: "🟣P1-重要不紧急",
        3: "🟠P2-紧急不重要",
        4: "⚪P3-不重要不紧急"
    }
    return priority_map.get(priority, "⚪P3-不重要不紧急")
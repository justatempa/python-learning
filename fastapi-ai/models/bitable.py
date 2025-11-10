from pydantic import BaseModel

# 1. 定义请求体 Pydantic 模型
class RowAddRequest(BaseModel):
    # 定义字段和类型，可以包含默认值
    title: str = "测试待办事项"
    due_date: str = ""
    desc: str = "通过API添加的待办事项"
    # 注意：如果 tags 预期是列表而不是管道分隔的字符串，最好定义为 list[str]
    tags: str = "测试标签|测试标签2" 
    priority: int = 4
    
    # 可以在这里添加配置，例如提供一个 JSON 示例
    class Config:
        schema_extra = {
            "example": {
                "title": "新创建的待办",
                "due_date": "2023-12-31",
                "desc": "这是一个示例描述。",
                "tags": "紧急|项目A",
                "priority": 1
            }
        }

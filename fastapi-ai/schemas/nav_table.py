from pydantic import BaseModel, Field
from datetime import datetime


class NavTableBase(BaseModel):
    """导航表基础模型"""
    name: str | None = Field(None, description="网站名称")
    url: str | None = Field(None, description="网站URL")
    logo: str | None = Field("https://nav.911250.xyz/favicon.ico", description="网站logo")
    catelog: str | None = Field("2", description="分类")
    desc: str | None = Field(None, description="网站描述")
    sort: int | None = Field(None, description="排序")
    hide: bool | None = Field(None, description="是否隐藏")
    tags: str | None = Field("", description="标签")


class NavTableCreate(NavTableBase):
    """创建导航记录的模型"""
    url: str | None = Field(..., min_length=1, description="网站URL")


class NavTableUpdate(NavTableBase):
    """更新导航记录的模型"""
    name: str | None = Field(None, min_length=1, description="网站名称")
    url: str | None = Field(None, min_length=1, description="网站URL")


class NavTableInDB(NavTableBase):
    """数据库中的导航记录模型"""
    id: int = Field(..., description="记录ID")


class NavTableResponse(NavTableInDB):
    """API响应的导航记录模型"""
    pass

# Pydantic v2 配置
NavTableInDB.model_config["from_attributes"] = True
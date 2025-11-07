import os

from typing import Union, Optional

from pydantic import AnyHttpUrl, IPvAnyAddress
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 开发模式配置
    DEBUG: bool = True
    # 项目文档
    TITLE: str = "FastAPI"
    DESCRIPTION: str = ""
    # 文档地址 默认为docs 生产环境关闭 None
    DOCS_URL: str = "/api/docs"
    # 文档关联请求数据接口
    OPENAPI_URL: str = "/api/openapi.json"
    # redoc 文档
    REDOC_URL: Optional[str] = "/api/redoc"

    # token过期时间 分钟
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # 生成token的加密算法
    ALGORITHM: str = "HS256"

    # 生产环境保管好 SECRET_KEY
    SECRET_KEY: str = 'xxxxxxxx'

    # 项目根路径
    BASE_PATH: str = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

    # 配置你的Mysql环境
    MYSQL_USERNAME: str = "runfast_go"
    MYSQL_PASSWORD: str = ""
    MYSQL_HOST: str = "mysql2.sqlpub.com"
    MYSQL_PORT: int = 3307
    MYSQL_DATABASE: str = 'runfast_go'
    
    print("init config success ")



settings = Settings()
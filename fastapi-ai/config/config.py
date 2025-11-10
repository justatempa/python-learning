import os

from typing import Union, Optional

from pydantic import AnyHttpUrl, IPvAnyAddress

from pydantic_settings import BaseSettings



# 惰性初始化的全局变量

_bitable_api = None



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

    

    # 飞书API配置

    APP_TOKEN: str = ""

    TABLE_ID: str = ""

    USER_ACCESS_TOKEN: str = ""

    APP_ID: str = ""

    APP_SECRET: str = ""

    VIEW_ID: str = ""

    TOKEN: str = "11111188"

    # 配置.env文件路径

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"  # 防止中文乱码（可选）
        # env_prefix = "MYAPP_"    # 如果 .env 中的变量有统一前缀（如 MYAPP_FEISHU_APP_ID
    

    print("init config success ")



def get_bitable_api():

    """获取全局的 BitableAPI 实例，如果不存在则初始化"""

    global _bitable_api

    if _bitable_api is None:

        # 延迟导入以避免循环依赖

        from feishu_api import auth as feishu_auth

        from feishu_api import base as feishu_base

        from feishu_api import bitable as feishu_bitable

        from dotenv import load_dotenv

        

        # 加载环境变量

        load_dotenv()

        # 使用配置中的APP_ID和APP_SECRET

        app_id = settings.APP_ID or os.getenv("app_id")

        app_secret = settings.APP_SECRET or os.getenv("app_secret")

        

        # 初始化认证和API客户端

        auth = feishu_auth.FeishuAuth(app_id, app_secret)

        api_client = feishu_base.RetryableAPIClient(

            max_retries=1,

            rate_limiter=feishu_base.RateLimiter(),

        )

        

        # 初始化 BitableAPI

        _bitable_api = feishu_bitable.BitableAPI(auth, api_client)

        print("BitableAPI initialized successfully")

    

    return _bitable_api



settings = Settings()
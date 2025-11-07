from typing import Any

from fastapi import APIRouter, Depends

from schemas.response import resp
from common import logger

router = APIRouter()

@router.get("/hello", summary="hello", name="hello", description="此API没有验证权限")
def hello(
) -> Any:
    """
    获取用户信息 这个路由分组没有验证权限
    :param current_user:
    :return:
    """
    logger.info("hello")
    return resp.ok(data="hello")
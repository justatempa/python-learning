#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/16 11:51
# @Author  : CoderCharm
# @File    : deps.py
# @Software: PyCharm
# @Github  : github/CoderCharm
# @Email   : wg_python@163.com
# @Desc    :
"""

一些通用的依赖功能

"""
from typing import Any, Union, Optional
#
from jose import jwt
from fastapi import Header, Depends, Request
from pydantic import ValidationError

from config.config import settings
from fastapi import Security, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

def check_jwt_token(
        token: Optional[str] = Header(..., description="登录token")
) -> Union[str, Any]:
    """
    解析验证token  默认验证headers里面为token字段的数据
    可以给 headers 里面token替换别名, 以下示例为 X-Token
    token: Optional[str] = Header(None, alias="X-Token")
    :param token:
    :return:
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpired()
    except (jwt.JWTError, ValidationError, AttributeError):
        raise TokenAuthError()

bearer_scheme = HTTPBearer()
def check_authority(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    if credentials.credentials != settings.TOKEN:
         raise TokenAuthError()

class TokenAuthError(Exception):
    def __init__(self, err_desc: str = "User Authentication Failed"):
        self.err_desc = err_desc


class TokenExpired(Exception):
    def __init__(self, err_desc: str = "Token has expired"):
        self.err_desc = err_desc


class AuthenticationError(Exception):
    def __init__(self, err_desc: str = "Permission denied"):
        self.err_desc = err_desc
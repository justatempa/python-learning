from fastapi import APIRouter, Request, Response
import json
import uuid
from typing import Any, Dict

jsonrpc_router = APIRouter()

# 存储已注册的方法
_methods = {}

def register_method(name: str, method):
    """注册一个JSON-RPC方法"""
    _methods[name] = method

async def handle_jsonrpc(request: Request) -> Response:
    """处理JSON-RPC请求"""
    try:
        body = await request.json()
    except json.JSONDecodeError:
        return _create_error_response(-32700, "Parse error", None)
    
    # 检查是否是批量请求
    is_batch = isinstance(body, list)
    
    if is_batch:
        responses = []
        for item in body:
            response = await _process_single_request(item)
            if response:
                responses.append(response)
        if responses:
            return Response(content=json.dumps(responses), media_type="application/json")
        else:
            # 如果所有请求都是通知，则返回204
            return Response(status_code=204)
    else:
        response = await _process_single_request(body)
        if response:
            return Response(content=json.dumps(response), media_type="application/json")
        else:
            # 单个通知请求
            return Response(status_code=204)

async def _process_single_request(req: Dict[str, Any]) -> Dict[str, Any] or None:
    """处理单个JSON-RPC请求"""
    # 验证JSON-RPC版本
    if req.get("jsonrpc") != "2.0":
        return _create_error_response(-32600, "Invalid Request", req.get("id"))
    
    method_name = req.get("method")
    if not method_name:
        return _create_error_response(-32600, "Invalid Request", req.get("id"))
    
    # 检查是否是通知(没有id)
    is_notification = "id" not in req
    
    # 获取方法
    method = _methods.get(method_name)
    if not method:
        return _create_error_response(-32601, "Method not found", req.get("id"))
    
    # 获取参数
    params = req.get("params", [])
    
    try:
        # 调用方法
        if isinstance(params, list):
            result = await method(*params) if hasattr(method, '__call__') else method
        elif isinstance(params, dict):
            result = await method(**params) if hasattr(method, '__call__') else method
        else:
            result = await method(params) if hasattr(method, '__call__') else method
            
        # 如果是通知，不返回结果
        if is_notification:
            return None
            
        # 返回成功响应
        return {
            "jsonrpc": "2.0",
            "result": result,
            "id": req.get("id")
        }
    except Exception as e:
        # 如果是通知，不返回错误
        if is_notification:
            return None
            
        return _create_error_response(-32603, str(e), req.get("id"))

def _create_error_response(code: int, message: str, id=None) -> Dict[str, Any]:
    """创建错误响应"""
    error_response = {
        "jsonrpc": "2.0",
        "error": {
            "code": code,
            "message": message
        },
        "id": id
    }
    
    # 移除id如果为None(通知)
    if id is None:
        del error_response["id"]
        
    return error_response

# 注册处理路由
@jsonrpc_router.post("")
async def jsonrpc_endpoint(request: Request):
    return await handle_jsonrpc(request)
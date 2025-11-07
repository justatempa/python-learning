from fastapi import FastAPI

from rpc.jsonrpc import register_method
from rpc.methods import hello_world

def init_rpc_methods(app: FastAPI):
    """初始化RPC方法"""
    register_method("hello_world", hello_world)
from fastapi import APIRouter
from .jsonrpc import jsonrpc_router

rpc_router = APIRouter()
rpc_router.include_router(jsonrpc_router, prefix="/jsonrpc")
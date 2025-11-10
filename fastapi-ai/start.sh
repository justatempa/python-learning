#!/bin/bash

# 项目启动脚本
# 用于在Linux环境下启动FastAPI项目

# 设置项目根目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd $PROJECT_DIR

# 检查虚拟环境
if [ -d "venv" ]; then
    echo "激活虚拟环境..."
    source venv/bin/activate
else
    echo "未找到虚拟环境，使用系统Python..."
fi

# 检查依赖
if [ ! -f "requirements.txt" ]; then
    echo "错误: 未找到 requirements.txt 文件"
    exit 1
fi

# 安装依赖函数
install_deps() {
    echo "检查并安装依赖..."
    pip install -r requirements.txt
}

# 开发环境启动
start_dev() {
    echo "启动开发环境 (带热重载)..."
    uvicorn main:app --host=127.0.0.1 --port=8010 --reload
}

# 生产环境启动 (Uvicorn 多进程)
start_prod_uvicorn() {
    echo "启动生产环境 (Uvicorn 多进程)..."
    uvicorn main:app --host=127.0.0.1 --port=8010 --workers=4
}

# 生产环境启动 (Gunicorn)
start_prod_gunicorn() {
    echo "启动生产环境 (Gunicorn)..."
    gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8020
}

# 显示帮助信息
show_help() {
    echo "用法: ./start.sh [选项]"
    echo "选项:"
    echo "  dev          启动开发环境 (带热重载)"
    echo "  prod         启动生产环境 (Uvicorn 多进程)"
    echo "  gunicorn     启动生产环境 (Gunicorn)"
    echo "  install      安装项目依赖"
    echo "  help         显示此帮助信息"
}

# 主程序逻辑
case "$1" in
    dev)
        install_deps
        start_dev
        ;;
    prod)
        install_deps
        start_prod_uvicorn
        ;;
    gunicorn)
        install_deps
        start_prod_gunicorn
        ;;
    install)
        install_deps
        ;;
    help|"")
        show_help
        ;;
    *)
        echo "未知选项: $1"
        show_help
        exit 1
        ;;
esac
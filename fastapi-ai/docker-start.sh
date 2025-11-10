#!/bin/bash

# Docker 启动脚本
# 用于构建和运行 FastAPI 项目的 Docker 容器

# 设置项目根目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd $PROJECT_DIR

# 显示帮助信息
show_help() {
    echo "用法: ./docker-start.sh [选项]"
    echo "选项:"
    echo "  build        构建 Docker 镜像"
    echo "  run          运行 Docker 容器"
    echo "  up           使用 docker-compose 启动服务"
    echo "  down         停止并移除 docker-compose 服务"
    echo "  logs         查看容器日志"
    echo "  clean        清理未使用的 Docker 资源"
    echo "  help         显示此帮助信息"
}

# 构建 Docker 镜像
build_image() {
    echo "正在构建 Docker 镜像..."
    docker build -t fastapi-app .
}

# 运行 Docker 容器
run_container() {
    echo "正在运行 Docker 容器..."
    # 检查容器是否已经在运行
    if [ $(docker ps -q -f name=fastapi-app) ]; then
        echo "容器已经在运行"
        return
    fi
    
    # 检查是否存在已停止的容器
    if [ $(docker ps -aq -f status=exited -f name=fastapi-app) ]; then
        echo "启动已存在的容器..."
        docker start fastapi-app
    else
        echo "创建并启动新容器..."
        docker run -d \
            --name fastapi-app \
            -p 8010:8010 \
            -v $(pwd)/logs:/app/logs \
            fastapi-app
    fi
}

# 使用 docker-compose 启动服务
start_compose() {
    echo "使用 docker-compose 启动服务..."
    docker-compose up -d
}

# 停止并移除 docker-compose 服务
stop_compose() {
    echo "停止并移除 docker-compose 服务..."
    docker-compose down
}

# 查看容器日志
view_logs() {
    echo "查看容器日志..."
    docker logs -f fastapi-app
}

# 清理未使用的 Docker 资源
clean_docker() {
    echo "清理未使用的 Docker 资源..."
    docker system prune -f
}

# 主程序逻辑
case "$1" in
    build)
        build_image
        ;;
    run)
        run_container
        ;;
    up)
        start_compose
        ;;
    down)
        stop_compose
        ;;
    logs)
        view_logs
        ;;
    clean)
        clean_docker
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
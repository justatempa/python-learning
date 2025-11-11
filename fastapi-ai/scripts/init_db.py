#!/usr/bin/env python3
"""
数据库初始化脚本
用于确保SQLite数据库和表结构正确创建
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.manager import init_database
from config.config import settings
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """主函数"""
    print("开始初始化数据库...")
    print(f"数据库文件路径: {settings.SQLITE_DB_PATH}")
    
    try:
        # 初始化数据库
        init_database()
        print("✅ 数据库初始化成功!")
        
        # 验证表是否存在
        from database.manager import get_db_manager
        db_manager = get_db_manager()
        
        # 检查表是否存在
        result = db_manager.fetch_one("SELECT name FROM sqlite_master WHERE type='table' AND name='nav_table';")
        if result:
            print("✅ nav_table表已存在")
            
            # 显示表结构
            columns = db_manager.fetch_all("PRAGMA table_info(nav_table);")
            print("表结构:")
            for column in columns:
                print(f"  - {column['name']}: {column['type']} (NOT NULL: {column['notnull']}, DEFAULT: {column['dflt_value']})")
        else:
            print("❌ nav_table表不存在")
            
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
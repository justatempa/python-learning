#!/usr/bin/env python3
"""
SQLite3集成验证脚本
快速验证SQLite3集成是否正常工作
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """主函数"""
    print("🔍 正在验证SQLite3集成...")
    
    try:
        # 1. 验证配置加载
        from config.config import settings
        print(f"✅ 配置加载成功: DB_PATH={settings.SQLITE_DB_PATH}")
        
        # 2. 验证数据库管理器
        from database.manager import get_db_manager, init_database
        db_manager = get_db_manager()
        print("✅ 数据库管理器初始化成功")
        
        # 3. 初始化数据库
        init_database()
        print("✅ 数据库初始化成功")
        
        # 4. 验证表存在
        result = db_manager.fetch_one("SELECT name FROM sqlite_master WHERE type='table' AND name='nav_table';")
        if result:
            print("✅ nav_table表存在")
        else:
            print("❌ nav_table表不存在")
            return False
            
        # 5. 验证仓库层
        from database.repositories.nav_table import NavTableRepository
        repo = NavTableRepository()
        print("✅ 数据访问层初始化成功")
        
        # 6. 验证API路由
        from router.nav_table import router
        print("✅ API路由加载成功")
        
        print("\n🎉 SQLite3集成验证成功!")
        print("\n可用的API接口:")
        print("- POST   /api/nav/           (创建导航记录)")
        print("- GET    /api/nav/           (获取所有记录)")
        print("- GET    /api/nav/{nav_id}   (根据ID查询)")
        print("- PUT    /api/nav/{nav_id}   (更新记录)")
        print("- DELETE /api/nav/{nav_id}   (删除记录)")
        print("- GET    /api/nav/search/    (搜索记录)")
        
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
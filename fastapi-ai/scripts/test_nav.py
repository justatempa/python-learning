#!/usr/bin/env python3
"""
SQLite3集成测试脚本
用于测试导航表的CRUD操作
"""

import sys
import os
import asyncio

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.nav_table import NavTableCreate, NavTableUpdate
from database.repositories.nav_table import NavTableRepository
from database.manager import get_db_manager

async def test_nav_operations():
    """测试导航表的CRUD操作"""
    print("开始测试导航表操作...")
    
    # 获取数据库管理器和仓库实例
    db_manager = get_db_manager()
    repo = NavTableRepository()
    
    # 测试1: 创建记录
    print("\n1. 测试创建记录...")
    nav_data = NavTableCreate(
        name="测试网站",
        url="https://example.com",
        desc="这是一个测试网站",
        sort=1,
        hide=False,
        tags="test,example"
    )
    
    try:
        created_nav = repo.create_nav(nav_data)
        print(f"✅ 创建成功: ID={created_nav.id}, Name={created_nav.name}")
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return
    
    # 测试2: 查询记录
    print("\n2. 测试查询记录...")
    try:
        # 通过ID查询
        nav_by_id = repo.get_nav_by_id(created_nav.id)
        if nav_by_id:
            print(f"✅ 通过ID查询成功: {nav_by_id.name}")
        
        # 通过URL查询
        nav_by_url = repo.get_nav_by_url("https://example.com")
        if nav_by_url:
            print(f"✅ 通过URL查询成功: {nav_by_url.name}")
        
        # 获取所有记录
        all_navs = repo.get_all_navs()
        print(f"✅ 获取所有记录成功: 共{len(all_navs)}条")
        
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return
    
    # 测试3: 更新记录
    print("\n3. 测试更新记录...")
    update_data = NavTableUpdate(
        name="更新后的测试网站",
        desc="这是更新后的测试网站",
        sort=2
    )
    
    try:
        updated_nav = repo.update_nav(created_nav.id, update_data)
        if updated_nav:
            print(f"✅ 更新成功: {updated_nav.name}")
        else:
            print("❌ 更新失败: 未找到记录")
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        return
    
    # 测试4: 搜索记录
    print("\n4. 测试搜索记录...")
    try:
        search_results = repo.search_navs("测试")
        print(f"✅ 搜索成功: 找到{len(search_results)}条记录")
        for nav in search_results:
            print(f"  - {nav.name}")
    except Exception as e:
        print(f"❌ 搜索失败: {e}")
        return
    
    # 测试5: 删除记录
    print("\n5. 测试删除记录...")
    try:
        success = repo.delete_nav(created_nav.id)
        if success:
            print("✅ 删除成功")
        else:
            print("❌ 删除失败: 未找到记录")
    except Exception as e:
        print(f"❌ 删除失败: {e}")
        return
    
    print("\n🎉 所有测试完成!")

if __name__ == "__main__":
    asyncio.run(test_nav_operations())
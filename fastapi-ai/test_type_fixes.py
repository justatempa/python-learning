#!/usr/bin/env python3
"""
类型检查修复验证脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def test_type_fixes():
    """测试类型修复"""
    print("🔍 正在验证类型修复...")
    
    try:
        # 测试导入
        from utils.website_info import get_website_info, WebsiteInfoExtractor
        print("✅ 模块导入成功")
        
        # 测试None安全的URL处理
        extractor = WebsiteInfoExtractor()
        
        # 测试None URL
        result1 = await extractor.extract_info(None)
        print(f"✅ None URL处理: {result1['name']}")
        
        # 测试空字符串URL
        result2 = await get_website_info("")
        print(f"✅ 空URL处理: {result2['name']}")
        
        # 测试有效URL
        result3 = await get_website_info("https://github.com")
        print(f"✅ 有效URL处理: {result3['name']}")
        
        print("🎉 所有类型修复验证成功!")
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_type_fixes())
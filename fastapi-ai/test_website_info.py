#!/usr/bin/env python3
"""
网站信息提取工具测试脚本
"""

import sys
import os
import asyncio

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.website_info import get_website_info

async def test_website_info():
    """测试网站信息提取"""
    print("🔍 正在测试网站信息提取工具...")
    
    # 测试URL列表
    test_urls = [
        "https://www.baidu.com",
        "https://www.zhihu.com"
    ]
    
    for url in test_urls:
        print(f"\n📝 提取 {url} 的信息:")
        try:
            info = await get_website_info(url)
            print(f"  ✅ 名称: {info['name']}")
            print(f"  ✅ 图标: {info['logo']}")
            print(f"  ✅ 描述: {info['description']}")
        except Exception as e:
            print(f"  ❌ 提取失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_website_info())
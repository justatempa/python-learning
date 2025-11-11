import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse
import re
from typing import Dict, Any
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

class WebsiteInfoExtractor:
    """网站信息提取工具"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def extract_info(self, url: str | None) -> Dict[str, Any]:
        """
        从URL提取网站信息
        
        Args:
            url: 网站URL
            
        Returns:
            包含name, logo, description的字典
        """
        if not url:
            return {
                'name': '',
                'logo': 'https://nav.911250.xyz/favicon.ico',
                'description': '',
                'url': ''
            }
            
        try:
            # 确保URL格式正确
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # 使用aiohttp异步获取网页内容
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status != 200:
                        raise Exception(f"HTTP {response.status}")
                    
                    content = await response.text()
                    
            # 解析HTML
            soup = BeautifulSoup(content, 'html.parser')
            
            # 提取网站信息
            result = {
                'name': self._extract_title(soup),
                'logo': await self._extract_favicon(session, url, soup),
                'description': self._extract_description(soup),
                'url': url
            }
            
            return result
            
        except Exception as e:
            logger.error(f"提取网站信息失败 {url}: {e}")
            # 返回默认值
            return {
                'name': self._extract_domain_name(url),
                'logo': 'https://nav.911250.xyz/favicon.ico',
                'description': '',
                'url': url
            }
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """提取网站标题"""
        # 优先级：og:title -> title -> h1 -> h2 -> h3
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            content = og_title['content']
            return str(content).strip() if content else ''
        
        title_tag = soup.find('title')
        if title_tag and title_tag.get_text():
            return title_tag.get_text().strip()
        
        h1 = soup.find('h1')
        if h1 and h1.get_text():
            return h1.get_text().strip()
        
        h2 = soup.find('h2')
        if h2 and h2.get_text():
            return h2.get_text().strip()
        
        h3 = soup.find('h3')
        if h3 and h3.get_text():
            return h3.get_text().strip()
        
        return ''
    
    async def _extract_favicon(self, session: aiohttp.ClientSession, base_url: str, soup: BeautifulSoup) -> str:
        """提取网站图标"""
        # 优先级：og:image -> link[rel="icon"] -> link[rel="shortcut icon"] -> /favicon.ico
        
        # 1. 检查og:image
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            content = og_image['content']
            favicon_url = str(content) if content else ''
            if self._is_valid_image_url(favicon_url):
                return favicon_url
        
        # 2. 检查各种icon标签
        icon_selectors = [
            'link[rel="icon"]',
            'link[rel="shortcut icon"]',
            'link[rel="apple-touch-icon"]',
            'link[rel="apple-touch-icon-precomposed"]'
        ]
        
        for selector in icon_selectors:
            icon_link = soup.select_one(selector)
            if icon_link and icon_link.get('href'):
                href = icon_link['href']
                favicon_url = urljoin(base_url, str(href) if href else '')
                if await self._is_valid_favicon(session, favicon_url):
                    return favicon_url
        
        # 3. 检查根目录favicon
        parsed_url = urlparse(base_url)
        root_favicon = f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"
        if await self._is_valid_favicon(session, root_favicon):
            return root_favicon
        
        return 'https://nav.911250.xyz/favicon.ico'
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """提取网站描述"""
        # 优先级：og:description -> meta[name="description"] -> meta[name="Description"]
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            content = og_desc['content']
            return str(content).strip() if content else ''
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            content = meta_desc['content']
            return str(content).strip() if content else ''
        
        meta_desc_case = soup.find('meta', attrs={'name': 'Description'})
        if meta_desc_case and meta_desc_case.get('content'):
            content = meta_desc_case['content']
            return str(content).strip() if content else ''
        
        return ''
    
    def _extract_domain_name(self, url: str | None) -> str:
        """从URL提取域名作为默认名称"""
        if not url:
            return ''
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            # 移除www前缀
            if domain and domain.startswith('www.'):
                domain = domain[4:]
            # 取主域名
            if domain:
                parts = domain.split('.')
                if len(parts) > 1:
                    return parts[0]
                return domain
            return ''
        except:
            return ''
    
    async def _is_valid_favicon(self, session: aiohttp.ClientSession, url: str | None) -> bool:
        """检查favicon URL是否有效"""
        if not url:
            return False
        try:
            async with session.head(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                return response.status == 200
        except:
            return False
    
    def _is_valid_image_url(self, url: str | None) -> bool:
        """检查是否为有效的图片URL"""
        if not url:
            return False
        
        # 检查文件扩展名
        image_extensions = ['.ico', '.png', '.jpg', '.jpeg', '.gif', '.svg']
        url_lower = url.lower()
        return any(url_lower.endswith(ext) for ext in image_extensions)


# 快速使用函数
async def get_website_info(url: str | None) -> Dict[str, Any]:
    """快速获取网站信息"""
    extractor = WebsiteInfoExtractor()
    return await extractor.extract_info(url)


# 使用示例
if __name__ == "__main__":
    async def main():
        # 测试示例
        test_urls = [
            "https://www.github.com",
            "https://stackoverflow.com",
            "https://nav.911250.xyz"
        ]
        
        extractor = WebsiteInfoExtractor()
        
        for url in test_urls:
            print(f"\n提取 {url} 的信息:")
            info = await extractor.extract_info(url)
            print(f"  名称: {info['name']}")
            print(f"  图标: {info['logo']}")
            print(f"  描述: {info['description']}")
    
    asyncio.run(main())
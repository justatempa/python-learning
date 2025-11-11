# 网站信息提取工具

这个工具可以从URL中自动提取网站的名称、图标和描述信息。

## 功能特性

- **异步处理**: 使用aiohttp进行异步HTTP请求
- **智能提取**: 支持多种元数据格式的优先级提取
- **错误处理**: 完善的异常处理和默认值回退
- **缓存友好**: 支持HEAD请求验证资源有效性

## 提取优先级

### 网站名称 (name)
1. `og:title` meta标签
2. `<title>`标签
3. `<h1>`标签
4. `<h2>`标签
5. `<h3>`标签
6. 从域名提取

### 网站图标 (logo)
1. `og:image` meta标签
2. `<link rel="icon">`
3. `<link rel="shortcut icon">`
4. `<link rel="apple-touch-icon">`
5. 根目录`/favicon.ico`
6. 默认图标

### 网站描述 (description)
1. `og:description` meta标签
2. `<meta name="description">`
3. `<meta name="Description">`

## 使用方法

### 基本使用

```python
from utils.website_info import get_website_info

# 异步调用
info = await get_website_info("https://example.com")
print(f"名称: {info['name']}")
print(f"图标: {info['logo']}")
print(f"描述: {info['description']}")
```

### 在API中使用

创建导航记录时会自动提取网站信息：

```bash
curl -X POST "http://localhost:8010/api/nav/" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://github.com",
    "catelog": "开发工具"
  }'
```

系统会自动提取GitHub的名称、图标和描述。

### 单独提取信息

```bash
curl -X POST "http://localhost:8010/api/nav/extract-info?url=https://github.com"
```

## API接口

### POST /api/nav/extract-info
从URL提取网站信息

**参数:**
- `url`: 网站URL

**响应:**
```json
{
  "id": 0,
  "name": "GitHub",
  "url": "https://github.com",
  "logo": "https://github.com/favicon.ico",
  "catelog": "2",
  "desc": "GitHub is where people build software.",
  "sort": 0,
  "hide": false,
  "tags": ""
}
```

## 依赖安装

```bash
pip install -r requirements_website.txt
```

包含的依赖：
- `beautifulsoup4`: HTML解析
- `aiohttp`: 异步HTTP客户端
- `requests`: HTTP客户端

## 错误处理

- 网络请求超时（10秒）
- HTTP错误状态码
- 无效的HTML内容
- 资源不存在

当提取失败时，会返回默认值：
- 名称: 从域名提取
- 图标: `https://nav.911250.xyz/favicon.ico`
- 描述: 空字符串

## 扩展性

可以轻松扩展支持更多元数据格式：
- Twitter Cards
- JSON-LD结构化数据
- 自定义CSS选择器
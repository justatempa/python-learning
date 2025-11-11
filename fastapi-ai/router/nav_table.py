from fastapi import APIRouter, Depends, HTTPException, status
from schemas.nav_table import NavTableCreate, NavTableUpdate, NavTableResponse
from database.repositories.nav_table import NavTableRepository
from utils.website_info import get_website_info

router = APIRouter(prefix="/api/nav", tags=["navigation"])


@router.post("/add", response_model=NavTableResponse, status_code=status.HTTP_201_CREATED)
async def create_nav(nav_data: NavTableCreate, repo: NavTableRepository = Depends()):
    """创建新的导航记录"""
    # 检查URL是否已存在
    url = nav_data.url
    if url is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL is required"
        )
    existing_nav = repo.get_nav_by_url(url)
    if existing_nav:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL already exists"
        )
    
    # 如果没有提供名称或描述，自动提取网站信息
    if not nav_data.name or not nav_data.desc:
        try:
            website_info = await get_website_info(url)  # 修复：使用确定的url变量
            if not nav_data.name:
                nav_data.name = website_info.get('name', '')
            if not nav_data.desc:
                nav_data.desc = website_info.get('description', '')
            if not nav_data.logo:
                nav_data.logo = website_info.get('logo', '')
        except Exception as e:
            # 如果提取失败，使用默认值
            pass
    
    return repo.create_nav(nav_data)


@router.get("/", response_model=list[NavTableResponse])
async def get_all_navs(
    skip: int = 0, 
    limit: int = 100, 
    repo: NavTableRepository = Depends()
):
    """获取所有导航记录"""
    return repo.get_all_navs(skip=skip, limit=limit)


@router.get("/{nav_id}", response_model=NavTableResponse)
async def get_nav_by_id(nav_id: int, repo: NavTableRepository = Depends()):
    """根据ID获取导航记录"""
    nav = repo.get_nav_by_id(nav_id)
    if not nav:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Navigation record not found"
        )
    return nav


@router.put("/{nav_id}", response_model=NavTableResponse)
async def update_nav(
    nav_id: int, 
    nav_data: NavTableUpdate, 
    repo: NavTableRepository = Depends()
):
    """更新导航记录"""
    existing_nav = repo.get_nav_by_id(nav_id)
    if not existing_nav:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Navigation record not found"
        )
    
    # 如果URL有变更，检查是否与其他记录冲突
    if nav_data.url and nav_data.url != existing_nav.url:
        existing_by_url = repo.get_nav_by_url(nav_data.url)
        if existing_by_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="URL already exists"
            )
    
    updated_nav = repo.update_nav(nav_id, nav_data)
    if not updated_nav:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed to update navigation record"
        )
    
    return updated_nav


@router.delete("/{nav_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_nav(nav_id: int, repo: NavTableRepository = Depends()):
    """删除导航记录"""
    success = repo.delete_nav(nav_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Navigation record not found"
        )
    return None


@router.get("/search/", response_model=list[NavTableResponse])
async def search_navs(
    keyword: str, 
    skip: int = 0, 
    limit: int = 100, 
    repo: NavTableRepository = Depends()
):
    """搜索导航记录"""
    if not keyword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search keyword is required"
        )
    
    return repo.search_navs(keyword, skip=skip, limit=limit)


@router.post("/extract-info", response_model=NavTableResponse)
async def extract_website_info(url: str, repo: NavTableRepository = Depends()):
    """从URL提取网站信息"""
    try:
        website_info = await get_website_info(url)
        return NavTableResponse(
            id=0,  # 临时ID，实际使用时会由数据库生成
            name=website_info.get('name', ''),
            url=url,
            logo=website_info.get('logo', 'https://nav.911250.xyz/favicon.ico'),
            catelog="2",
            desc=website_info.get('description', ''),
            sort=0,
            hide=False,
            tags=""
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to extract website info: {str(e)}"
        )
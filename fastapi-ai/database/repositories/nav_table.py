from typing import List, Optional
from database.manager import get_db_manager
from schemas.nav_table import NavTableCreate, NavTableUpdate, NavTableResponse


class NavTableRepository:
    """导航表数据访问层"""
    
    def __init__(self):
        self.db_manager = get_db_manager()
    
    def create_nav(self, nav_data: NavTableCreate) -> NavTableResponse:
        """创建新的导航记录"""
        insert_query = """
        INSERT INTO nav_table (name, url, logo, catelog, "desc", sort, hide, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            nav_data.name,
            nav_data.url,
            nav_data.logo,
            nav_data.catelog,
            nav_data.desc,
            nav_data.sort,
            nav_data.hide,
            nav_data.tags
        )
        
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(insert_query, params)
            conn.commit()
            
            # 获取刚插入的记录ID
            nav_id = cursor.lastrowid
            
            # 返回完整的记录
            return self.get_nav_by_id(nav_id)
    
    def get_nav_by_id(self, nav_id: int) -> Optional[NavTableResponse]:
        """根据ID获取导航记录"""
        query = "SELECT * FROM nav_table WHERE id = ?"
        result = self.db_manager.fetch_one(query, (nav_id,))
        
        if result:
            return NavTableResponse(**result)
        return None
    
    def get_nav_by_url(self, url: str) -> Optional[NavTableResponse]:
        """根据URL获取导航记录"""
        query = "SELECT * FROM nav_table WHERE url = ?"
        result = self.db_manager.fetch_one(query, (url,))
        
        if result:
            return NavTableResponse(**result)
        return None
    
    def get_all_navs(self, skip: int = 0, limit: int = 100) -> List[NavTableResponse]:
        """获取所有导航记录"""
        query = "SELECT * FROM nav_table ORDER BY sort ASC, id DESC LIMIT ? OFFSET ?"
        results = self.db_manager.fetch_all(query, (limit, skip))
        
        return [NavTableResponse(**result) for result in results]
    
    def update_nav(self, nav_id: int, nav_data: NavTableUpdate) -> Optional[NavTableResponse]:
        """更新导航记录"""
        # 构建动态更新语句
        update_fields = []
        params = []
        
        if nav_data.name is not None:
            update_fields.append("name = ?")
            params.append(nav_data.name)
        
        if nav_data.url is not None:
            update_fields.append("url = ?")
            params.append(nav_data.url)
        
        if nav_data.logo is not None:
            update_fields.append("logo = ?")
            params.append(nav_data.logo)
        
        if nav_data.catelog is not None:
            update_fields.append("catelog = ?")
            params.append(nav_data.catelog)
        
        if nav_data.desc is not None:
            update_fields.append('"desc" = ?')
            params.append(nav_data.desc)
        
        if nav_data.sort is not None:
            update_fields.append("sort = ?")
            params.append(nav_data.sort)
        
        if nav_data.hide is not None:
            update_fields.append("hide = ?")
            params.append(nav_data.hide)
        
        if nav_data.tags is not None:
            update_fields.append("tags = ?")
            params.append(nav_data.tags)
        
        if not update_fields:
            return self.get_nav_by_id(nav_id)
        
        query = f"UPDATE nav_table SET {', '.join(update_fields)} WHERE id = ?"
        params.append(nav_id)
        
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            
            return self.get_nav_by_id(nav_id)
    
    def delete_nav(self, nav_id: int) -> bool:
        """删除导航记录"""
        query = "DELETE FROM nav_table WHERE id = ?"
        
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (nav_id,))
            conn.commit()
            
            return cursor.rowcount > 0
    
    def search_navs(self, keyword: str, skip: int = 0, limit: int = 100) -> List[NavTableResponse]:
        """搜索导航记录"""
        query = """
        SELECT * FROM nav_table 
        WHERE name LIKE ? OR url LIKE ? OR tags LIKE ?
        ORDER BY sort ASC, id DESC 
        LIMIT ? OFFSET ?
        """
        search_term = f"%{keyword}%"
        params = (search_term, search_term, search_term, limit, skip)
        
        results = self.db_manager.fetch_all(query, params)
        return [NavTableResponse(**result) for result in results]
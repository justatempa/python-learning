import sqlite3
import os
import logging
from contextlib import contextmanager
from typing import Generator, Optional
from config.config import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """SQLite数据库管理器，使用连接池和上下文管理器"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_db_directory()
        
    def _ensure_db_directory(self):
        """确保数据库目录存在"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            logger.info(f"Created database directory: {db_dir}")
    
    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """获取数据库连接的上下文管理器"""
        conn = None
        try:
            conn = sqlite3.connect(
                self.db_path,
                check_same_thread=False,  # 允许多线程访问
                timeout=30.0  # 连接超时时间
            )
            conn.row_factory = sqlite3.Row  # 启用字典式访问
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> Optional[sqlite3.Cursor]:
        """执行查询语句"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor
    
    def execute_many(self, query: str, params_list: list) -> None:
        """批量执行查询"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[dict]:
        """获取单条记录"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def fetch_all(self, query: str, params: tuple = ()) -> list:
        """获取所有记录"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]


# 全局数据库管理器实例
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """获取全局数据库管理器实例"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager(settings.SQLITE_DB_PATH)
    return _db_manager


def init_database():
    """初始化数据库和表结构"""
    db_manager = get_db_manager()
    
    # 创建nav_table表
    create_table_query = """
    CREATE TABLE IF NOT EXISTS "nav_table" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "name" TEXT,
        "url" TEXT,
        "logo" TEXT DEFAULT 'https://nav.911250.xyz/favicon.ico',
        "catelog" TEXT DEFAULT '2',
        "desc" TEXT,
        "sort" INTEGER,
        "hide" BOOLEAN,
        "tags" TEXT DEFAULT ''
    )
    """
    
    try:
        db_manager.execute_query(create_table_query)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
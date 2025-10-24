"""
数据库操作助手类
"""
import sqlite3
import os
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta


class DatabaseHelper:
    """数据库操作助手"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.path.join(
            os.path.dirname(__file__), 
            "../../src/database/taobei.db"
        )
    
    def get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 使结果可以通过列名访问
        return conn
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """执行查询语句"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """执行更新语句"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    # 用户相关操作
    def create_test_user(self, phone_number: str, nickname: str = None) -> int:
        """创建测试用户"""
        query = """
        INSERT INTO users (phone_number, nickname, created_at, updated_at)
        VALUES (?, ?, datetime('now'), datetime('now'))
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (phone_number, nickname))
            conn.commit()
            return cursor.lastrowid
    
    def get_user_by_phone(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """根据手机号获取用户"""
        query = "SELECT * FROM users WHERE phone_number = ?"
        results = self.execute_query(query, (phone_number,))
        return results[0] if results else None
    
    def delete_user_by_phone(self, phone_number: str) -> int:
        """根据手机号删除用户"""
        query = "DELETE FROM users WHERE phone_number = ?"
        return self.execute_update(query, (phone_number,))
    
    def user_exists(self, phone_number: str) -> bool:
        """检查用户是否存在"""
        return self.get_user_by_phone(phone_number) is not None
    
    def create_user_if_not_exists(self, phone_number: str, nickname: str = None) -> int:
        """如果用户不存在则创建用户"""
        if not self.user_exists(phone_number):
            return self.create_test_user(phone_number, nickname or f"用户{phone_number[-4:]}")
        else:
            user = self.get_user_by_phone(phone_number)
            return user['id'] if user else None
    
    # 验证码相关操作
    def create_verification_code(self, phone_number: str, code: str, expires_in_seconds: int = 60) -> int:
        """创建验证码记录"""
        expires_at = datetime.now() + timedelta(seconds=expires_in_seconds)
        query = """
        INSERT INTO verification_codes (phone_number, code, expires_at, created_at)
        VALUES (?, ?, ?, datetime('now'))
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (phone_number, code, expires_at.isoformat()))
            conn.commit()
            return cursor.lastrowid
    
    def get_verification_code(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """获取最新的验证码"""
        query = """
        SELECT * FROM verification_codes 
        WHERE phone_number = ? 
        ORDER BY created_at DESC 
        LIMIT 1
        """
        results = self.execute_query(query, (phone_number,))
        return results[0] if results else None
    
    def delete_verification_codes(self, phone_number: str) -> int:
        """删除指定手机号的所有验证码"""
        query = "DELETE FROM verification_codes WHERE phone_number = ?"
        return self.execute_update(query, (phone_number,))
    
    def expire_verification_code(self, phone_number: str) -> int:
        """将指定手机号的验证码设置为过期"""
        query = """
        UPDATE verification_codes 
        SET expires_at = datetime('now', '-1 minute')
        WHERE phone_number = ? AND expires_at > datetime('now')
        """
        return self.execute_update(query, (phone_number,))
    
    def is_verification_code_valid(self, phone_number: str, code: str) -> bool:
        """验证验证码是否有效"""
        query = """
        SELECT * FROM verification_codes 
        WHERE phone_number = ? AND code = ? AND expires_at > datetime('now')
        ORDER BY created_at DESC 
        LIMIT 1
        """
        results = self.execute_query(query, (phone_number, code))
        return len(results) > 0
    
    # 测试数据清理
    def clean_test_data(self):
        """清理测试数据"""
        test_phones = [
            "13800138001",
            "13800138002", 
            "13800138003",
            "13800138004",
            "13800138005"
        ]
        
        # 删除测试用户
        for phone in test_phones:
            self.delete_user_by_phone(phone)
            self.delete_verification_codes(phone)
    
    def setup_test_data(self):
        """设置测试数据"""
        # 创建已注册的测试用户
        if not self.user_exists("13800138001"):
            self.create_test_user("13800138001", "测试用户1")
        
        # 确保未注册的测试手机号不存在
        self.delete_user_by_phone("13800138002")
    
    def get_table_count(self, table_name: str) -> int:
        """获取表中记录数量"""
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        result = self.execute_query(query)
        return result[0]['count'] if result else 0
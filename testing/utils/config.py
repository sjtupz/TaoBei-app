"""
测试配置管理
"""
import os
from typing import Optional


class Config:
    """测试配置类"""
    
    def __init__(self):
        # 基础配置
        self.BASE_URL = os.getenv("BASE_URL", "http://localhost:5173")
        self.API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000/api")
        
        # 浏览器配置
        self.HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
        self.SLOW_MO = int(os.getenv("SLOW_MO", "0"))
        self.TIMEOUT = int(os.getenv("TIMEOUT", "30000"))
        
        # 数据库配置
        self.DB_PATH = os.getenv("DB_PATH", "../src/database/taobei.db")
        
        # 测试数据配置
        self.TEST_PHONE_REGISTERED = "13800138001"
        self.TEST_PHONE_UNREGISTERED = "13800138002"
        self.TEST_VERIFICATION_CODE = "123456"
        self.INVALID_PHONE = "123"
        self.INVALID_VERIFICATION_CODE = "000000"
        
        # 等待时间配置
        self.SHORT_WAIT = 2000  # 2秒
        self.MEDIUM_WAIT = 5000  # 5秒
        self.LONG_WAIT = 10000  # 10秒
        
        # 重试配置
        self.MAX_RETRIES = 3
        self.RETRY_DELAY = 1000  # 1秒
    
    @property
    def login_url(self) -> str:
        """登录页面URL"""
        return f"{self.BASE_URL}/#login"
    
    @property
    def register_url(self) -> str:
        """注册页面URL"""
        return f"{self.BASE_URL}/#register"
    
    @property
    def home_url(self) -> str:
        """首页URL"""
        return self.BASE_URL
    
    def get_api_url(self, endpoint: str) -> str:
        """获取API完整URL"""
        return f"{self.API_BASE_URL}/{endpoint.lstrip('/')}"
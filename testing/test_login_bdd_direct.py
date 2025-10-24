"""
直接运行登录BDD测试
"""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入必要的模块
from utils.database_helper import DatabaseHelper
from utils.api_helper import APIHelper
from pages.login_page import LoginPage

# 加载登录功能的场景
scenarios('features/login.feature')

# 导入所有步骤定义
from features.steps.login_steps import *

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
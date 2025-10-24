"""BDD测试运行器"""
import pytest
from pytest_bdd import scenarios

# 导入所有步骤定义
from features.steps import login_steps
from features.steps import register_steps
from features.steps import user_management_steps
from features.steps import product_management_steps

# 加载所有feature文件的场景
scenarios('features/login.feature')
scenarios('features/register.feature')
scenarios('features/user_management.feature')
scenarios('features/product_management.feature')
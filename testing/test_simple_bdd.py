"""
简单的BDD测试
"""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# 导入场景
scenarios('features/simple_login.feature')

@given('我在登录页面')
def navigate_to_login():
    """导航到登录页面"""
    print("步骤：我在登录页面")
    pass

@when(parsers.parse('我输入手机号 "{phone}"'))
def enter_phone(phone):
    """输入手机号"""
    print(f"步骤：我输入手机号 {phone}")
    pass

@then('我应该看到登录页面')
def verify_login_page():
    """验证登录页面"""
    print("步骤：我应该看到登录页面")
    pass
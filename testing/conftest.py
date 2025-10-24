"""
pytest 全局配置和 fixture 定义
"""
import os
import pytest
from playwright.sync_api import sync_playwright
from utils.config import Config
from utils.database_helper import DatabaseHelper

# 导入所有步骤定义
from features.steps import login_steps, register_steps, user_management_steps, product_management_steps


@pytest.fixture(scope="session")
def config():
    """全局配置fixture"""
    return Config()


@pytest.fixture(scope="session")
def database_helper():
    """数据库操作助手fixture"""
    return DatabaseHelper()


@pytest.fixture(scope="session")
def playwright_instance():
    """Playwright实例fixture"""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance, config):
    """浏览器实例fixture"""
    browser = playwright_instance.chromium.launch(
        headless=config.HEADLESS,
        slow_mo=config.SLOW_MO
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser, config):
    """页面实例fixture"""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="zh-CN"
    )
    page = context.new_page()
    
    # 导航到应用首页
    page.goto(config.BASE_URL)
    
    yield page
    
    # 清理
    context.close()


@pytest.fixture(scope="function")
def clean_database(database_helper):
    """清理测试数据fixture"""
    yield
    # 测试后清理数据
    database_helper.clean_test_data()


def pytest_configure(config):
    """pytest配置钩子"""
    # 创建报告目录
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)


def pytest_collection_modifyitems(config, items):
    """修改测试项收集"""
    for item in items:
        # 为UI测试添加标记
        if "ui" in item.nodeid or "page" in item.fixturenames:
            item.add_marker(pytest.mark.ui)
        
        # 为API测试添加标记
        if "api" in item.nodeid or "requests" in str(item.function):
            item.add_marker(pytest.mark.api)


@pytest.fixture(autouse=True)
def setup_test_environment(config):
    """自动设置测试环境"""
    # 确保测试环境变量设置正确
    os.environ["TEST_ENV"] = "true"
    yield
    # 测试后清理环境变量
    if "TEST_ENV" in os.environ:
        del os.environ["TEST_ENV"]
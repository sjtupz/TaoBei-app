# -*- coding: utf-8 -*-
"""
Behave环境配置文件
设置测试环境和浏览器实例
"""
from playwright.sync_api import sync_playwright
from utils.database_helper import DatabaseHelper
from utils.api_helper import APIHelper


def before_all(context):
    """在所有测试开始前执行"""
    print("=== before_all 被调用 ===")
    # 启动Playwright
    context.playwright = sync_playwright().start()
    
    # 启动浏览器
    context.browser = context.playwright.chromium.launch(
        headless=False,  # 设置为False以便调试
        slow_mo=500      # 减慢操作速度以便观察
    )
    
    # 初始化数据库和API助手
    context.db_helper = DatabaseHelper()
    context.api_helper = APIHelper()
    
    print("测试环境初始化完成")


def before_scenario(context, scenario):
    """在每个场景开始前执行"""
    print("=== before_scenario 被调用 ===")
    # 创建新的浏览器上下文和页面
    context.browser_context = context.browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="zh-CN"
    )
    
    context.driver = context.browser_context.new_page()
    
    # 设置页面超时
    context.driver.set_default_timeout(30000)
    
    print(f"开始执行场景: {scenario.name}")
    print(f"浏览器已初始化: {hasattr(context, 'browser')}")
    print(f"浏览器上下文已初始化: {hasattr(context, 'browser_context')}")
    print(f"页面驱动已初始化: {hasattr(context, 'driver')}")


def after_scenario(context, scenario):
    """在每个场景结束后执行"""
    if hasattr(context, 'driver'):
        context.driver.close()
    
    if hasattr(context, 'browser_context'):
        context.browser_context.close()
    
    print(f"场景执行完成: {scenario.name}")


def after_all(context):
    """在所有测试结束后执行"""
    if hasattr(context, 'browser'):
        context.browser.close()
    
    if hasattr(context, 'playwright'):
        context.playwright.stop()
    
    print("测试环境清理完成")
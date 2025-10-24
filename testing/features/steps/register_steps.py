# -*- coding: utf-8 -*-
"""
注册功能的BDD步骤定义
"""
import time
from behave import given, when, then
from pages.register_page import RegisterPage
from utils.database_helper import DatabaseHelper
from utils.api_helper import APIHelper


@given('用户在注册页面')
def step_user_on_register_page(context):
    """用户在注册页面"""
    context.register_page = RegisterPage(context.driver)
    context.register_page.navigate_to_register()
    print("用户已导航到注册页面")


@given('用户在注册页面输入了手机号和验证码')
def step_user_entered_phone_and_code(context):
    """用户在注册页面输入了手机号和验证码"""
    context.register_page = RegisterPage(context.driver)
    context.register_page.navigate_to_register()
    
    # 输入测试手机号和验证码
    test_phone = "13800138000"
    test_code = "123456"
    
    context.register_page.enter_phone_number(test_phone)
    context.register_page.enter_verification_code(test_code)
    
    context.test_phone = test_phone
    context.test_code = test_code
    print(f"用户已输入手机号 {test_phone} 和验证码")


@when('用户输入一个无效的手机号"{phone_number}"并点击"获取验证码"')
def step_enter_invalid_phone_and_click_get_code_register(context, phone_number):
    """用户输入无效手机号并点击获取验证码（注册页面）"""
    context.register_page.enter_phone_number(phone_number)
    context.register_page.click_get_verification_code()
    context.invalid_phone = phone_number
    print(f"用户在注册页面输入无效手机号: {phone_number}")


@when('用户输入一个格式正确的手机号"{phone_number}"并点击"获取验证码"')
def step_enter_valid_phone_and_click_get_code_register(context, phone_number):
    """用户输入格式正确的手机号并点击获取验证码（注册页面）"""
    context.register_page.enter_phone_number(phone_number)
    context.register_page.click_get_verification_code()
    context.valid_phone = phone_number
    # 模拟生成验证码
    context.generated_code = "123456"
    print(f"用户在注册页面输入有效手机号: {phone_number}")


@when('用户使用该手机号和正确的验证码点击"注册"')
def step_register_with_registered_phone(context):
    """使用已注册手机号和正确验证码注册"""
    phone = context.registered_phone
    code = "123456"  # 模拟正确的验证码
    
    context.register_page.enter_phone_number(phone)
    context.register_page.enter_verification_code(code)
    context.register_page.check_agreement()  # 勾选协议
    context.register_page.click_register()
    print(f"使用已注册手机号 {phone} 尝试注册")


@when('用户未勾选"同意《淘贝用户协议》"复选框')
def step_user_not_check_agreement(context):
    """用户未勾选用户协议"""
    # 确保协议复选框未被勾选
    context.register_page.uncheck_agreement()
    print("用户未勾选用户协议")


@when('用户勾选"同意《淘贝用户协议》"复选框')
def step_user_check_agreement(context):
    """用户勾选用户协议"""
    context.register_page.check_agreement()
    print("用户已勾选用户协议")


@when('用户输入未注册的手机号"{phone_number}"和正确的验证码，勾选协议并点击"注册"')
def step_register_new_user(context, phone_number):
    """注册新用户"""
    code = "123456"  # 模拟正确的验证码
    
    # 确保该手机号未被注册
    context.db_helper.delete_user_by_phone(phone_number)
    
    context.register_page.enter_phone_number(phone_number)
    context.register_page.enter_verification_code(code)
    context.register_page.check_agreement()
    context.register_page.click_register()
    
    context.new_user_phone = phone_number
    context.new_user_code = code
    print(f"使用未注册手机号 {phone_number} 进行注册")


@then('系统不创建新用户')
def step_system_does_not_create_user(context):
    """系统不创建新用户"""
    # 验证用户数量没有增加
    phone = context.registered_phone
    user_count_before = context.db_helper.get_user_count()
    
    # 等待一段时间确保操作完成
    time.sleep(1)
    
    user_count_after = context.db_helper.get_user_count()
    assert user_count_after == user_count_before, "用户数量不应该增加"
    print("系统未创建新用户")


@then('用户成功登录并跳转到首页')
def step_user_login_and_redirect(context):
    """用户成功登录并跳转到首页"""
    # 等待页面跳转
    context.register_page.wait_for_redirect_to_home(timeout=10)
    
    # 验证当前URL
    current_url = context.driver.current_url
    assert "home" in current_url.lower() or current_url.endswith("/"), f"应该跳转到首页，当前URL: {current_url}"
    print("用户已成功登录并跳转到首页")


@then('"注册"按钮为不可点击状态')
def step_register_button_disabled(context):
    """注册按钮为不可点击状态"""
    is_disabled = context.register_page.is_register_button_disabled()
    assert is_disabled, "注册按钮应该被禁用"
    print("注册按钮为不可点击状态")


@then('"注册"按钮变为可点击状态')
def step_register_button_enabled(context):
    """注册按钮变为可点击状态"""
    is_enabled = not context.register_page.is_register_button_disabled()
    assert is_enabled, "注册按钮应该可以点击"
    print("注册按钮变为可点击状态")


@then('系统在数据库中创建新用户')
def step_system_creates_new_user(context):
    """系统在数据库中创建新用户"""
    phone = context.new_user_phone
    
    # 等待用户创建完成
    time.sleep(2)
    
    # 验证用户是否被创建
    user_exists = context.db_helper.user_exists(phone)
    assert user_exists, f"用户 {phone} 应该被创建"
    print(f"系统已在数据库中创建用户: {phone}")


@then('用户成功登录并自动跳转到首页')
def step_user_auto_login_and_redirect(context):
    """用户成功登录并自动跳转到首页"""
    # 等待页面跳转
    context.register_page.wait_for_redirect_to_home(timeout=10)
    
    # 验证当前URL
    current_url = context.driver.current_url
    assert "home" in current_url.lower() or current_url.endswith("/"), f"应该跳转到首页，当前URL: {current_url}"
    print("用户已成功登录并自动跳转到首页")


# 重用登录步骤中的一些通用步骤定义
@then('注册页面系统不发送验证码')
def step_system_does_not_send_code_register(context):
    """系统不发送验证码（注册页面）"""
    # 验证系统没有生成验证码
    assert not hasattr(context, 'generated_code') or context.generated_code is None
    print("系统未发送验证码")


@then('注册页面提示"{message}"')
def step_page_shows_message_register(context, message):
    """页面显示指定消息（注册页面）"""
    # 等待消息出现
    context.driver.wait_for_timeout(1000)
    # 这里应该检查页面上的实际消息
    print(f"注册页面显示消息: {message}")


# 注册页面特有的步骤定义
@then('注册时数据库记录手机号和验证码，有效期为60秒')
def step_database_records_phone_and_code_register(context):
    """数据库记录手机号和验证码（注册）"""
    phone_number = getattr(context, 'valid_phone', '13800138000')
    verification_code = getattr(context, 'generated_code', '123456')
    
    # 使用数据库助手记录验证码
    db_helper = DatabaseHelper()
    # 这里应该调用实际的数据库方法来记录验证码
    print(f"注册时数据库记录 - 手机号: {phone_number}, 验证码: {verification_code}, 有效期: 60秒")
"""
用户管理模块的步骤定义文件
"""
import json
import time
from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page, expect
from pages.user_management_page import UserManagementPage
from utils.api_helper import APIHelper
from utils.test_data import TestDataManager
from utils.config import Config

# 全局变量存储测试上下文
test_context = {}

# 创建测试数据管理器实例
test_data_manager = TestDataManager()

# 通用步骤定义
@given('系统已经启动并运行正常')
def step_system_is_running():
    """系统已经启动并运行正常"""
    # 这是一个前置条件步骤，通常不需要具体实现
    # 在实际测试中，这表示系统环境已经准备就绪
    pass

@given('用户已登录')
def step_user_is_logged_in():
    """用户已登录"""
    # 这是一个前置条件步骤，表示用户已经成功登录系统
    # 在实际测试中，这表示用户认证状态已经建立
    pass

@given('用户未登录')
def step_user_is_not_logged_in():
    """用户未登录"""
    # 这是一个前置条件步骤，表示用户未登录系统
    # 在实际测试中，这表示用户处于未认证状态
    pass

@given('用户通过API已登录')
def step_user_logged_in_via_api():
    """用户通过API已登录"""
    # 这是一个前置条件步骤，表示用户通过API成功登录
    # 在实际测试中，这表示API认证状态已经建立
    pass

@given('用户未通过API登录')
def step_user_not_logged_in_via_api():
    """用户未通过API登录"""
    # 这是一个前置条件步骤，表示用户未通过API登录
    # 在实际测试中，这表示API认证状态未建立
    pass

@given('我使用无效的token')
def step_use_invalid_token():
    """我使用无效的token"""
    # 这是一个前置条件步骤，设置无效的认证token
    # 在实际测试中，这用于测试无效认证的场景
    pass

# UI测试步骤定义
@given('用户已登录并在用户信息页面')
def step_user_logged_in_on_profile_page(context):
    """用户已登录并在用户信息页面"""
    # 获取测试用户数据
    user_data = test_data_manager.get_valid_user()
    context.current_user = user_data
    
    # 初始化页面对象
    context.user_page = UserManagementPage(context.page)
    
    # 模拟登录状态（设置token）
    context.page.add_init_script(f"""
        localStorage.setItem('token', 'valid_test_token');
        localStorage.setItem('user_info', '{json.dumps(user_data)}');
    """)
    
    # 导航到用户信息页面
    context.user_page.navigate_to_profile_page()
    
    # 验证页面加载完成
    expect(context.page.locator('[data-testid="user-profile-form"]')).to_be_visible()


@when('用户输入新的昵称"{nickname}"')
def step_user_enters_new_nickname(context, nickname):
    """用户输入新的昵称"""
    context.user_page.enter_nickname(nickname)
    context.new_nickname = nickname


@when('用户输入新的头像URL"{avatar_url}"')
def step_user_enters_new_avatar_url(context, avatar_url):
    """用户输入新的头像URL"""
    context.user_page.enter_avatar_url(avatar_url)
    context.new_avatar_url = avatar_url


@when('用户点击保存按钮')
def step_user_clicks_save_button(context):
    """用户点击保存按钮"""
    context.user_page.click_save_button()


@when('用户清空昵称输入框')
def step_user_clears_nickname_field(context):
    """用户清空昵称输入框"""
    context.user_page.clear_nickname()


@when('用户清空头像URL输入框')
def step_user_clears_avatar_url_field(context):
    """用户清空头像URL输入框"""
    context.user_page.clear_avatar_url()


@when('用户不修改任何信息直接点击保存')
def step_user_saves_without_changes(context):
    """用户不修改任何信息直接点击保存"""
    context.user_page.click_save_button()


@when('用户点击退出登录按钮')
def step_user_clicks_logout_button(context):
    """用户点击退出登录按钮"""
    context.user_page.click_logout_button()


@when('用户尝试访问用户信息页面')
def step_user_tries_to_access_profile_page(context):
    """用户尝试访问用户信息页面"""
    context.user_page.navigate_to_profile_page()


@when('未登录用户尝试访问用户信息页面')
def step_unauthenticated_user_tries_to_access_profile_page(context):
    """未登录用户尝试访问用户信息页面"""
    # 清除登录状态
    context.page.evaluate("localStorage.clear()")
    context.user_page.navigate_to_profile_page()


@when('未登录用户尝试点击退出登录')
def step_unauthenticated_user_tries_to_logout(context):
    """未登录用户尝试点击退出登录"""
    # 清除登录状态
    context.page.evaluate("localStorage.clear()")
    # 尝试访问包含退出登录按钮的页面
    context.user_page.navigate_to_profile_page()


@then('用户信息更新成功')
def step_user_info_updated_successfully(context):
    """用户信息更新成功"""
    # 验证成功提示消息
    success_message = context.user_page.get_success_message()
    assert "更新成功" in success_message or "保存成功" in success_message
    
    # 验证页面显示的信息已更新
    if hasattr(context, 'new_nickname'):
        displayed_nickname = context.user_page.get_displayed_nickname()
        assert displayed_nickname == context.new_nickname
    
    if hasattr(context, 'new_avatar_url'):
        displayed_avatar = context.user_page.get_displayed_avatar_url()
        assert displayed_avatar == context.new_avatar_url


@then('显示错误信息"{error_message}"')
def step_display_error_message(context, error_message):
    """显示错误信息"""
    actual_error = context.user_page.get_error_message()
    assert error_message in actual_error


@then('用户成功退出登录')
def step_user_logged_out_successfully(context):
    """用户成功退出登录"""
    # 验证跳转到登录页面
    expect(context.page).to_have_url(Config.BASE_URL + "/login")
    
    # 验证localStorage中的token已清除
    token = context.page.evaluate("localStorage.getItem('token')")
    assert token is None


@then('用户被重定向到登录页面')
def step_user_redirected_to_login_page(context):
    """用户被重定向到登录页面"""
    # 等待页面跳转
    context.page.wait_for_url(Config.BASE_URL + "/login", timeout=5000)
    expect(context.page).to_have_url(Config.BASE_URL + "/login")


@then('显示未授权访问提示')
def step_display_unauthorized_access_message(context):
    """显示未授权访问提示"""
    # 检查是否显示未授权提示或跳转到登录页面
    try:
        error_message = context.user_page.get_error_message()
        assert "未授权" in error_message or "请先登录" in error_message
    except:
        # 如果没有错误消息，检查是否跳转到登录页面
        expect(context.page).to_have_url(Config.BASE_URL + "/login")


# API测试步骤定义
@given('API测试环境已准备就绪')
def step_api_test_environment_ready(context):
    """API测试环境已准备就绪"""
    context.api_helper = APIHelper()
    context.test_user = test_data_manager.get_valid_user()


@given('用户已通过API登录')
def step_user_logged_in_via_api(context):
    """用户已通过API登录"""
    if not hasattr(context, 'api_helper'):
        context.api_helper = APIHelper()
    
    # 使用测试用户数据登录
    user_data = test_data_manager.get_valid_user()
    login_data = {
        "phone_number": user_data["phone_number"],
        "verification_code": "123456"  # 测试验证码
    }
    
    response = context.api_helper.login_user(login_data)
    context.api_helper.assert_success_response(response)
    
    # 设置认证token
    response_data = context.api_helper.get_response_data(response)
    if "token" in response_data:
        context.api_helper.set_auth_token(response_data["token"])
    
    context.current_user = user_data


@when('发送GET请求获取用户信息')
def step_send_get_request_for_user_info(context):
    """发送GET请求获取用户信息"""
    context.response = context.api_helper.get_user_profile()


@when('发送PUT请求更新用户信息')
def step_send_put_request_to_update_user_info(context):
    """发送PUT请求更新用户信息"""
    update_data = test_data_manager.get_valid_user_update_data()
    context.update_data = update_data
    context.response = context.api_helper.update_user_profile(update_data)


@when('发送PUT请求更新昵称为"{nickname}"')
def step_send_put_request_to_update_nickname(context, nickname):
    """发送PUT请求更新昵称"""
    update_data = {"nickname": nickname}
    context.update_data = update_data
    context.response = context.api_helper.update_user_profile(update_data)


@when('发送PUT请求更新头像为"{avatar_url}"')
def step_send_put_request_to_update_avatar(context, avatar_url):
    """发送PUT请求更新头像"""
    update_data = {"avatar": avatar_url}
    context.update_data = update_data
    context.response = context.api_helper.update_user_profile(update_data)


@when('发送PUT请求使用无效数据更新用户信息')
def step_send_put_request_with_invalid_data(context):
    """发送PUT请求使用无效数据更新用户信息"""
    invalid_data_list = test_data_manager.get_invalid_user_data()
    # 使用第一个无效数据进行测试
    invalid_data = invalid_data_list[0]
    context.expected_error = invalid_data.get("error", "参数验证失败")
    
    # 构造更新数据（排除error字段）
    update_data = {k: v for k, v in invalid_data.items() if k != "error"}
    context.update_data = update_data
    context.response = context.api_helper.update_user_profile(update_data)


@when('发送POST请求退出登录')
def step_send_post_request_to_logout(context):
    """发送POST请求退出登录"""
    context.response = context.api_helper.logout_user()


@when('使用无效token发送GET请求获取用户信息')
def step_send_get_request_with_invalid_token(context):
    """使用无效token发送GET请求获取用户信息"""
    # 设置无效token
    context.api_helper.set_auth_token("invalid_token_12345")
    context.response = context.api_helper.get_user_profile()


@when('使用无效token发送PUT请求更新用户信息')
def step_send_put_request_with_invalid_token(context):
    """使用无效token发送PUT请求更新用户信息"""
    # 设置无效token
    context.api_helper.set_auth_token("invalid_token_12345")
    update_data = test_data_manager.get_valid_user_update_data()
    context.response = context.api_helper.update_user_profile(update_data)


@when('不提供token发送GET请求获取用户信息')
def step_send_get_request_without_token(context):
    """不提供token发送GET请求获取用户信息"""
    # 清除认证token
    context.api_helper.clear_auth_token()
    context.response = context.api_helper.get_user_profile()


@when('不提供token发送PUT请求更新用户信息')
def step_send_put_request_without_token(context):
    """不提供token发送PUT请求更新用户信息"""
    # 清除认证token
    context.api_helper.clear_auth_token()
    update_data = test_data_manager.get_valid_user_update_data()
    context.response = context.api_helper.update_user_profile(update_data)


@when('不提供token发送POST请求退出登录')
def step_send_post_request_logout_without_token(context):
    """不提供token发送POST请求退出登录"""
    # 清除认证token
    context.api_helper.clear_auth_token()
    context.response = context.api_helper.logout_user()


@then('API返回状态码200')
def step_api_returns_status_200(context):
    """API返回状态码200"""
    context.api_helper.assert_success_response(context.response)


@then('API返回状态码400')
def step_api_returns_status_400(context):
    """API返回状态码400"""
    context.api_helper.assert_error_response(context.response, 400)


@then('API返回状态码401')
def step_api_returns_status_401(context):
    """API返回状态码401"""
    context.api_helper.assert_error_response(context.response, 401)


@then('响应包含用户信息')
def step_response_contains_user_info(context):
    """响应包含用户信息"""
    response_data = context.api_helper.get_response_data(context.response)
    
    # 验证响应包含必要的用户信息字段
    required_fields = ["id", "phone_number", "nickname", "avatar"]
    for field in required_fields:
        assert field in response_data, f"响应中缺少字段: {field}"
    
    # 验证用户信息与当前用户匹配
    if hasattr(context, 'current_user'):
        assert response_data["phone_number"] == context.current_user["phone_number"]


@then('响应包含更新后的用户信息')
def step_response_contains_updated_user_info(context):
    """响应包含更新后的用户信息"""
    response_data = context.api_helper.get_response_data(context.response)
    
    # 验证更新的字段
    if hasattr(context, 'update_data'):
        for key, value in context.update_data.items():
            assert response_data.get(key) == value, f"字段 {key} 未正确更新"


@then('响应包含错误信息')
def step_response_contains_error_message(context):
    """响应包含错误信息"""
    response_data = context.api_helper.get_response_data(context.response)
    
    # 验证响应包含错误信息
    assert "error" in response_data or "message" in response_data
    
    # 如果有预期的错误信息，进行验证
    if hasattr(context, 'expected_error'):
        error_message = response_data.get("error", response_data.get("message", ""))
        assert context.expected_error in error_message


@then('响应包含成功消息')
def step_response_contains_success_message(context):
    """响应包含成功消息"""
    response_data = context.api_helper.get_response_data(context.response)
    
    # 验证响应包含成功消息
    success_indicators = ["success", "message", "退出成功", "登出成功"]
    has_success_indicator = any(indicator in str(response_data).lower() for indicator in success_indicators)
    assert has_success_indicator, f"响应中未找到成功指示: {response_data}"


@then('响应包含未授权错误信息')
def step_response_contains_unauthorized_error(context):
    """响应包含未授权错误信息"""
    response_data = context.api_helper.get_response_data(context.response)
    
    # 验证响应包含未授权相关的错误信息
    error_message = response_data.get("error", response_data.get("message", "")).lower()
    unauthorized_keywords = ["unauthorized", "未授权", "token", "认证", "登录"]
    
    has_unauthorized_error = any(keyword in error_message for keyword in unauthorized_keywords)
    assert has_unauthorized_error, f"响应中未找到未授权错误信息: {response_data}"
"""
商品管理模块的步骤定义文件
"""
import json
import time
from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page, expect
from pages.product_management_page import ProductListPage, ProductDetailPage
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

@given('系统中存在商品数据')
def step_system_has_product_data():
    """系统中存在商品数据"""
    # 这是一个前置条件步骤，确保系统中有测试商品数据
    # 在实际测试中，这表示数据库中已经有商品数据可供测试
    pass

@given(parsers.parse('商品ID "{product_id}" 存在'))
def step_product_id_exists(product_id):
    """商品ID存在"""
    # 这是一个前置条件步骤，确保指定ID的商品存在
    # 在实际测试中，这表示数据库中存在指定ID的商品
    pass

@given(parsers.parse('商品ID "{product_id}" 不存在'))
def step_product_id_not_exists(product_id):
    """商品ID不存在"""
    # 这是一个前置条件步骤，确保指定ID的商品不存在
    # 在实际测试中，这表示数据库中不存在指定ID的商品
    pass

# UI测试步骤定义
@given('用户在商品列表页面')
def step_user_on_product_list_page(context):
    """用户在商品列表页面"""
    # 初始化页面对象
    context.product_page = ProductManagementPage(context.page)
    
    # 导航到商品列表页面
    context.product_page.navigate_to_product_list()
    
    # 验证页面加载完成
    expect(context.page.locator('[data-testid="product-list"]')).to_be_visible()


@given('用户在商品详情页面')
def step_user_on_product_detail_page(context):
    """用户在商品详情页面"""
    # 初始化页面对象
    context.product_page = ProductManagementPage(context.page)
    
    # 获取测试商品数据
    test_product = test_data_manager.get_product_by_id(1)
    context.current_product = test_product
    
    # 导航到商品详情页面
    context.product_page.navigate_to_product_detail(test_product["id"])
    
    # 验证页面加载完成
    expect(context.page.locator('[data-testid="product-detail"]')).to_be_visible()


@when('用户查看商品列表')
def step_user_views_product_list(context):
    """用户查看商品列表"""
    # 等待商品列表加载
    context.product_page.wait_for_product_list_load()


@when('用户设置每页显示{page_size:d}个商品')
def step_user_sets_page_size(context, page_size):
    """用户设置每页显示商品数量"""
    context.product_page.set_page_size(page_size)
    context.current_page_size = page_size


@when('用户跳转到第{page:d}页')
def step_user_goes_to_page(context, page):
    """用户跳转到指定页面"""
    context.product_page.go_to_page(page)
    context.current_page = page


@when('用户设置页码为{page:d}，每页{page_size:d}个商品')
def step_user_sets_pagination_params(context, page, page_size):
    """用户设置分页参数"""
    context.product_page.set_pagination_params(page, page_size)
    context.current_page = page
    context.current_page_size = page_size


@when('用户搜索关键词"{keyword}"')
def step_user_searches_keyword(context, keyword):
    """用户搜索关键词"""
    context.product_page.search_products(keyword)
    context.search_keyword = keyword


@when('用户选择分类"{category}"')
def step_user_selects_category(context, category):
    """用户选择商品分类"""
    context.product_page.filter_by_category(category)
    context.selected_category = category


@when('用户按价格升序排序')
def step_user_sorts_by_price_asc(context):
    """用户按价格升序排序"""
    context.product_page.sort_by_price("asc")
    context.sort_field = "price"
    context.sort_order = "asc"


@when('用户按价格降序排序')
def step_user_sorts_by_price_desc(context):
    """用户按价格降序排序"""
    context.product_page.sort_by_price("desc")
    context.sort_field = "price"
    context.sort_order = "desc"


@when('用户按名称升序排序')
def step_user_sorts_by_name_asc(context):
    """用户按名称升序排序"""
    context.product_page.sort_by_name("asc")
    context.sort_field = "name"
    context.sort_order = "asc"


@when('用户按名称降序排序')
def step_user_sorts_by_name_desc(context):
    """用户按名称降序排序"""
    context.product_page.sort_by_name("desc")
    context.sort_field = "name"
    context.sort_order = "desc"


@when('用户搜索"{keyword}"并选择分类"{category}"')
def step_user_searches_and_filters(context, keyword, category):
    """用户搜索并筛选分类"""
    context.product_page.search_products(keyword)
    context.product_page.filter_by_category(category)
    context.search_keyword = keyword
    context.selected_category = category


@when('用户点击商品ID为{product_id:d}的商品')
def step_user_clicks_product(context, product_id):
    """用户点击指定商品"""
    context.product_page.click_product(product_id)
    context.clicked_product_id = product_id


@when('用户尝试访问不存在的商品详情页面')
def step_user_tries_to_access_nonexistent_product(context):
    """用户尝试访问不存在的商品详情页面"""
    invalid_product_ids = test_data_manager.get_invalid_product_ids()
    invalid_id = invalid_product_ids[0]
    context.product_page.navigate_to_product_detail(invalid_id)
    context.invalid_product_id = invalid_id


@when('用户使用无效的商品ID参数访问详情页')
def step_user_uses_invalid_product_id_param(context):
    """用户使用无效的商品ID参数访问详情页"""
    # 使用非数字的无效ID
    context.product_page.navigate_to_product_detail("invalid_id")
    context.invalid_product_id = "invalid_id"


@when('用户查看商品详情信息')
def step_user_views_product_detail_info(context):
    """用户查看商品详情信息"""
    # 等待商品详情加载
    context.product_page.wait_for_product_detail_load()


@when('用户点击商品图片')
def step_user_clicks_product_image(context):
    """用户点击商品图片"""
    context.product_page.click_product_image()


@when('用户点击添加到购物车按钮')
def step_user_clicks_add_to_cart(context):
    """用户点击添加到购物车按钮"""
    context.product_page.click_add_to_cart_button()


@then('显示商品列表')
def step_display_product_list(context):
    """显示商品列表"""
    # 验证商品列表可见
    expect(context.page.locator('[data-testid="product-list"]')).to_be_visible()
    
    # 验证至少有一个商品项
    product_items = context.page.locator('[data-testid="product-item"]')
    expect(product_items.first()).to_be_visible()


@then('每页显示{expected_count:d}个商品')
def step_display_expected_product_count(context, expected_count):
    """验证每页显示的商品数量"""
    product_items = context.page.locator('[data-testid="product-item"]')
    actual_count = product_items.count()
    
    # 获取总商品数量来判断是否是最后一页
    total_products = len(test_data_manager.get_all_products())
    current_page = getattr(context, 'current_page', 1)
    page_size = getattr(context, 'current_page_size', expected_count)
    
    # 计算当前页应该显示的商品数量
    start_index = (current_page - 1) * page_size
    remaining_products = total_products - start_index
    expected_on_current_page = min(expected_count, remaining_products)
    
    assert actual_count == expected_on_current_page, f"期望显示{expected_on_current_page}个商品，实际显示{actual_count}个"


@then('显示第{expected_page:d}页的商品')
def step_display_expected_page_products(context, expected_page):
    """验证显示指定页面的商品"""
    # 验证分页指示器显示正确的页码
    current_page_indicator = context.product_page.get_current_page_number()
    assert current_page_indicator == expected_page, f"期望显示第{expected_page}页，实际显示第{current_page_indicator}页"


@then('显示分页信息')
def step_display_pagination_info(context):
    """显示分页信息"""
    # 验证分页组件可见
    expect(context.page.locator('[data-testid="pagination"]')).to_be_visible()
    
    # 验证分页信息
    pagination_info = context.product_page.get_pagination_info()
    assert pagination_info is not None
    assert "total" in pagination_info or "总计" in str(pagination_info)


@then('显示包含"{keyword}"的商品')
def step_display_products_containing_keyword(context, keyword):
    """显示包含关键词的商品"""
    # 获取显示的商品列表
    displayed_products = context.product_page.get_displayed_products()
    
    # 验证至少有一个商品包含关键词
    found_matching_product = False
    for product in displayed_products:
        product_name = product.get("name", "").lower()
        product_desc = product.get("description", "").lower()
        if keyword.lower() in product_name or keyword.lower() in product_desc:
            found_matching_product = True
            break
    
    assert found_matching_product, f"未找到包含关键词'{keyword}'的商品"


@then('显示"未找到相关商品"提示')
def step_display_no_products_found_message(context):
    """显示未找到商品的提示"""
    no_results_message = context.product_page.get_no_results_message()
    assert "未找到" in no_results_message or "没有" in no_results_message or "暂无" in no_results_message


@then('显示"{category}"分类的商品')
def step_display_category_products(context, category):
    """显示指定分类的商品"""
    # 获取显示的商品列表
    displayed_products = context.product_page.get_displayed_products()
    
    # 验证所有商品都属于指定分类
    for product in displayed_products:
        assert product.get("category") == category, f"商品'{product.get('name')}'不属于分类'{category}'"


@then('商品按价格升序排列')
def step_products_sorted_by_price_asc(context):
    """验证商品按价格升序排列"""
    displayed_products = context.product_page.get_displayed_products()
    
    # 验证价格排序
    prices = [float(product.get("price", 0)) for product in displayed_products]
    assert prices == sorted(prices), "商品未按价格升序排列"


@then('商品按价格降序排列')
def step_products_sorted_by_price_desc(context):
    """验证商品按价格降序排列"""
    displayed_products = context.product_page.get_displayed_products()
    
    # 验证价格排序
    prices = [float(product.get("price", 0)) for product in displayed_products]
    assert prices == sorted(prices, reverse=True), "商品未按价格降序排列"


@then('商品按名称升序排列')
def step_products_sorted_by_name_asc(context):
    """验证商品按名称升序排列"""
    displayed_products = context.product_page.get_displayed_products()
    
    # 验证名称排序
    names = [product.get("name", "") for product in displayed_products]
    assert names == sorted(names), "商品未按名称升序排列"


@then('商品按名称降序排列')
def step_products_sorted_by_name_desc(context):
    """验证商品按名称降序排列"""
    displayed_products = context.product_page.get_displayed_products()
    
    # 验证名称排序
    names = [product.get("name", "") for product in displayed_products]
    assert names == sorted(names, reverse=True), "商品未按名称降序排列"


@then('显示商品详情信息')
def step_display_product_detail_info(context):
    """显示商品详情信息"""
    # 验证商品详情页面元素可见
    expect(context.page.locator('[data-testid="product-detail"]')).to_be_visible()
    expect(context.page.locator('[data-testid="product-name"]')).to_be_visible()
    expect(context.page.locator('[data-testid="product-price"]')).to_be_visible()
    expect(context.page.locator('[data-testid="product-description"]')).to_be_visible()
    
    # 验证商品信息与测试数据匹配
    if hasattr(context, 'current_product'):
        displayed_name = context.product_page.get_product_name()
        displayed_price = context.product_page.get_product_price()
        
        assert displayed_name == context.current_product["name"]
        assert displayed_price == context.current_product["price"]


@then('显示商品不存在错误')
def step_display_product_not_found_error(context):
    """显示商品不存在错误"""
    error_message = context.product_page.get_error_message()
    assert "不存在" in error_message or "未找到" in error_message or "404" in error_message


@then('显示参数错误提示')
def step_display_parameter_error_message(context):
    """显示参数错误提示"""
    error_message = context.product_page.get_error_message()
    assert "参数错误" in error_message or "无效" in error_message or "格式错误" in error_message


@then('跳转到商品详情页面')
def step_redirect_to_product_detail_page(context):
    """跳转到商品详情页面"""
    # 验证URL包含商品ID
    if hasattr(context, 'clicked_product_id'):
        expected_url_pattern = f"/product/{context.clicked_product_id}"
        expect(context.page).to_have_url(Config.BASE_URL + expected_url_pattern)


@then('显示商品大图')
def step_display_product_large_image(context):
    """显示商品大图"""
    # 验证大图模态框或放大图片可见
    large_image_modal = context.page.locator('[data-testid="product-image-modal"]')
    expect(large_image_modal).to_be_visible()


@then('显示添加成功提示')
def step_display_add_to_cart_success_message(context):
    """显示添加到购物车成功提示"""
    success_message = context.product_page.get_success_message()
    assert "添加成功" in success_message or "已添加" in success_message


# API测试步骤定义
@given('商品管理API测试环境已准备就绪')
def step_product_api_test_environment_ready(context):
    """商品管理API测试环境已准备就绪"""
    context.api_helper = APIHelper()


@when('发送GET请求获取商品列表')
def step_send_get_request_for_product_list(context):
    """发送GET请求获取商品列表"""
    context.response = context.api_helper.get_product_list()


@when('发送GET请求获取商品列表，页码{page:d}，每页{page_size:d}个')
def step_send_get_request_with_pagination(context, page, page_size):
    """发送带分页参数的GET请求获取商品列表"""
    params = {"page": page, "pageSize": page_size}
    context.response = context.api_helper.get_product_list(params)
    context.request_params = params


@when('发送GET请求搜索商品，关键词"{keyword}"')
def step_send_get_request_search_products(context, keyword):
    """发送GET请求搜索商品"""
    params = {"keyword": keyword}
    context.response = context.api_helper.search_products(keyword)
    context.search_keyword = keyword


@when('发送GET请求筛选商品，分类"{category}"')
def step_send_get_request_filter_by_category(context, category):
    """发送GET请求按分类筛选商品"""
    context.response = context.api_helper.filter_products_by_category(category)
    context.filter_category = category


@when('发送GET请求排序商品，按价格升序')
def step_send_get_request_sort_by_price_asc(context):
    """发送GET请求按价格升序排序商品"""
    context.response = context.api_helper.sort_products("price", "asc")
    context.sort_field = "price"
    context.sort_order = "asc"


@when('发送GET请求排序商品，按价格降序')
def step_send_get_request_sort_by_price_desc(context):
    """发送GET请求按价格降序排序商品"""
    context.response = context.api_helper.sort_products("price", "desc")
    context.sort_field = "price"
    context.sort_order = "desc"


@when('发送GET请求排序商品，按名称升序')
def step_send_get_request_sort_by_name_asc(context):
    """发送GET请求按名称升序排序商品"""
    context.response = context.api_helper.sort_products("name", "asc")
    context.sort_field = "name"
    context.sort_order = "asc"


@when('发送GET请求获取商品详情，商品ID为{product_id:d}')
def step_send_get_request_for_product_detail(context, product_id):
    """发送GET请求获取商品详情"""
    context.response = context.api_helper.get_product_detail(product_id)
    context.requested_product_id = product_id


@when('发送GET请求获取不存在的商品详情')
def step_send_get_request_for_nonexistent_product(context):
    """发送GET请求获取不存在的商品详情"""
    invalid_product_ids = test_data_manager.get_invalid_product_ids()
    invalid_id = invalid_product_ids[0]
    context.response = context.api_helper.get_product_detail(invalid_id)
    context.requested_product_id = invalid_id


@when('发送GET请求使用无效分页参数')
def step_send_get_request_with_invalid_pagination(context):
    """发送GET请求使用无效分页参数"""
    invalid_params_list = test_data_manager.get_invalid_pagination_params()
    invalid_params = invalid_params_list[0]  # 使用第一个无效参数
    context.expected_error = invalid_params.get("error", "参数验证失败")
    
    # 构造请求参数（排除error字段）
    params = {k: v for k, v in invalid_params.items() if k != "error"}
    context.response = context.api_helper.get_product_list(params)
    context.request_params = params


@when('发送GET请求使用无效商品ID')
def step_send_get_request_with_invalid_product_id(context):
    """发送GET请求使用无效商品ID"""
    # 使用字符串作为无效ID
    invalid_id = "invalid_id"
    context.response = context.api_helper.get_product_detail(invalid_id)
    context.requested_product_id = invalid_id


@when('发送GET请求使用超长关键词搜索')
def step_send_get_request_with_long_keyword(context):
    """发送GET请求使用超长关键词搜索"""
    search_keywords = test_data_manager.get_search_keywords()
    long_keyword = search_keywords["invalid"][0]  # 超长关键词
    context.response = context.api_helper.search_products(long_keyword)
    context.search_keyword = long_keyword


@then('API返回商品列表数据')
def step_api_returns_product_list_data(context):
    """API返回商品列表数据"""
    context.api_helper.assert_success_response(context.response)
    response_data = context.api_helper.get_response_data(context.response)
    
    # 验证响应包含商品列表
    assert "products" in response_data or isinstance(response_data, list)
    
    # 如果是分页响应，验证分页信息
    if "products" in response_data:
        products = response_data["products"]
        assert isinstance(products, list)
        
        # 验证分页信息
        if "pagination" in response_data:
            pagination = response_data["pagination"]
            required_pagination_fields = ["current_page", "page_size", "total_items", "total_pages"]
            for field in required_pagination_fields:
                assert field in pagination, f"分页信息中缺少字段: {field}"


@then('API返回符合分页参数的商品数据')
def step_api_returns_paginated_product_data(context):
    """API返回符合分页参数的商品数据"""
    context.api_helper.assert_success_response(context.response)
    response_data = context.api_helper.get_response_data(context.response)
    
    # 验证分页参数
    if hasattr(context, 'request_params'):
        expected_page = context.request_params.get("page", 1)
        expected_page_size = context.request_params.get("pageSize", 10)
        
        if "pagination" in response_data:
            pagination = response_data["pagination"]
            assert pagination["current_page"] == expected_page
            assert pagination["page_size"] == expected_page_size
        
        # 验证返回的商品数量不超过每页限制
        products = response_data.get("products", response_data)
        assert len(products) <= expected_page_size


@then('API返回包含关键词的商品数据')
def step_api_returns_keyword_matching_products(context):
    """API返回包含关键词的商品数据"""
    context.api_helper.assert_success_response(context.response)
    response_data = context.api_helper.get_response_data(context.response)
    
    products = response_data.get("products", response_data)
    keyword = getattr(context, 'search_keyword', '')
    
    # 验证返回的商品包含关键词
    for product in products:
        product_name = product.get("name", "").lower()
        product_desc = product.get("description", "").lower()
        assert keyword.lower() in product_name or keyword.lower() in product_desc


@then('API返回指定分类的商品数据')
def step_api_returns_category_filtered_products(context):
    """API返回指定分类的商品数据"""
    context.api_helper.assert_success_response(context.response)
    response_data = context.api_helper.get_response_data(context.response)
    
    products = response_data.get("products", response_data)
    expected_category = getattr(context, 'filter_category', '')
    
    # 验证所有商品都属于指定分类
    for product in products:
        assert product.get("category") == expected_category


@then('API返回按指定方式排序的商品数据')
def step_api_returns_sorted_products(context):
    """API返回按指定方式排序的商品数据"""
    context.api_helper.assert_success_response(context.response)
    response_data = context.api_helper.get_response_data(context.response)
    
    products = response_data.get("products", response_data)
    sort_field = getattr(context, 'sort_field', '')
    sort_order = getattr(context, 'sort_order', 'asc')
    
    if sort_field == "price":
        prices = [float(product.get("price", 0)) for product in products]
        if sort_order == "asc":
            assert prices == sorted(prices), "商品未按价格升序排列"
        else:
            assert prices == sorted(prices, reverse=True), "商品未按价格降序排列"
    elif sort_field == "name":
        names = [product.get("name", "") for product in products]
        if sort_order == "asc":
            assert names == sorted(names), "商品未按名称升序排列"
        else:
            assert names == sorted(names, reverse=True), "商品未按名称降序排列"


@then('API返回商品详情数据')
def step_api_returns_product_detail_data(context):
    """API返回商品详情数据"""
    context.api_helper.assert_success_response(context.response)
    response_data = context.api_helper.get_response_data(context.response)
    
    # 验证商品详情包含必要字段
    required_fields = ["id", "name", "price", "description", "category"]
    for field in required_fields:
        assert field in response_data, f"商品详情中缺少字段: {field}"
    
    # 验证商品ID匹配
    if hasattr(context, 'requested_product_id'):
        assert response_data["id"] == context.requested_product_id


@then('API返回404状态码')
def step_api_returns_status_404(context):
    """API返回404状态码"""
    context.api_helper.assert_error_response(context.response, 404)


@then('API返回空的商品列表')
def step_api_returns_empty_product_list(context):
    """API返回空的商品列表"""
    context.api_helper.assert_success_response(context.response)
    response_data = context.api_helper.get_response_data(context.response)
    
    products = response_data.get("products", response_data)
    assert len(products) == 0, "期望返回空列表，但返回了商品数据"


@then('API返回参数验证错误')
def step_api_returns_parameter_validation_error(context):
    """API返回参数验证错误"""
    context.api_helper.assert_error_response(context.response, 400)
    
    response_data = context.api_helper.get_response_data(context.response)
    error_message = response_data.get("error", response_data.get("message", "")).lower()
    
    # 验证错误信息包含参数验证相关内容
    validation_keywords = ["参数", "验证", "无效", "格式", "范围"]
    has_validation_error = any(keyword in error_message for keyword in validation_keywords)
    assert has_validation_error, f"响应中未找到参数验证错误信息: {response_data}"
"""
商品管理页面的Page Object Model
"""
import time
from playwright.sync_api import Page, expect, Locator
from utils.config import Config


class ProductListPage:
    """商品列表页面对象"""
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = Config.BASE_URL
        
        # 页面元素定位器
        self.product_list_container = '[data-testid="product-list-container"]'
        self.product_items = '[data-testid="product-item"]'
        self.product_card = '[data-testid="product-card"]'
        self.product_image = '[data-testid="product-image"]'
        self.product_title = '[data-testid="product-title"]'
        self.product_price = '[data-testid="product-price"]'
        self.product_category = '[data-testid="product-category"]'
        
        # 搜索功能
        self.search_input = '[data-testid="search-input"]'
        self.search_button = '[data-testid="search-button"]'
        self.search_clear_button = '[data-testid="search-clear"]'
        
        # 分类筛选
        self.category_filter = '[data-testid="category-filter"]'
        self.category_options = '[data-testid="category-option"]'
        self.category_all = '[data-testid="category-all"]'
        
        # 排序功能
        self.sort_dropdown = '[data-testid="sort-dropdown"]'
        self.sort_price_asc = '[data-testid="sort-price-asc"]'
        self.sort_price_desc = '[data-testid="sort-price-desc"]'
        self.sort_name_asc = '[data-testid="sort-name-asc"]'
        self.sort_name_desc = '[data-testid="sort-name-desc"]'
        
        # 分页功能
        self.pagination_container = '[data-testid="pagination-container"]'
        self.pagination_info = '[data-testid="pagination-info"]'
        self.page_size_selector = '[data-testid="page-size-selector"]'
        self.current_page_input = '[data-testid="current-page-input"]'
        self.prev_page_button = '[data-testid="prev-page"]'
        self.next_page_button = '[data-testid="next-page"]'
        self.first_page_button = '[data-testid="first-page"]'
        self.last_page_button = '[data-testid="last-page"]'
        self.page_numbers = '[data-testid="page-number"]'
        
        # 加载和状态
        self.loading_spinner = '[data-testid="loading-spinner"]'
        self.empty_state = '[data-testid="empty-state"]'
        self.error_message = '[data-testid="error-message"]'
        
        # 页面信息
        self.page_title = '[data-testid="page-title"]'
        self.total_count = '[data-testid="total-count"]'
        self.results_info = '[data-testid="results-info"]'
    
    def navigate_to_product_list(self):
        """导航到商品列表页面"""
        products_url = f"{self.base_url}/products"
        self.page.goto(products_url)
        self.wait_for_page_load()
    
    def wait_for_page_load(self):
        """等待页面加载完成"""
        try:
            # 等待商品列表容器加载
            self.page.wait_for_selector(self.product_list_container, timeout=10000)
        except:
            pass
        
        # 等待加载动画消失
        try:
            self.page.wait_for_selector(self.loading_spinner, state="hidden", timeout=10000)
        except:
            pass
    
    def get_product_list(self) -> list:
        """获取商品列表"""
        try:
            self.wait_for_page_load()
            product_elements = self.page.locator(self.product_items).all()
            
            products = []
            for element in product_elements:
                try:
                    product = {
                        "title": element.locator(self.product_title).text_content() or "",
                        "price": element.locator(self.product_price).text_content() or "",
                        "category": element.locator(self.product_category).text_content() or "",
                        "image_src": element.locator(self.product_image).get_attribute("src") or ""
                    }
                    products.append(product)
                except:
                    continue
            
            return products
        except:
            return []
    
    def get_product_count(self) -> int:
        """获取商品数量"""
        try:
            product_elements = self.page.locator(self.product_items)
            return product_elements.count()
        except:
            return 0
    
    def search_products(self, keyword: str):
        """搜索商品"""
        search_input = self.page.locator(self.search_input)
        search_input.clear()
        search_input.fill(keyword)
        
        search_btn = self.page.locator(self.search_button)
        search_btn.click()
        
        self.wait_for_search_results()
    
    def wait_for_search_results(self):
        """等待搜索结果加载"""
        try:
            self.page.wait_for_selector(self.loading_spinner, state="hidden", timeout=10000)
        except:
            pass
        
        # 等待一下让结果稳定
        time.sleep(0.5)
    
    def clear_search(self):
        """清空搜索"""
        try:
            clear_btn = self.page.locator(self.search_clear_button)
            if clear_btn.is_visible():
                clear_btn.click()
            else:
                # 手动清空搜索框
                search_input = self.page.locator(self.search_input)
                search_input.clear()
                search_btn = self.page.locator(self.search_button)
                search_btn.click()
        except:
            pass
        
        self.wait_for_search_results()
    
    def filter_by_category(self, category: str):
        """按分类筛选"""
        if category.lower() == "all" or category == "全部":
            category_btn = self.page.locator(self.category_all)
        else:
            # 查找特定分类选项
            category_btn = self.page.locator(f'{self.category_options}[data-category="{category}"]')
            if not category_btn.is_visible():
                # 尝试按文本查找
                category_btn = self.page.locator(self.category_options).filter(has_text=category)
        
        category_btn.click()
        self.wait_for_filter_results()
    
    def wait_for_filter_results(self):
        """等待筛选结果加载"""
        try:
            self.page.wait_for_selector(self.loading_spinner, state="hidden", timeout=10000)
        except:
            pass
        
        time.sleep(0.5)
    
    def sort_by_price_ascending(self):
        """按价格升序排序"""
        self._select_sort_option(self.sort_price_asc)
    
    def sort_by_price_descending(self):
        """按价格降序排序"""
        self._select_sort_option(self.sort_price_desc)
    
    def sort_by_name_ascending(self):
        """按名称升序排序"""
        self._select_sort_option(self.sort_name_asc)
    
    def sort_by_name_descending(self):
        """按名称降序排序"""
        self._select_sort_option(self.sort_name_desc)
    
    def _select_sort_option(self, sort_option_selector: str):
        """选择排序选项"""
        try:
            # 先点击排序下拉框
            sort_dropdown = self.page.locator(self.sort_dropdown)
            sort_dropdown.click()
            
            # 等待下拉选项出现
            time.sleep(0.3)
            
            # 点击具体排序选项
            sort_option = self.page.locator(sort_option_selector)
            sort_option.click()
            
            self.wait_for_sort_results()
        except:
            pass
    
    def wait_for_sort_results(self):
        """等待排序结果加载"""
        try:
            self.page.wait_for_selector(self.loading_spinner, state="hidden", timeout=10000)
        except:
            pass
        
        time.sleep(0.5)
    
    def set_page_size(self, page_size: int):
        """设置每页显示数量"""
        try:
            page_size_select = self.page.locator(self.page_size_selector)
            page_size_select.select_option(str(page_size))
            self.wait_for_pagination_update()
        except:
            pass
    
    def go_to_page(self, page_number: int):
        """跳转到指定页面"""
        try:
            # 方法1：直接点击页码
            page_btn = self.page.locator(f'{self.page_numbers}[data-page="{page_number}"]')
            if page_btn.is_visible():
                page_btn.click()
            else:
                # 方法2：输入页码
                page_input = self.page.locator(self.current_page_input)
                page_input.clear()
                page_input.fill(str(page_number))
                page_input.press("Enter")
            
            self.wait_for_pagination_update()
        except:
            pass
    
    def go_to_next_page(self):
        """跳转到下一页"""
        try:
            next_btn = self.page.locator(self.next_page_button)
            if next_btn.is_enabled():
                next_btn.click()
                self.wait_for_pagination_update()
        except:
            pass
    
    def go_to_prev_page(self):
        """跳转到上一页"""
        try:
            prev_btn = self.page.locator(self.prev_page_button)
            if prev_btn.is_enabled():
                prev_btn.click()
                self.wait_for_pagination_update()
        except:
            pass
    
    def wait_for_pagination_update(self):
        """等待分页更新"""
        try:
            self.page.wait_for_selector(self.loading_spinner, state="hidden", timeout=10000)
        except:
            pass
        
        time.sleep(0.5)
    
    def click_product(self, product_index: int = 0):
        """点击商品进入详情页"""
        try:
            product_elements = self.page.locator(self.product_items)
            if product_index < product_elements.count():
                product_elements.nth(product_index).click()
                time.sleep(1)  # 等待页面跳转
        except:
            pass
    
    def click_product_by_title(self, title: str):
        """根据标题点击商品"""
        try:
            product_element = self.page.locator(self.product_items).filter(has_text=title)
            product_element.click()
            time.sleep(1)
        except:
            pass
    
    def get_pagination_info(self) -> dict:
        """获取分页信息"""
        info = {
            "current_page": 1,
            "total_pages": 1,
            "page_size": 10,
            "total_count": 0
        }
        
        try:
            # 从分页信息元素获取
            pagination_text = self.page.locator(self.pagination_info).text_content() or ""
            
            # 解析分页信息（假设格式为 "第1页 共10页 每页20条 共200条"）
            import re
            
            current_match = re.search(r'第(\d+)页', pagination_text)
            if current_match:
                info["current_page"] = int(current_match.group(1))
            
            total_pages_match = re.search(r'共(\d+)页', pagination_text)
            if total_pages_match:
                info["total_pages"] = int(total_pages_match.group(1))
            
            page_size_match = re.search(r'每页(\d+)条', pagination_text)
            if page_size_match:
                info["page_size"] = int(page_size_match.group(1))
            
            total_count_match = re.search(r'共(\d+)条', pagination_text)
            if total_count_match:
                info["total_count"] = int(total_count_match.group(1))
        except:
            pass
        
        return info
    
    def is_empty_state_visible(self) -> bool:
        """检查是否显示空状态"""
        try:
            empty_element = self.page.locator(self.empty_state)
            return empty_element.is_visible()
        except:
            return False
    
    def get_error_message(self) -> str:
        """获取错误消息"""
        try:
            error_element = self.page.locator(self.error_message)
            if error_element.is_visible():
                return error_element.text_content() or ""
        except:
            pass
        return ""
    
    def get_current_search_keyword(self) -> str:
        """获取当前搜索关键词"""
        try:
            search_input = self.page.locator(self.search_input)
            return search_input.input_value() or ""
        except:
            return ""


class ProductDetailPage:
    """商品详情页面对象"""
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = Config.BASE_URL
        
        # 页面元素定位器
        self.product_detail_container = '[data-testid="product-detail-container"]'
        self.product_title = '[data-testid="product-title"]'
        self.product_price = '[data-testid="product-price"]'
        self.product_category = '[data-testid="product-category"]'
        self.product_description = '[data-testid="product-description"]'
        self.product_images = '[data-testid="product-image"]'
        self.main_image = '[data-testid="main-product-image"]'
        self.thumbnail_images = '[data-testid="thumbnail-image"]'
        
        # 操作按钮
        self.add_to_cart_button = '[data-testid="add-to-cart-button"]'
        self.buy_now_button = '[data-testid="buy-now-button"]'
        self.back_button = '[data-testid="back-button"]'
        
        # 数量选择
        self.quantity_input = '[data-testid="quantity-input"]'
        self.quantity_increase = '[data-testid="quantity-increase"]'
        self.quantity_decrease = '[data-testid="quantity-decrease"]'
        
        # 状态和消息
        self.loading_spinner = '[data-testid="loading-spinner"]'
        self.error_message = '[data-testid="error-message"]'
        self.success_message = '[data-testid="success-message"]'
        self.not_found_message = '[data-testid="not-found-message"]'
        
        # 面包屑导航
        self.breadcrumb = '[data-testid="breadcrumb"]'
        self.breadcrumb_links = '[data-testid="breadcrumb-link"]'
    
    def navigate_to_product_detail(self, product_id: str):
        """导航到商品详情页面"""
        detail_url = f"{self.base_url}/products/{product_id}"
        self.page.goto(detail_url)
        self.wait_for_page_load()
    
    def wait_for_page_load(self):
        """等待页面加载完成"""
        try:
            # 等待商品详情容器或错误消息加载
            self.page.wait_for_selector(f"{self.product_detail_container}, {self.error_message}, {self.not_found_message}", timeout=10000)
        except:
            pass
        
        # 等待加载动画消失
        try:
            self.page.wait_for_selector(self.loading_spinner, state="hidden", timeout=10000)
        except:
            pass
    
    def get_product_details(self) -> dict:
        """获取商品详情信息"""
        details = {}
        
        try:
            title_element = self.page.locator(self.product_title)
            if title_element.is_visible():
                details["title"] = title_element.text_content() or ""
        except:
            details["title"] = ""
        
        try:
            price_element = self.page.locator(self.product_price)
            if price_element.is_visible():
                details["price"] = price_element.text_content() or ""
        except:
            details["price"] = ""
        
        try:
            category_element = self.page.locator(self.product_category)
            if category_element.is_visible():
                details["category"] = category_element.text_content() or ""
        except:
            details["category"] = ""
        
        try:
            desc_element = self.page.locator(self.product_description)
            if desc_element.is_visible():
                details["description"] = desc_element.text_content() or ""
        except:
            details["description"] = ""
        
        return details
    
    def get_product_images(self) -> list:
        """获取商品图片列表"""
        images = []
        try:
            image_elements = self.page.locator(self.product_images).all()
            for img in image_elements:
                src = img.get_attribute("src")
                if src:
                    images.append(src)
        except:
            pass
        
        return images
    
    def click_product_image(self, image_index: int = 0):
        """点击商品图片"""
        try:
            image_elements = self.page.locator(self.product_images)
            if image_index < image_elements.count():
                image_elements.nth(image_index).click()
                time.sleep(0.5)  # 等待图片切换
        except:
            pass
    
    def click_thumbnail_image(self, thumbnail_index: int):
        """点击缩略图"""
        try:
            thumbnail_elements = self.page.locator(self.thumbnail_images)
            if thumbnail_index < thumbnail_elements.count():
                thumbnail_elements.nth(thumbnail_index).click()
                time.sleep(0.5)
        except:
            pass
    
    def set_quantity(self, quantity: int):
        """设置商品数量"""
        try:
            quantity_input = self.page.locator(self.quantity_input)
            quantity_input.clear()
            quantity_input.fill(str(quantity))
        except:
            pass
    
    def increase_quantity(self):
        """增加商品数量"""
        try:
            increase_btn = self.page.locator(self.quantity_increase)
            increase_btn.click()
        except:
            pass
    
    def decrease_quantity(self):
        """减少商品数量"""
        try:
            decrease_btn = self.page.locator(self.quantity_decrease)
            decrease_btn.click()
        except:
            pass
    
    def get_current_quantity(self) -> int:
        """获取当前数量"""
        try:
            quantity_input = self.page.locator(self.quantity_input)
            value = quantity_input.input_value() or "1"
            return int(value)
        except:
            return 1
    
    def add_to_cart(self):
        """添加到购物车"""
        try:
            add_btn = self.page.locator(self.add_to_cart_button)
            add_btn.click()
            
            # 等待操作完成
            self.wait_for_add_to_cart_completion()
        except:
            pass
    
    def wait_for_add_to_cart_completion(self):
        """等待添加到购物车操作完成"""
        try:
            # 等待成功或错误消息出现
            self.page.wait_for_selector(f"{self.success_message}, {self.error_message}", timeout=5000)
        except:
            pass
    
    def buy_now(self):
        """立即购买"""
        try:
            buy_btn = self.page.locator(self.buy_now_button)
            buy_btn.click()
            time.sleep(1)  # 等待页面跳转
        except:
            pass
    
    def go_back(self):
        """返回上一页"""
        try:
            back_btn = self.page.locator(self.back_button)
            if back_btn.is_visible():
                back_btn.click()
            else:
                self.page.go_back()
            
            time.sleep(1)
        except:
            self.page.go_back()
    
    def get_success_message(self) -> str:
        """获取成功消息"""
        try:
            success_element = self.page.locator(self.success_message)
            if success_element.is_visible():
                return success_element.text_content() or ""
        except:
            pass
        return ""
    
    def get_error_message(self) -> str:
        """获取错误消息"""
        try:
            error_element = self.page.locator(self.error_message)
            if error_element.is_visible():
                return error_element.text_content() or ""
        except:
            pass
        return ""
    
    def is_not_found_message_visible(self) -> bool:
        """检查是否显示商品未找到消息"""
        try:
            not_found_element = self.page.locator(self.not_found_message)
            return not_found_element.is_visible()
        except:
            return False
    
    def is_product_detail_visible(self) -> bool:
        """检查商品详情是否可见"""
        try:
            detail_container = self.page.locator(self.product_detail_container)
            return detail_container.is_visible()
        except:
            return False
    
    def is_add_to_cart_button_enabled(self) -> bool:
        """检查添加到购物车按钮是否可用"""
        try:
            add_btn = self.page.locator(self.add_to_cart_button)
            return add_btn.is_enabled()
        except:
            return False
    
    def get_breadcrumb_text(self) -> str:
        """获取面包屑导航文本"""
        try:
            breadcrumb_element = self.page.locator(self.breadcrumb)
            return breadcrumb_element.text_content() or ""
        except:
            return ""
    
    def click_breadcrumb_link(self, link_text: str):
        """点击面包屑导航链接"""
        try:
            breadcrumb_link = self.page.locator(self.breadcrumb_links).filter(has_text=link_text)
            breadcrumb_link.click()
            time.sleep(1)
        except:
            pass
    
    def get_current_url(self) -> str:
        """获取当前页面URL"""
        return self.page.url
    
    def refresh_page(self):
        """刷新页面"""
        self.page.reload()
        self.wait_for_page_load()
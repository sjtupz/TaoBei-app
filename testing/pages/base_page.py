"""
基础页面类
"""
from playwright.sync_api import Page, Locator, expect
from typing import Optional
import time


class BasePage:
    """页面对象基类"""
    
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 30000  # 30秒超时
    
    def navigate_to(self, url: str):
        """导航到指定URL"""
        # 如果URL是相对路径，需要拼接基础URL
        if url.startswith('/'):
            from utils.config import Config
            config = Config()
            full_url = f"{config.BASE_URL}{url}"
        else:
            full_url = url
        self.page.goto(full_url)
    
    def wait_for_page_load(self, timeout: int = 30000):
        """等待页面加载完成"""
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def get_element(self, selector: str) -> Locator:
        """获取页面元素"""
        return self.page.locator(selector)
    
    def click_element(self, selector: str, timeout: int = None):
        """点击元素"""
        timeout = timeout or self.timeout
        element = self.get_element(selector)
        element.wait_for(state="visible", timeout=timeout)
        # 确保元素可点击
        element.wait_for(state="attached", timeout=timeout)
        element.click(timeout=timeout)
    
    def fill_input(self, selector: str, text: str, timeout: int = None):
        """填充输入框"""
        timeout = timeout or self.timeout
        element = self.get_element(selector)
        element.wait_for(state="visible", timeout=timeout)
        element.wait_for(state="attached", timeout=timeout)
        element.clear()
        element.fill(text, timeout=timeout)
    
    def get_text(self, selector: str, timeout: int = None) -> str:
        """获取元素文本"""
        timeout = timeout or self.timeout
        element = self.get_element(selector)
        element.wait_for(state="visible", timeout=timeout)
        return element.text_content()
    
    def is_element_visible(self, selector: str, timeout: int = 5000) -> bool:
        """检查元素是否可见"""
        try:
            element = self.get_element(selector)
            element.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False
    
    def is_element_enabled(self, selector: str) -> bool:
        """检查元素是否可用"""
        element = self.get_element(selector)
        return element.is_enabled()
    
    def wait_for_element(self, selector: str, state: str = "visible", timeout: int = None):
        """等待元素状态"""
        timeout = timeout or self.timeout
        try:
            element = self.get_element(selector)
            element.wait_for(state=state, timeout=timeout)
            return element
        except Exception as e:
            print(f"等待元素失败 - 选择器: {selector}, 状态: {state}, 错误: {e}")
            return None
    
    def wait_for_text(self, selector: str, text: str, timeout: int = None):
        """等待元素包含指定文本"""
        timeout = timeout or self.timeout
        element = self.get_element(selector)
        expect(element).to_contain_text(text, timeout=timeout)
    
    def wait_for_url(self, url_pattern: str, timeout: int = None):
        """等待URL匹配"""
        timeout = timeout or self.timeout
        self.page.wait_for_url(url_pattern, timeout=timeout)
    
    def get_current_url(self) -> str:
        """获取当前URL"""
        return self.page.url
    
    def scroll_to_element(self, selector: str):
        """滚动到元素"""
        element = self.get_element(selector)
        element.scroll_into_view_if_needed()
    
    def take_screenshot(self, path: str = None) -> bytes:
        """截图"""
        if path:
            return self.page.screenshot(path=path)
        else:
            return self.page.screenshot()
    
    def wait_for_timeout(self, timeout: int):
        """等待指定时间（毫秒）"""
        self.page.wait_for_timeout(timeout)
    
    def get_element_attribute(self, selector: str, attribute: str) -> str:
        """获取元素属性"""
        element = self.get_element(selector)
        return element.get_attribute(attribute)
    
    def is_checked(self, selector: str) -> bool:
        """检查复选框是否选中"""
        element = self.get_element(selector)
        return element.is_checked()
    
    def check_element(self, selector: str):
        """勾选复选框"""
        element = self.get_element(selector)
        if not element.is_checked():
            element.check()
    
    def uncheck_element(self, selector: str):
        """取消勾选复选框"""
        element = self.get_element(selector)
        if element.is_checked():
            element.uncheck()
    
    def get_page_title(self) -> str:
        """获取页面标题"""
        return self.page.title()
    
    def refresh_page(self):
        """刷新页面"""
        self.page.reload()
    
    def go_back(self):
        """返回上一页"""
        self.page.go_back()
    
    def go_forward(self):
        """前进到下一页"""
        self.page.go_forward()
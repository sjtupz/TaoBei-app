"""
用户管理页面的Page Object Model
"""
import time
from playwright.sync_api import Page, expect, Locator
from utils.config import Config


class UserManagementPage:
    """用户管理页面对象"""
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = Config.BASE_URL
        
        # 页面元素定位器
        self.profile_form = '[data-testid="user-profile-form"]'
        self.nickname_input = '[data-testid="nickname-input"]'
        self.avatar_url_input = '[data-testid="avatar-url-input"]'
        self.save_button = '[data-testid="save-button"]'
        self.logout_button = '[data-testid="logout-button"]'
        self.success_message = '[data-testid="success-message"]'
        self.error_message = '[data-testid="error-message"]'
        self.loading_spinner = '[data-testid="loading-spinner"]'
        
        # 显示元素定位器
        self.displayed_nickname = '[data-testid="displayed-nickname"]'
        self.displayed_avatar = '[data-testid="displayed-avatar"]'
        self.user_avatar_image = '[data-testid="user-avatar-image"]'
        
        # 表单验证元素
        self.nickname_error = '[data-testid="nickname-error"]'
        self.avatar_url_error = '[data-testid="avatar-url-error"]'
        
        # 页面标题和导航
        self.page_title = '[data-testid="page-title"]'
        self.breadcrumb = '[data-testid="breadcrumb"]'
        
        # 确认对话框
        self.confirm_dialog = '[data-testid="confirm-dialog"]'
        self.confirm_yes_button = '[data-testid="confirm-yes"]'
        self.confirm_no_button = '[data-testid="confirm-no"]'
    
    def navigate_to_profile_page(self):
        """导航到用户信息页面"""
        profile_url = f"{self.base_url}/profile"
        self.page.goto(profile_url)
        self.wait_for_page_load()
    
    def wait_for_page_load(self):
        """等待页面加载完成"""
        # 等待主要内容加载
        try:
            self.page.wait_for_selector(self.profile_form, timeout=10000)
        except:
            # 如果没有找到表单，可能是被重定向到登录页面
            pass
        
        # 等待加载动画消失
        try:
            self.page.wait_for_selector(self.loading_spinner, state="hidden", timeout=5000)
        except:
            pass
    
    def enter_nickname(self, nickname: str):
        """输入昵称"""
        nickname_field = self.page.locator(self.nickname_input)
        nickname_field.clear()
        nickname_field.fill(nickname)
    
    def enter_avatar_url(self, avatar_url: str):
        """输入头像URL"""
        avatar_field = self.page.locator(self.avatar_url_input)
        avatar_field.clear()
        avatar_field.fill(avatar_url)
    
    def clear_nickname(self):
        """清空昵称输入框"""
        nickname_field = self.page.locator(self.nickname_input)
        nickname_field.clear()
    
    def clear_avatar_url(self):
        """清空头像URL输入框"""
        avatar_field = self.page.locator(self.avatar_url_input)
        avatar_field.clear()
    
    def click_save_button(self):
        """点击保存按钮"""
        save_btn = self.page.locator(self.save_button)
        save_btn.click()
        
        # 等待请求完成
        self.wait_for_save_completion()
    
    def wait_for_save_completion(self):
        """等待保存操作完成"""
        # 等待加载状态消失
        try:
            self.page.wait_for_selector(self.loading_spinner, state="hidden", timeout=10000)
        except:
            pass
        
        # 等待成功或错误消息出现
        try:
            self.page.wait_for_selector(f"{self.success_message}, {self.error_message}", timeout=5000)
        except:
            pass
    
    def click_logout_button(self):
        """点击退出登录按钮"""
        logout_btn = self.page.locator(self.logout_button)
        logout_btn.click()
        
        # 处理可能的确认对话框
        self.handle_logout_confirmation()
        
        # 等待页面跳转
        time.sleep(1)
    
    def handle_logout_confirmation(self):
        """处理退出登录确认对话框"""
        try:
            # 等待确认对话框出现
            self.page.wait_for_selector(self.confirm_dialog, timeout=3000)
            
            # 点击确认按钮
            confirm_btn = self.page.locator(self.confirm_yes_button)
            confirm_btn.click()
        except:
            # 如果没有确认对话框，直接继续
            pass
    
    def get_success_message(self) -> str:
        """获取成功提示消息"""
        try:
            success_element = self.page.locator(self.success_message)
            success_element.wait_for(state="visible", timeout=5000)
            return success_element.text_content() or ""
        except:
            return ""
    
    def get_error_message(self) -> str:
        """获取错误提示消息"""
        try:
            # 尝试获取通用错误消息
            error_element = self.page.locator(self.error_message)
            if error_element.is_visible():
                return error_element.text_content() or ""
            
            # 尝试获取字段特定的错误消息
            nickname_error = self.page.locator(self.nickname_error)
            if nickname_error.is_visible():
                return nickname_error.text_content() or ""
            
            avatar_error = self.page.locator(self.avatar_url_error)
            if avatar_error.is_visible():
                return avatar_error.text_content() or ""
            
            return ""
        except:
            return ""
    
    def get_displayed_nickname(self) -> str:
        """获取页面显示的昵称"""
        try:
            nickname_element = self.page.locator(self.displayed_nickname)
            return nickname_element.text_content() or ""
        except:
            # 如果没有专门的显示元素，尝试从输入框获取
            try:
                nickname_input = self.page.locator(self.nickname_input)
                return nickname_input.input_value() or ""
            except:
                return ""
    
    def get_displayed_avatar_url(self) -> str:
        """获取页面显示的头像URL"""
        try:
            # 尝试从头像图片元素获取src属性
            avatar_img = self.page.locator(self.user_avatar_image)
            return avatar_img.get_attribute("src") or ""
        except:
            # 如果没有图片元素，尝试从输入框获取
            try:
                avatar_input = self.page.locator(self.avatar_url_input)
                return avatar_input.input_value() or ""
            except:
                return ""
    
    def get_current_nickname_value(self) -> str:
        """获取昵称输入框当前值"""
        try:
            nickname_input = self.page.locator(self.nickname_input)
            return nickname_input.input_value() or ""
        except:
            return ""
    
    def get_current_avatar_url_value(self) -> str:
        """获取头像URL输入框当前值"""
        try:
            avatar_input = self.page.locator(self.avatar_url_input)
            return avatar_input.input_value() or ""
        except:
            return ""
    
    def is_save_button_enabled(self) -> bool:
        """检查保存按钮是否可用"""
        try:
            save_btn = self.page.locator(self.save_button)
            return save_btn.is_enabled()
        except:
            return False
    
    def is_save_button_loading(self) -> bool:
        """检查保存按钮是否处于加载状态"""
        try:
            save_btn = self.page.locator(self.save_button)
            # 检查按钮是否包含加载类名或属性
            return save_btn.get_attribute("disabled") is not None or "loading" in (save_btn.get_attribute("class") or "")
        except:
            return False
    
    def wait_for_nickname_validation(self):
        """等待昵称验证完成"""
        try:
            # 等待验证消息出现或消失
            self.page.wait_for_timeout(1000)  # 给验证一些时间
        except:
            pass
    
    def wait_for_avatar_url_validation(self):
        """等待头像URL验证完成"""
        try:
            # 等待验证消息出现或消失
            self.page.wait_for_timeout(1000)  # 给验证一些时间
        except:
            pass
    
    def get_page_title(self) -> str:
        """获取页面标题"""
        try:
            title_element = self.page.locator(self.page_title)
            return title_element.text_content() or ""
        except:
            return self.page.title()
    
    def is_profile_form_visible(self) -> bool:
        """检查用户信息表单是否可见"""
        try:
            form_element = self.page.locator(self.profile_form)
            return form_element.is_visible()
        except:
            return False
    
    def is_logout_button_visible(self) -> bool:
        """检查退出登录按钮是否可见"""
        try:
            logout_btn = self.page.locator(self.logout_button)
            return logout_btn.is_visible()
        except:
            return False
    
    def get_form_validation_errors(self) -> dict:
        """获取表单验证错误信息"""
        errors = {}
        
        try:
            nickname_error = self.page.locator(self.nickname_error)
            if nickname_error.is_visible():
                errors["nickname"] = nickname_error.text_content() or ""
        except:
            pass
        
        try:
            avatar_error = self.page.locator(self.avatar_url_error)
            if avatar_error.is_visible():
                errors["avatar"] = avatar_error.text_content() or ""
        except:
            pass
        
        return errors
    
    def fill_user_form(self, nickname: str = None, avatar_url: str = None):
        """填写用户信息表单"""
        if nickname is not None:
            self.enter_nickname(nickname)
            self.wait_for_nickname_validation()
        
        if avatar_url is not None:
            self.enter_avatar_url(avatar_url)
            self.wait_for_avatar_url_validation()
    
    def submit_user_form(self):
        """提交用户信息表单"""
        self.click_save_button()
    
    def reset_form(self):
        """重置表单"""
        try:
            # 如果有重置按钮
            reset_btn = self.page.locator('[data-testid="reset-button"]')
            if reset_btn.is_visible():
                reset_btn.click()
            else:
                # 手动清空字段
                self.clear_nickname()
                self.clear_avatar_url()
        except:
            # 手动清空字段
            self.clear_nickname()
            self.clear_avatar_url()
    
    def wait_for_redirect_to_login(self):
        """等待重定向到登录页面"""
        try:
            login_url_pattern = f"{self.base_url}/login"
            self.page.wait_for_url(login_url_pattern, timeout=10000)
        except:
            pass
    
    def is_on_login_page(self) -> bool:
        """检查是否在登录页面"""
        current_url = self.page.url
        return "/login" in current_url
    
    def get_current_url(self) -> str:
        """获取当前页面URL"""
        return self.page.url
    
    def refresh_page(self):
        """刷新页面"""
        self.page.reload()
        self.wait_for_page_load()
    
    def go_back(self):
        """返回上一页"""
        self.page.go_back()
        self.wait_for_page_load()
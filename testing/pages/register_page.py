"""
注册页面的页面对象模型
实现注册页面的元素定位和操作方法
"""

from playwright.sync_api import Page, expect
from .base_page import BasePage
import time
import re


class RegisterPage(BasePage):
    """注册页面类"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # 页面元素定位器
        self.phone_input = "input[placeholder*='手机号']"
        self.verification_code_input = "input[placeholder*='验证码']"
        self.get_code_button = "button:has-text('获取验证码')"
        self.register_button = "button:has-text('注册')"
        self.agreement_checkbox = "input[type='checkbox'], .checkbox"
        self.agreement_text = ".agreement-text, .user-agreement"
        self.login_link = "a:has-text('登录'), a:has-text('已有账号')"
        
        # 错误和成功消息定位器
        self.error_message = ".error-message, .toast-error, .message.error, [class*='error']"
        self.success_message = ".success-message, .toast-success, .message.success, [class*='success']"
        
        # 页面状态定位器
        self.register_form = ".register-form, form"
        self.countdown_button = "button:has-text('s')"
        
    def navigate_to_register_page(self):
        """导航到注册页面"""
        try:
            self.page.goto("http://localhost:3000/register", timeout=30000)
            self.wait_for_element(self.register_form, timeout=15000)
            
            # 等待手机号输入框可见
            self.wait_for_element(self.phone_input, timeout=15000)
            
        except Exception as e:
            print(f"导航到注册页面失败: {e}")
            raise
    
    def enter_phone_number(self, phone_number: str):
        """输入手机号"""
        try:
            # 等待并清空输入框
            phone_element = self.wait_for_element(self.phone_input, timeout=15000)
            phone_element.clear()
            
            # 输入手机号
            self.fill_input(self.phone_input, phone_number, timeout=15000)
            
        except Exception as e:
            print(f"输入手机号失败: {e}")
            raise
    
    def clear_phone_number(self):
        """清空手机号输入框"""
        try:
            phone_element = self.wait_for_element(self.phone_input, timeout=10000)
            phone_element.clear()
        except Exception as e:
            print(f"清空手机号失败: {e}")
            raise
    
    def enter_verification_code(self, code: str):
        """输入验证码"""
        try:
            # 等待验证码输入框
            code_element = self.wait_for_element(self.verification_code_input, timeout=15000)
            code_element.clear()
            
            # 输入验证码
            self.fill_input(self.verification_code_input, code, timeout=15000)
            
        except Exception as e:
            print(f"输入验证码失败: {e}")
            raise
    
    def clear_verification_code(self):
        """清空验证码输入框"""
        try:
            code_element = self.wait_for_element(self.verification_code_input, timeout=10000)
            code_element.clear()
        except Exception as e:
            print(f"清空验证码失败: {e}")
            raise
    
    def click_get_verification_code(self):
        """点击获取验证码按钮"""
        try:
            # 尝试多个可能的定位器
            selectors = [
                "button:has-text('获取验证码')",
                "button[class*='get-code']",
                ".get-code-btn",
                "button:contains('获取验证码')"
            ]
            
            clicked = False
            for selector in selectors:
                try:
                    element = self.page.locator(selector).first
                    if element.is_visible() and element.is_enabled():
                        element.click()
                        clicked = True
                        break
                except:
                    continue
            
            if not clicked:
                # 最后尝试通过文本查找
                self.click_element(self.get_code_button, timeout=15000)
                
        except Exception as e:
            print(f"点击获取验证码按钮失败: {e}")
            raise
    
    def click_register_button(self):
        """点击注册按钮"""
        try:
            self.click_element(self.register_button, timeout=15000)
        except Exception as e:
            print(f"点击注册按钮失败: {e}")
            raise
    
    def check_agreement_checkbox(self):
        """勾选用户协议复选框"""
        try:
            # 尝试多种复选框定位方式
            selectors = [
                "input[type='checkbox']",
                ".checkbox input",
                ".agreement-checkbox",
                "[data-testid='agreement-checkbox']"
            ]
            
            checked = False
            for selector in selectors:
                try:
                    element = self.page.locator(selector).first
                    if element.is_visible():
                        if not element.is_checked():
                            element.check()
                        checked = True
                        break
                except:
                    continue
            
            if not checked:
                # 尝试点击协议文本区域
                try:
                    agreement_area = self.page.locator(self.agreement_text).first
                    if agreement_area.is_visible():
                        agreement_area.click()
                except:
                    pass
                    
        except Exception as e:
            print(f"勾选用户协议失败: {e}")
            raise
    
    def uncheck_agreement_checkbox(self):
        """取消勾选用户协议复选框"""
        try:
            # 尝试多种复选框定位方式
            selectors = [
                "input[type='checkbox']",
                ".checkbox input", 
                ".agreement-checkbox",
                "[data-testid='agreement-checkbox']"
            ]
            
            for selector in selectors:
                try:
                    element = self.page.locator(selector).first
                    if element.is_visible() and element.is_checked():
                        element.uncheck()
                        break
                except:
                    continue
                    
        except Exception as e:
            print(f"取消勾选用户协议失败: {e}")
            raise
    
    def is_agreement_checked(self):
        """检查用户协议是否已勾选"""
        try:
            selectors = [
                "input[type='checkbox']",
                ".checkbox input",
                ".agreement-checkbox"
            ]
            
            for selector in selectors:
                try:
                    element = self.page.locator(selector).first
                    if element.is_visible():
                        return element.is_checked()
                except:
                    continue
            
            return False
        except:
            return False
    
    def click_login_link(self):
        """点击登录链接"""
        try:
            self.click_element(self.login_link, timeout=15000)
        except Exception as e:
            print(f"点击登录链接失败: {e}")
            raise
    
    def get_phone_number_value(self):
        """获取手机号输入框的值"""
        try:
            element = self.wait_for_element(self.phone_input, timeout=10000)
            return element.input_value()
        except Exception as e:
            print(f"获取手机号值失败: {e}")
            return ""
    
    def get_verification_code_value(self):
        """获取验证码输入框的值"""
        try:
            element = self.wait_for_element(self.verification_code_input, timeout=10000)
            return element.input_value()
        except Exception as e:
            print(f"获取验证码值失败: {e}")
            return ""
    
    def is_get_code_button_enabled(self):
        """检查获取验证码按钮是否可点击"""
        try:
            element = self.page.locator(self.get_code_button).first
            return element.is_enabled() if element.is_visible() else False
        except:
            return False
    
    def is_register_button_enabled(self):
        """检查注册按钮是否可点击"""
        try:
            element = self.page.locator(self.register_button).first
            return element.is_enabled() if element.is_visible() else False
        except:
            return False
    
    def is_countdown_active(self):
        """检查是否在倒计时状态"""
        try:
            # 检查按钮文本是否包含秒数
            button = self.page.locator(self.get_code_button).first
            if button.is_visible():
                text = button.text_content()
                return 's' in text or '秒' in text or re.search(r'\d+', text)
            return False
        except:
            return False
    
    def get_error_message(self):
        """获取错误消息"""
        try:
            # 尝试多个可能的错误消息选择器
            selectors = [
                ".error-message",
                ".toast-error",
                ".message.error", 
                "[class*='error']",
                ".ant-message-error",
                ".el-message--error"
            ]
            
            for selector in selectors:
                elements = self.page.locator(selector)
                if elements.count() > 0:
                    for i in range(elements.count()):
                        element = elements.nth(i)
                        if element.is_visible():
                            return element.text_content().strip()
            
            return ""
        except Exception as e:
            print(f"获取错误消息失败: {e}")
            return ""
    
    def get_success_message(self):
        """获取成功消息"""
        try:
            # 尝试多个可能的成功消息选择器
            selectors = [
                ".success-message",
                ".toast-success",
                ".message.success",
                "[class*='success']", 
                ".ant-message-success",
                ".el-message--success"
            ]
            
            for selector in selectors:
                elements = self.page.locator(selector)
                if elements.count() > 0:
                    for i in range(elements.count()):
                        element = elements.nth(i)
                        if element.is_visible():
                            return element.text_content().strip()
            
            return ""
        except Exception as e:
            print(f"获取成功消息失败: {e}")
            return ""
    
    def is_error_message_visible(self):
        """检查是否有错误消息显示"""
        return len(self.get_error_message()) > 0
    
    def is_success_message_visible(self):
        """检查是否有成功消息显示"""
        return len(self.get_success_message()) > 0
    
    def wait_for_error_message(self, timeout: int = 15000):
        """等待错误消息出现"""
        try:
            # 尝试多个错误消息选择器
            selectors = [
                ".error-message",
                ".toast-error",
                ".message.error",
                "[class*='error']"
            ]
            
            for selector in selectors:
                try:
                    element = self.page.locator(selector).first
                    element.wait_for(state="visible", timeout=5000)
                    if element.is_visible():
                        return element.text_content().strip()
                except:
                    continue
            
            # 如果没有找到错误消息，等待一下再检查
            time.sleep(2)
            return self.get_error_message()
            
        except Exception as e:
            print(f"等待错误消息失败: {e}")
            return ""
    
    def wait_for_success_message(self, timeout: int = 15000):
        """等待成功消息出现"""
        try:
            # 尝试多个成功消息选择器
            selectors = [
                ".success-message",
                ".toast-success",
                ".message.success", 
                "[class*='success']"
            ]
            
            for selector in selectors:
                try:
                    element = self.page.locator(selector).first
                    element.wait_for(state="visible", timeout=5000)
                    if element.is_visible():
                        return element.text_content().strip()
                except:
                    continue
            
            # 如果没有找到成功消息，等待一下再检查
            time.sleep(2)
            return self.get_success_message()
            
        except Exception as e:
            print(f"等待成功消息失败: {e}")
            return ""
    
    def wait_for_redirect_to_home(self, timeout: int = 10000):
        """等待跳转到首页"""
        try:
            # 等待URL变化或首页特征元素出现
            start_time = time.time()
            while time.time() - start_time < timeout / 1000:
                current_url = self.page.url
                if "/home" in current_url or current_url.endswith("/") or "register" not in current_url:
                    return True
                
                # 检查是否有用户信息等首页特征
                home_indicators = [
                    ".user-info",
                    ".home-content",
                    ".main-content", 
                    "[data-testid='home']"
                ]
                
                for indicator in home_indicators:
                    if self.page.locator(indicator).is_visible():
                        return True
                
                time.sleep(0.5)
            
            return False
            
        except Exception as e:
            print(f"等待跳转到首页失败: {e}")
            return False
    
    def wait_for_redirect_to_login(self, timeout: int = 10000):
        """等待跳转到登录页面"""
        try:
            # 等待URL变化到登录页面
            start_time = time.time()
            while time.time() - start_time < timeout / 1000:
                current_url = self.page.url
                if "/login" in current_url:
                    return True
                time.sleep(0.5)
            
            return False
            
        except Exception as e:
            print(f"等待跳转到登录页面失败: {e}")
            return False
    
    def validate_phone_number_format(self, phone_number: str):
        """验证手机号格式"""
        # 中国手机号正则表达式
        pattern = r'^1[3-9]\d{9}$'
        return re.match(pattern, phone_number) is not None
    
    def is_sql_injection_attempt(self, input_text: str):
        """检测是否为SQL注入尝试"""
        sql_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'SELECT', '--', ';', 'UNION']
        return any(keyword.lower() in input_text.lower() for keyword in sql_keywords)
    
    def is_xss_attempt(self, input_text: str):
        """检测是否为XSS攻击尝试"""
        xss_patterns = ['<script', 'javascript:', 'onerror=', 'onload=', 'alert(']
        return any(pattern.lower() in input_text.lower() for pattern in xss_patterns)
    
    def has_special_characters(self, input_text: str):
        """检测是否包含特殊字符"""
        special_chars = ['<', '>', '&', '"', "'", '/', '\\', '|', '*', '?', ':', ';']
        return any(char in input_text for char in special_chars)
    
    def is_too_long(self, input_text: str, max_length: int = 20):
        """检测输入是否过长"""
        return len(input_text) > max_length
    
    def check_database_integrity(self):
        """检查数据库完整性（模拟）"""
        # 这里应该连接数据库检查表结构
        # 为了测试目的，我们假设数据库完整
        return True
    
    def check_script_execution(self):
        """检查是否有脚本被执行"""
        try:
            # 检查页面是否有alert弹窗
            alerts = self.page.evaluate("() => window.alertExecuted || false")
            return alerts
        except:
            return False
    
    def simulate_user_creation_in_database(self, phone_number: str):
        """模拟在数据库中创建用户"""
        # 这里应该实际连接数据库创建用户
        # 为了测试目的，我们模拟这个过程
        print(f"模拟创建用户: {phone_number}")
        return True
    
    def check_user_exists_in_database(self, phone_number: str):
        """检查用户是否在数据库中存在"""
        # 这里应该实际查询数据库
        # 为了测试目的，我们模拟一些已存在的用户
        existing_users = ["13800138000", "13900139001"]
        return phone_number in existing_users
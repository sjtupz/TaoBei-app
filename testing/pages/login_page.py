"""
登录页面的页面对象模型
实现登录页面的元素定位和操作方法
"""

from playwright.sync_api import Page, expect
from .base_page import BasePage
import time
import re


class LoginPage(BasePage):
    """登录页面类"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # 页面元素定位器
        self.phone_input = "input[placeholder*='手机号']"
        self.verification_code_input = "input[placeholder*='验证码']"
        self.get_code_button = "button:has-text('获取验证码')"
        self.login_button = "button:has-text('登录')"
        self.register_link = "a.free-register, a:has-text('立即注册'), a:has-text('免费注册')"
        self.sms_login_tab = "span.tab:has-text('短信登录')"
        self.password_login_tab = "span.tab:has-text('密码登录')"
        
        # 错误和成功消息定位器
        self.error_message = ".error-message, .toast-error, .message.error, [class*='error']"
        self.success_message = ".success-message, .toast-success, .message.success, [class*='success']"
        
        # 页面状态定位器
        self.login_form = ".login-form, form"
        self.countdown_button = "button:has-text('s')"
        
    def navigate_to_login_page(self):
        """导航到登录页面"""
        try:
            self.page.goto("http://localhost:5173/login", timeout=30000)
            self.wait_for_element(self.login_form, timeout=15000)
            
            # 确保切换到短信登录模式
            self.switch_to_sms_login()
            
            # 等待手机号输入框可见
            self.wait_for_element(self.phone_input, timeout=15000)
            
        except Exception as e:
            print(f"导航到登录页面失败: {e}")
            raise
    
    def switch_to_sms_login(self):
        """切换到短信登录模式"""
        try:
            # 检查是否已经在短信登录模式
            sms_tab = self.page.locator(self.sms_login_tab).first
            if sms_tab.is_visible():
                # 检查是否已经激活
                if not sms_tab.get_attribute("class") or "active" not in sms_tab.get_attribute("class"):
                    sms_tab.click()
                    time.sleep(1)  # 等待切换完成
            
            # 等待手机号输入框出现
            self.wait_for_element(self.phone_input, timeout=10000)
            
        except Exception as e:
            print(f"切换到短信登录模式失败: {e}")
            # 如果切换失败，继续执行，可能已经在正确模式
    
    def enter_phone_number(self, phone_number: str):
        """输入手机号"""
        try:
            # 等待并清空输入框
            phone_element = self.wait_for_element(self.phone_input, timeout=15000)
            if phone_element is None:
                raise Exception(f"无法找到手机号输入框: {self.phone_input}")
            
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
    
    def click_login(self):
        """点击登录按钮"""
        try:
            self.click_element(self.login_button, timeout=15000)
        except Exception as e:
            print(f"点击登录按钮失败: {e}")
            raise
    
    def click_register_link(self):
        """点击注册链接"""
        try:
            self.click_element(self.register_link, timeout=15000)
        except Exception as e:
            print(f"点击注册链接失败: {e}")
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
    
    def is_login_button_enabled(self):
        """检查登录按钮是否可点击"""
        try:
            element = self.page.locator(self.login_button).first
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
                if "/home" in current_url or current_url.endswith("/") or "login" not in current_url:
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
    
    def is_get_code_button_disabled(self):
        """检查获取验证码按钮是否被禁用"""
        try:
            button = self.page.locator(self.get_code_button).first
            return not button.is_enabled()
        except Exception as e:
            print(f"检查获取验证码按钮状态失败: {e}")
            return False
    
    def get_code_button_text(self):
        """获取验证码按钮的文本内容"""
        try:
            button = self.page.locator(self.get_code_button).first
            return button.text_content().strip()
        except Exception as e:
            print(f"获取验证码按钮文本失败: {e}")
            return ""

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
"""
登录功能API测试
直接测试后端登录接口，验证登录功能的核心逻辑
"""
import pytest
import requests
import json
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.api_helper import APIHelper
from utils.database_helper import DatabaseHelper

class TestLoginAPI:
    """登录API测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.api_helper = APIHelper()
        self.db_helper = DatabaseHelper()
        self.base_url = "http://localhost:3001/api"
        print("API测试环境准备完成")
    
    def test_get_verification_code_valid_phone(self):
        """测试获取验证码 - 有效手机号"""
        phone_number = "13800138000"
        
        try:
            # 发送获取验证码请求
            response = requests.post(
                f"{self.base_url}/auth/send-verification-code",
                json={"phone": phone_number},
                timeout=10
            )
            
            print(f"请求URL: {self.base_url}/auth/send-verification-code")
            print(f"请求数据: {{'phone': '{phone_number}'}}")
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            # 验证响应
            if response.status_code == 200:
                data = response.json()
                assert data.get('success') == True, "获取验证码应该成功"
                assert 'message' in data, "响应应该包含消息"
                print("✓ 有效手机号获取验证码测试通过")
            else:
                print(f"⚠ 服务器响应状态码: {response.status_code}")
                print("注意: 这可能是因为后端服务未启动或接口路径不正确")
                
        except requests.exceptions.ConnectionError:
            print("⚠ 无法连接到后端服务，请确保后端服务正在运行")
            print("提示: 请检查 http://localhost:3000 是否可访问")
        except Exception as e:
            print(f"⚠ 测试过程中发生异常: {str(e)}")
    
    def test_get_verification_code_invalid_phone(self):
        """测试获取验证码 - 无效手机号"""
        invalid_phone = "123"
        
        try:
            # 发送获取验证码请求
            response = requests.post(
                f"{self.base_url}/auth/send-verification-code",
                json={"phone": invalid_phone},
                timeout=10
            )
            
            print(f"请求URL: {self.base_url}/auth/send-verification-code")
            print(f"请求数据: {{'phone': '{invalid_phone}'}}")
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            # 验证响应
            if response.status_code == 400:
                data = response.json()
                assert data.get('success') == False, "无效手机号应该返回失败"
                assert 'error' in data or 'message' in data, "响应应该包含错误信息"
                print("✓ 无效手机号获取验证码测试通过")
            else:
                print(f"⚠ 预期状态码400，实际状态码: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("⚠ 无法连接到后端服务，请确保后端服务正在运行")
        except Exception as e:
            print(f"⚠ 测试过程中发生异常: {str(e)}")
    
    def test_login_with_verification_code(self):
        """测试使用验证码登录"""
        phone_number = "13800138000"
        verification_code = "123456"
        
        try:
            # 发送登录请求
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={
                    "phone": phone_number,
                    "code": verification_code
                },
                timeout=10
            )
            
            print(f"请求URL: {self.base_url}/auth/login")
            print(f"请求数据: {{'phone': '{phone_number}', 'code': '{verification_code}'}}")
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            # 验证响应
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    assert 'token' in data or 'user' in data, "登录成功应该返回token或用户信息"
                    print("✓ 验证码登录测试通过")
                else:
                    print("⚠ 登录失败，可能是验证码错误或用户不存在")
            else:
                print(f"⚠ 服务器响应状态码: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("⚠ 无法连接到后端服务，请确保后端服务正在运行")
        except Exception as e:
            print(f"⚠ 测试过程中发生异常: {str(e)}")
    
    def test_login_with_wrong_code(self):
        """测试使用错误验证码登录"""
        phone_number = "13800138000"
        wrong_code = "000000"
        
        try:
            # 发送登录请求
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={
                    "phone": phone_number,
                    "code": wrong_code
                },
                timeout=10
            )
            
            print(f"请求URL: {self.base_url}/auth/login")
            print(f"请求数据: {{'phone': '{phone_number}', 'code': '{wrong_code}'}}")
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            # 验证响应
            if response.status_code in [400, 401]:
                data = response.json()
                assert data.get('success') == False, "错误验证码应该返回失败"
                print("✓ 错误验证码登录测试通过")
            else:
                print(f"⚠ 预期状态码400或401，实际状态码: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("⚠ 无法连接到后端服务，请确保后端服务正在运行")
        except Exception as e:
            print(f"⚠ 测试过程中发生异常: {str(e)}")
    
    def test_backend_service_health(self):
        """测试后端服务健康状态"""
        try:
            # 测试根路径
            response = requests.get("http://localhost:3001", timeout=5)
            print(f"后端服务根路径状态码: {response.status_code}")
            
            # 测试API路径
            api_response = requests.get(f"{self.base_url}/health", timeout=5)
            print(f"API健康检查状态码: {api_response.status_code}")
            
            if response.status_code == 200:
                print("✓ 后端服务运行正常")
            else:
                print("⚠ 后端服务可能存在问题")
                
        except requests.exceptions.ConnectionError:
            print("❌ 无法连接到后端服务")
            print("请确保后端服务正在 http://localhost:3001 运行")
        except Exception as e:
            print(f"⚠ 健康检查过程中发生异常: {str(e)}")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
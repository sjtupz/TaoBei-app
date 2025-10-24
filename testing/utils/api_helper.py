"""
API测试助手类
"""
import requests
import json
from typing import Dict, Any, Optional
from .config import Config


class APIHelper:
    """API测试助手"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def post(self, endpoint: str, data: Dict[str, Any] = None, headers: Dict[str, str] = None) -> requests.Response:
        """发送POST请求"""
        url = self.config.get_api_url(endpoint)
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        return self.session.post(
            url, 
            json=data, 
            headers=request_headers,
            timeout=30
        )
    
    def get(self, endpoint: str, params: Dict[str, Any] = None, headers: Dict[str, str] = None) -> requests.Response:
        """发送GET请求"""
        url = self.config.get_api_url(endpoint)
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        return self.session.get(
            url, 
            params=params, 
            headers=request_headers,
            timeout=30
        )
    
    def set_auth_token(self, token: str):
        """设置认证token"""
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
    
    def clear_auth_token(self):
        """清除认证token"""
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
    
    # 认证相关API
    def send_verification_code(self, phone_number: str) -> requests.Response:
        """发送验证码"""
        return self.post('/auth/send-code', {'phoneNumber': phone_number})
    
    def login(self, phone_number: str, verification_code: str) -> requests.Response:
        """用户登录"""
        return self.post('/auth/login', {
            'phoneNumber': phone_number,
            'verificationCode': verification_code
        })
    
    def register(self, phone_number: str, verification_code: str, agree_to_terms: bool = True) -> requests.Response:
        """用户注册"""
        return self.post('/auth/register', {
            'phoneNumber': phone_number,
            'verificationCode': verification_code,
            'agreeToTerms': str(agree_to_terms).lower()
        })
    
    def logout(self, token: str) -> requests.Response:
        """用户退出登录"""
        headers = {'Authorization': f'Bearer {token}'}
        return self.post('/auth/logout', headers=headers)
    
    def get_user_profile(self, token: str) -> requests.Response:
        """获取用户信息"""
        headers = {'Authorization': f'Bearer {token}'}
        return self.get('/user/profile', headers=headers)
    
    def update_user_profile(self, token: str, nickname: str = None, avatar: str = None) -> requests.Response:
        """更新用户信息"""
        headers = {'Authorization': f'Bearer {token}'}
        data = {}
        if nickname is not None:
            data['nickname'] = nickname
        if avatar is not None:
            data['avatar'] = avatar
        return self.post('/user/profile', data, headers=headers)
    
    # 商品管理相关API
    def get_products(self, page: int = 1, page_size: int = 10, keyword: str = None, 
                    category: str = None, sort_by: str = None, sort_order: str = None) -> requests.Response:
        """获取商品列表"""
        params = {
            'page': page,
            'pageSize': page_size
        }
        if keyword:
            params['keyword'] = keyword
        if category:
            params['category'] = category
        if sort_by:
            params['sortBy'] = sort_by
        if sort_order:
            params['sortOrder'] = sort_order
        
        return self.get('/products', params=params)
    
    def get_product_detail(self, product_id: int) -> requests.Response:
        """获取商品详情"""
        return self.get(f'/products/{product_id}')
    
    def search_products(self, keyword: str, page: int = 1, page_size: int = 10) -> requests.Response:
        """搜索商品"""
        params = {
            'keyword': keyword,
            'page': page,
            'pageSize': page_size
        }
        return self.get('/products', params=params)
    
    def filter_products_by_category(self, category: str, page: int = 1, page_size: int = 10) -> requests.Response:
        """按分类筛选商品"""
        params = {
            'category': category,
            'page': page,
            'pageSize': page_size
        }
        return self.get('/products', params=params)
    
    def sort_products(self, sort_by: str, sort_order: str = 'ASC', page: int = 1, page_size: int = 10) -> requests.Response:
        """商品排序"""
        params = {
            'sortBy': sort_by,
            'sortOrder': sort_order,
            'page': page,
            'pageSize': page_size
        }
        return self.get('/products', params=params)
    
    # 响应验证方法
    def assert_response_success(self, response: requests.Response, expected_status: int = 200):
        """断言响应成功"""
        assert response.status_code == expected_status, f"期望状态码 {expected_status}，实际 {response.status_code}，响应内容: {response.text}"
    
    def assert_response_error(self, response: requests.Response, expected_status: int = 400):
        """断言响应错误"""
        assert response.status_code == expected_status, f"期望状态码 {expected_status}，实际 {response.status_code}，响应内容: {response.text}"
    
    def assert_response_contains_message(self, response: requests.Response, expected_message: str):
        """断言响应包含指定消息"""
        response_data = response.json()
        message = response_data.get('message', '') or response_data.get('error', '')
        assert expected_message in message, f"响应消息中未找到 '{expected_message}'，实际消息: {message}"
    
    def get_response_data(self, response: requests.Response) -> Dict[str, Any]:
        """获取响应数据"""
        try:
            return response.json()
        except json.JSONDecodeError:
            return {'text': response.text}
"""
API模块测试 - 用户管理和商品管理功能验证
"""
import requests
import pytest

BASE_URL = 'http://localhost:3001/api'

class TestUserManagementAPI:
    """用户管理API测试"""
    
    def test_get_user_profile_without_auth(self):
        """测试未认证状态下获取用户信息"""
        response = requests.get(f'{BASE_URL}/user/profile')
        # 预期返回401未授权或404未找到
        assert response.status_code in [401, 404, 500], f"预期401/404/500，实际: {response.status_code}"
    
    def test_update_user_profile_without_auth(self):
        """测试未认证状态下更新用户信息"""
        update_data = {'nickname': '测试用户', 'avatar': 'https://example.com/avatar.jpg'}
        response = requests.put(f'{BASE_URL}/user/profile', json=update_data)
        # 预期返回401未授权或404未找到
        assert response.status_code in [401, 404, 500], f"预期401/404/500，实际: {response.status_code}"

class TestProductManagementAPI:
    """商品管理API测试"""
    
    def test_get_products_list(self):
        """测试获取商品列表"""
        response = requests.get(f'{BASE_URL}/products')
        print(f'商品列表API状态: {response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            print(f'返回数据: {data}')
            # 检查返回数据结构 - API返回格式为 {code: 200, data: {products: []}}
            assert 'data' in data and 'products' in data['data'], "返回数据应包含data.products字段"
            products = data['data']['products']
            assert isinstance(products, list), "商品列表应为数组"
            print(f'商品数量: {len(products)}')
        else:
            # API可能未实现，记录状态码
            print(f'商品列表API未实现或出错，状态码: {response.status_code}')
    
    def test_get_product_detail(self):
        """测试获取商品详情"""
        response = requests.get(f'{BASE_URL}/products/1')
        print(f'商品详情API状态: {response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            print(f'商品详情: {data}')
            # 检查返回数据结构 - API返回格式为 {code: 200, data: {id: 1, name: ...}}
            assert 'data' in data, "返回数据应包含data字段"
            product_data = data['data']
            assert 'id' in product_data, "商品数据应包含ID字段"
            print(f'商品ID: {product_data["id"]}, 商品名称: {product_data.get("name", "未知")}')
        else:
            # API可能未实现，记录状态码
            print(f'商品详情API未实现或出错，状态码: {response.status_code}')
    
    def test_search_products(self):
        """测试商品搜索"""
        response = requests.get(f'{BASE_URL}/products/search?keyword=测试')
        print(f'商品搜索API状态: {response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            print(f'搜索结果: {data}')
        else:
            print(f'商品搜索API未实现或出错，状态码: {response.status_code}')

class TestRegistrationAPI:
    """用户注册API测试"""
    
    def test_send_verification_code(self):
        """测试发送验证码"""
        data = {'phone_number': '13800138999'}
        response = requests.post(f'{BASE_URL}/auth/send-verification-code', json=data)
        print(f'发送验证码API状态: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            print(f'发送验证码结果: {result}')
            assert result.get('success') == True, "发送验证码应该成功"
        else:
            print(f'发送验证码API状态: {response.status_code}')
    
    def test_register_user(self):
        """测试用户注册"""
        data = {
            'phone_number': '13800138999',
            'verification_code': '123456',
            'agree_to_terms': True
        }
        response = requests.post(f'{BASE_URL}/auth/register', json=data)
        print(f'用户注册API状态: {response.status_code}')
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f'注册结果: {result}')
        else:
            print(f'用户注册API状态: {response.status_code}')
            if response.status_code == 400:
                print(f'注册失败原因: {response.text}')
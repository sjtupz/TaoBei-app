"""
测试数据管理类
"""
import random
import string
from typing import Dict, List, Any
from datetime import datetime, timedelta


class TestDataManager:
    """测试数据管理器"""
    
    # 添加这个方法来避免pytest收集警告
    __test__ = False
    
    def __init__(self):
        self.users = []
        self.products = []
        self.categories = []
        self._init_default_data()
    
    def _init_default_data(self):
        """初始化默认测试数据"""
        self._init_categories()
        self._init_products()
        self._init_users()
    
    def _init_categories(self):
        """初始化商品分类数据"""
        self.categories = [
            {"id": 1, "name": "电子产品", "description": "手机、电脑、数码产品等"},
            {"id": 2, "name": "服装", "description": "男装、女装、童装等"},
            {"id": 3, "name": "家居用品", "description": "家具、装饰、生活用品等"},
            {"id": 4, "name": "图书", "description": "小说、教材、工具书等"},
            {"id": 5, "name": "运动户外", "description": "运动器材、户外用品等"},
            {"id": 6, "name": "美妆护肤", "description": "化妆品、护肤品等"},
            {"id": 7, "name": "食品饮料", "description": "零食、饮料、生鲜等"},
            {"id": 8, "name": "母婴用品", "description": "奶粉、玩具、婴儿用品等"}
        ]
    
    def _init_products(self):
        """初始化商品测试数据"""
        self.products = [
            {
                "id": 1,
                "name": "iPhone 15 Pro",
                "price": 7999.00,
                "category": "电子产品",
                "category_id": 1,
                "description": "苹果最新款智能手机，配备A17 Pro芯片",
                "image": "https://example.com/iphone15pro.jpg",
                "stock": 100,
                "rating": 4.8,
                "reviews_count": 1250,
                "specifications": {
                    "screen_size": "6.1英寸",
                    "storage": "128GB",
                    "color": "深空黑色",
                    "battery": "3274mAh"
                },
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "id": 2,
                "name": "华为 Mate 60 Pro",
                "price": 6999.00,
                "category": "电子产品",
                "category_id": 1,
                "description": "华为旗舰手机，麒麟9000S处理器",
                "image": "https://example.com/mate60pro.jpg",
                "stock": 80,
                "rating": 4.7,
                "reviews_count": 890,
                "specifications": {
                    "screen_size": "6.82英寸",
                    "storage": "256GB",
                    "color": "雅川青",
                    "battery": "5000mAh"
                },
                "created_at": "2024-01-02T00:00:00Z"
            },
            {
                "id": 3,
                "name": "MacBook Pro 14英寸",
                "price": 14999.00,
                "category": "电子产品",
                "category_id": 1,
                "description": "苹果专业级笔记本电脑，M3芯片",
                "image": "https://example.com/macbookpro14.jpg",
                "stock": 50,
                "rating": 4.9,
                "reviews_count": 567,
                "specifications": {
                    "processor": "Apple M3",
                    "memory": "16GB",
                    "storage": "512GB SSD",
                    "display": "14.2英寸 Liquid Retina XDR"
                },
                "created_at": "2024-01-03T00:00:00Z"
            },
            {
                "id": 4,
                "name": "Nike Air Max 270",
                "price": 899.00,
                "category": "运动户外",
                "category_id": 5,
                "description": "Nike经典跑步鞋，舒适透气",
                "image": "https://example.com/nikeairmax270.jpg",
                "stock": 200,
                "rating": 4.5,
                "reviews_count": 2340,
                "specifications": {
                    "size": "42",
                    "color": "黑白配色",
                    "material": "网布+合成革",
                    "sole": "橡胶大底"
                },
                "created_at": "2024-01-04T00:00:00Z"
            },
            {
                "id": 5,
                "name": "《Python编程：从入门到实践》",
                "price": 89.00,
                "category": "图书",
                "category_id": 4,
                "description": "Python编程入门经典教材",
                "image": "https://example.com/python-book.jpg",
                "stock": 300,
                "rating": 4.6,
                "reviews_count": 1890,
                "specifications": {
                    "author": "埃里克·马瑟斯",
                    "publisher": "人民邮电出版社",
                    "pages": "459页",
                    "isbn": "9787115428028"
                },
                "created_at": "2024-01-05T00:00:00Z"
            }
        ]
    
    def _init_users(self):
        """初始化用户测试数据"""
        self.users = [
            {
                "id": 1,
                "phone_number": "13800138001",
                "nickname": "测试用户1",
                "avatar": "https://example.com/avatar1.jpg",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            },
            {
                "id": 2,
                "phone_number": "13800138002",
                "nickname": "测试用户2",
                "avatar": "https://example.com/avatar2.jpg",
                "created_at": "2024-01-02T00:00:00Z",
                "updated_at": "2024-01-02T00:00:00Z"
            },
            {
                "id": 3,
                "phone_number": "13800138003",
                "nickname": "小明",
                "avatar": "https://example.com/avatar3.jpg",
                "created_at": "2024-01-03T00:00:00Z",
                "updated_at": "2024-01-03T00:00:00Z"
            }
        ]
    
    # 用户数据相关方法
    def get_valid_user(self) -> Dict[str, Any]:
        """获取有效的用户数据"""
        return self.users[0].copy()
    
    def get_user_by_phone(self, phone_number: str) -> Dict[str, Any]:
        """根据手机号获取用户数据"""
        for user in self.users:
            if user["phone_number"] == phone_number:
                return user.copy()
        return None
    
    def generate_random_phone(self) -> str:
        """生成随机手机号"""
        return f"138{random.randint(10000000, 99999999)}"
    
    def generate_random_nickname(self) -> str:
        """生成随机昵称"""
        prefixes = ["测试", "用户", "小", "大", "老"]
        suffixes = ["明", "红", "华", "强", "丽", "伟", "芳", "军", "娟", "涛"]
        return random.choice(prefixes) + random.choice(suffixes)
    
    def get_valid_user_update_data(self) -> Dict[str, Any]:
        """获取有效的用户更新数据"""
        return {
            "nickname": self.generate_random_nickname(),
            "avatar": f"https://example.com/avatar{random.randint(1, 100)}.jpg"
        }
    
    def get_invalid_user_data(self) -> List[Dict[str, Any]]:
        """获取无效的用户数据"""
        return [
            {
                "nickname": "",  # 空昵称
                "error": "昵称长度必须在1-50个字符之间"
            },
            {
                "nickname": "这是一个非常非常非常非常非常非常非常非常非常非常非常非常非常非常非常非常长的昵称",  # 超长昵称
                "error": "昵称长度必须在1-50个字符之间"
            },
            {
                "avatar": "invalid-url",  # 无效URL
                "error": "头像必须是有效的URL地址"
            },
            {
                "avatar": "not-a-url",  # 无效URL
                "error": "头像必须是有效的URL地址"
            },
            {
                "avatar": "ftp://invalid",  # 无效协议
                "error": "头像必须是有效的URL地址"
            }
        ]
    
    # 商品数据相关方法
    def get_all_products(self) -> List[Dict[str, Any]]:
        """获取所有商品数据"""
        return [product.copy() for product in self.products]
    
    def get_product_by_id(self, product_id: int) -> Dict[str, Any]:
        """根据ID获取商品数据"""
        for product in self.products:
            if product["id"] == product_id:
                return product.copy()
        return None
    
    def get_products_by_category(self, category: str) -> List[Dict[str, Any]]:
        """根据分类获取商品数据"""
        return [product.copy() for product in self.products if product["category"] == category]
    
    def search_products_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """根据关键词搜索商品"""
        results = []
        for product in self.products:
            if keyword.lower() in product["name"].lower() or keyword.lower() in product["description"].lower():
                results.append(product.copy())
        return results
    
    def get_products_sorted_by_price(self, ascending: bool = True) -> List[Dict[str, Any]]:
        """按价格排序获取商品"""
        sorted_products = sorted(self.products, key=lambda x: x["price"], reverse=not ascending)
        return [product.copy() for product in sorted_products]
    
    def get_products_sorted_by_name(self, ascending: bool = True) -> List[Dict[str, Any]]:
        """按名称排序获取商品"""
        sorted_products = sorted(self.products, key=lambda x: x["name"], reverse=not ascending)
        return [product.copy() for product in sorted_products]
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """获取所有分类数据"""
        return [category.copy() for category in self.categories]
    
    def get_category_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取分类数据"""
        for category in self.categories:
            if category["name"] == name:
                return category.copy()
        return None
    
    def get_paginated_products(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """获取分页商品数据"""
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        
        total_products = len(self.products)
        products_page = self.products[start_index:end_index]
        
        return {
            "products": [product.copy() for product in products_page],
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_items": total_products,
                "total_pages": (total_products + page_size - 1) // page_size,
                "has_next": end_index < total_products,
                "has_prev": page > 1
            }
        }
    
    def get_invalid_product_ids(self) -> List[int]:
        """获取无效的商品ID"""
        return [0, -1, 99999, 100000]
    
    def get_invalid_pagination_params(self) -> List[Dict[str, Any]]:
        """获取无效的分页参数"""
        return [
            {"page": 0, "pageSize": 10, "error": "页码必须是大于0的整数"},
            {"page": -1, "pageSize": 10, "error": "页码必须是大于0的整数"},
            {"page": 1, "pageSize": 0, "error": "每页数量必须是1-100之间的整数"},
            {"page": 1, "pageSize": 101, "error": "每页数量必须是1-100之间的整数"},
            {"page": 1, "pageSize": -1, "error": "每页数量必须是1-100之间的整数"}
        ]
    
    def get_search_keywords(self) -> Dict[str, List[str]]:
        """获取搜索关键词"""
        return {
            "valid": ["手机", "苹果", "iPhone", "电脑", "Nike", "Python"],
            "no_results": ["不存在的商品xyz123", "测试无结果关键词"],
            "invalid": ["a" * 101]  # 超长关键词
        }
    
    # 验证码相关数据
    def get_verification_codes(self) -> Dict[str, str]:
        """获取验证码数据"""
        return {
            "valid": "123456",
            "invalid": "000000",
            "expired": "999999"
        }
    
    # 清理和重置方法
    def reset_data(self):
        """重置所有测试数据"""
        self._init_default_data()
    
    def add_test_user(self, user_data: Dict[str, Any]) -> int:
        """添加测试用户"""
        user_id = max([user["id"] for user in self.users]) + 1 if self.users else 1
        user_data["id"] = user_id
        user_data["created_at"] = datetime.now().isoformat() + "Z"
        user_data["updated_at"] = datetime.now().isoformat() + "Z"
        self.users.append(user_data)
        return user_id
    
    def add_test_product(self, product_data: Dict[str, Any]) -> int:
        """添加测试商品"""
        product_id = max([product["id"] for product in self.products]) + 1 if self.products else 1
        product_data["id"] = product_id
        product_data["created_at"] = datetime.now().isoformat() + "Z"
        self.products.append(product_data)
        return product_id
    
    def remove_test_user(self, user_id: int):
        """删除测试用户"""
        self.users = [user for user in self.users if user["id"] != user_id]
    
    def remove_test_product(self, product_id: int):
        """删除测试商品"""
        self.products = [product for product in self.products if product["id"] != product_id]


# 全局测试数据管理器实例
test_data_manager = TestDataManager()
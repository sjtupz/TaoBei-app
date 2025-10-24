# -*- coding: utf-8 -*-
"""
测试 environment.py 是否被 Behave 正确加载
"""
import os
import sys

def test_environment_loading():
    """测试环境文件加载"""
    print("当前工作目录:", os.getcwd())
    print("Python 路径:", sys.path[:3])
    
    # 尝试导入 environment
    try:
        import environment
        print("✓ environment.py 导入成功")
        print("可用函数:", [name for name in dir(environment) if not name.startswith('_')])
    except ImportError as e:
        print("✗ environment.py 导入失败:", e)
    
    # 检查 Behave 是否能找到 environment.py
    from behave.configuration import Configuration
    from behave.runner import Runner
    
    config = Configuration()
    print("Behave 配置路径:", config.paths)
    print("Behave 基础目录:", config.base_dir)

if __name__ == "__main__":
    test_environment_loading()
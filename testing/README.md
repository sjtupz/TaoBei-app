# 淘贝应用自动化测试项目

本项目为淘贝应用提供完整的自动化测试解决方案，包括用户登录、注册、用户管理和商品管理功能的UI测试和API测试。

## 项目结构

```
TesT/
├── features/                      # BDD特性文件
│   ├── login.feature             # 登录功能测试场景
│   ├── register.feature          # 注册功能测试场景
│   ├── user_management.feature   # 用户管理功能测试场景
│   └── product_management.feature # 商品管理功能测试场景
├── pages/                        # 页面对象模型
│   ├── __init__.py
│   ├── base_page.py             # 基础页面类
│   ├── login_page.py            # 登录页面对象
│   ├── register_page.py         # 注册页面对象
│   ├── user_management_page.py  # 用户管理页面对象
│   └── product_management_page.py # 商品管理页面对象
├── steps/                        # BDD步骤定义
│   ├── __init__.py
│   ├── login_steps.py           # 登录功能步骤定义
│   ├── register_steps.py        # 注册功能步骤定义
│   ├── user_management_steps.py # 用户管理功能步骤定义
│   └── product_management_steps.py # 商品管理功能步骤定义
├── utils/                        # 工具类
│   ├── __init__.py
│   ├── config.py                # 配置管理
│   ├── database_helper.py       # 数据库操作工具
│   ├── api_helper.py            # API测试工具
│   └── test_data.py             # 测试数据管理
├── reports/                      # 测试报告目录
├── conftest.py                  # pytest配置和fixtures
├── pytest.ini                  # pytest配置文件
├── requirements.txt             # 项目依赖
└── README.md                   # 项目说明文档
```

## 技术栈

- **测试框架**: pytest + pytest-bdd
- **UI自动化**: Playwright
- **API测试**: requests + httpx
- **数据管理**: SQLite
- **报告生成**: pytest-html + allure-pytest
- **设计模式**: Page Object Model (POM)

## 环境准备

### 1. 安装Python依赖

```bash
cd d:/Project/taobei-app/TesT
pip install -r requirements.txt
```

### 2. 安装Playwright浏览器

```bash
playwright install
```

### 3. 环境配置

确保淘贝应用正在运行：
- 前端应用: http://localhost:3000
- 后端API: http://localhost:5000

## 运行测试

### 运行所有测试

```bash
pytest
```

### 运行特定功能测试

```bash
# 只运行登录功能测试
pytest -m login

# 只运行注册功能测试
pytest -m register

# 只运行用户管理功能测试
pytest -m user_management

# 只运行商品管理功能测试
pytest -m product_management

# 只运行UI测试
pytest -m ui

# 只运行API测试
pytest -m api
```

### 运行特定测试文件

```bash
# 运行登录功能的所有测试
pytest features/login.feature

# 运行注册功能的所有测试
pytest features/register.feature

# 运行用户管理功能的所有测试
pytest features/user_management.feature

# 运行商品管理功能的所有测试
pytest features/product_management.feature
```

### 运行特定场景

```bash
# 运行特定场景（使用场景名称）
pytest -k "成功登录"
pytest -k "成功注册"
```

### 生成测试报告

```bash
# 生成HTML报告
pytest --html=reports/report.html --self-contained-html

# 生成JSON报告
pytest --json-report --json-report-file=reports/report.json

# 生成Allure报告
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 测试配置

### 浏览器配置

在 `utils/config.py` 中可以配置：
- 浏览器类型（默认：chromium）
- 无头模式（默认：True）
- 慢动作模式（默认：0ms）
- 超时时间（默认：30秒）

### 测试数据配置

在 `utils/config.py` 中可以配置：
- 测试用手机号
- 测试用验证码
- API端点URL
- 数据库路径

## 测试覆盖范围

### 登录功能测试

#### UI测试场景：
- ✅ 成功登录流程
- ✅ 无效手机号验证
- ✅ 错误验证码处理
- ✅ 未注册手机号处理
- ✅ 过期验证码处理
- ✅ 空字段验证
- ✅ 验证码倒计时功能
- ✅ 页面跳转验证

#### API测试场景：
- ✅ 登录API成功响应
- ✅ 登录API错误处理
- ✅ 验证码发送API
- ✅ 令牌生成验证

### 注册功能测试

#### UI测试场景：
- ✅ 成功注册流程
- ✅ 无效手机号验证
- ✅ 错误/过期验证码处理
- ✅ 已注册手机号处理
- ✅ 用户协议验证
- ✅ 空字段验证
- ✅ 实时格式验证
- ✅ 页面跳转验证

#### API测试场景：
- ✅ 注册API成功响应
- ✅ 注册API错误处理
- ✅ 用户信息创建验证
- ✅ 数据库记录验证

### 用户管理功能测试

#### UI测试场景：
- ✅ 成功更新用户信息（昵称、头像）
- ✅ 单独更新昵称或头像
- ✅ 无效昵称验证
- ✅ 无效头像URL验证
- ✅ 空字段提交处理
- ✅ 成功退出登录
- ✅ 退出登录后访问保护页面
- ✅ 未授权访问处理

#### API测试场景：
- ✅ 获取用户信息API
- ✅ 更新用户信息API成功响应
- ✅ 更新用户信息验证失败处理
- ✅ 退出登录API
- ✅ 未授权访问API处理
- ✅ 无效令牌处理

### 商品管理功能测试

#### UI测试场景：
- ✅ 查看商品列表（默认分页）
- ✅ 自定义分页参数
- ✅ 无效分页参数处理
- ✅ 商品搜索功能
- ✅ 搜索不存在的商品
- ✅ 按分类筛选商品
- ✅ 按价格排序（升序/降序）
- ✅ 按名称排序（升序/降序）
- ✅ 组合筛选和搜索
- ✅ 查看商品详情
- ✅ 访问不存在的商品详情
- ✅ 商品详情页面交互

#### API测试场景：
- ✅ 获取商品列表API（带/不带分页）
- ✅ 商品搜索API
- ✅ 商品分类筛选API
- ✅ 商品排序API
- ✅ 获取商品详情API
- ✅ 不存在商品详情处理
- ✅ 无效分页参数处理
- ✅ 无效商品ID处理
- ✅ 搜索关键词长度验证

## 最佳实践

### 1. 页面对象模型 (POM)
- 所有页面元素和操作都封装在对应的页面类中
- 测试逻辑与页面实现分离
- 提高代码可维护性和复用性

### 2. BDD测试方法
- 使用Given-When-Then结构编写测试场景
- 测试场景直接对应业务需求
- 提高测试可读性和业务理解

### 3. 数据管理
- 每个测试用例独立的测试数据
- 自动清理测试数据
- 支持并行测试执行

### 4. 错误处理
- 完善的异常处理机制
- 详细的错误日志记录
- 失败时自动截图保存

## 故障排除

### 常见问题

1. **浏览器启动失败**
   ```bash
   playwright install chromium
   ```

2. **数据库连接错误**
   - 检查数据库文件路径
   - 确保有读写权限

3. **API连接超时**
   - 确认后端服务正在运行
   - 检查API端点配置

4. **元素定位失败**
   - 检查页面是否完全加载
   - 验证元素选择器是否正确

### 调试模式

```bash
# 启用详细日志
pytest -v -s

# 启用浏览器可视模式
pytest --headed

# 启用慢动作模式
pytest --slowmo=1000
```

## 持续集成

本测试项目支持在CI/CD环境中运行：

```yaml
# GitHub Actions 示例
- name: Run Tests
  run: |
    pip install -r requirements.txt
    playwright install
    pytest --html=reports/report.html
```

## 贡献指南

1. 遵循现有的代码风格和结构
2. 为新功能添加相应的测试用例
3. 更新相关文档
4. 确保所有测试通过

## 联系信息

如有问题或建议，请联系测试团队。
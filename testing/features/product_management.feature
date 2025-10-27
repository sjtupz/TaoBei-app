# language: zh-CN
Feature: 商品管理
  作为一个用户
  我希望能够浏览和搜索商品
  以便找到我需要的商品信息

  Background:
    Given 系统已经启动并运行正常
    And 测试数据库已经初始化
    And 系统中存在商品数据

  Scenario: 成功获取商品列表 - 默认参数
    Given 系统中存在商品数据
    When 用户请求商品列表
    Then 系统返回分页的商品列表
    And 包含商品的基本信息（ID、名称、价格、图片等）
    And 商品列表页面显示商品信息
    And 显示分页控件

  Scenario Outline: 成功获取商品列表 - 自定义分页参数
    Given 系统中存在商品数据
    When 用户请求商品列表，页码为 <page>，每页数量为 <pageSize>
    Then 系统返回分页的商品列表
    And 包含商品的基本信息（ID、名称、价格、图片等）
    And 返回的商品数量不超过 <pageSize>
    And 商品列表页面显示第 <page> 页的商品

    Examples:
      | page | pageSize |
      | 1    | 10       |
      | 2    | 5        |
      | 1    | 20       |

  Scenario: 成功获取商品详情
    Given 系统中存在ID为1的商品
    When 用户请求ID为1的商品详情
    Then 系统返回该商品的详细信息
    And 包含商品的完整信息（ID、名称、价格、描述、图片、库存等）
    And 商品详情页面显示商品信息

  Scenario: 获取不存在的商品详情
    Given 系统中不存在ID为999的商品
    When 用户请求ID为999的商品详情
    Then 系统返回404错误
    And 错误信息包含 "商品不存在"

  Scenario Outline: 成功搜索商品 - 按名称搜索
    Given 系统中存在商品数据
    When 用户搜索商品，关键词为 "<keyword>"
    Then 系统返回包含关键词的商品列表
    And 商品名称包含 "<keyword>"
    And 搜索结果页面显示匹配的商品

    Examples:
      | keyword |
      | 手机    |
      | 电脑    |
      | 耳机    |

  Scenario: 搜索商品 - 无匹配结果
    Given 系统中存在商品数据
    When 用户搜索商品，关键词为 "不存在的商品"
    Then 系统返回空的商品列表
    And 搜索结果页面显示 "未找到匹配的商品"

  Scenario Outline: 成功搜索商品 - 按价格范围搜索
    Given 系统中存在商品数据
    When 用户搜索商品，价格范围为 <minPrice> 到 <maxPrice>
    Then 系统返回价格在指定范围内的商品列表
    And 所有商品价格都在 <minPrice> 到 <maxPrice> 之间

    Examples:
      | minPrice | maxPrice |
      | 100      | 500      |
      | 500      | 1000     |
      | 1000     | 5000     |

  Scenario: 商品列表分页 - 超出范围的页码
    Given 系统中存在10个商品
    When 用户请求商品列表，页码为 999，每页数量为 10
    Then 系统返回空的商品列表
    And 分页信息显示总页数和当前页码

  Scenario: 商品列表 - 无效的分页参数
    Given 系统中存在商品数据
    When 用户请求商品列表，页码为 0，每页数量为 -1
    Then 系统返回400错误
    And 错误信息包含 "无效的分页参数"

  # API测试场景
  Scenario: API - 成功获取商品列表
    Given 系统中存在商品数据
    When 我通过API请求商品列表
    Then API返回状态码200
    And API响应包含商品列表
    And 商品列表包含商品的基本信息

  Scenario: API - 成功获取商品详情
    Given 系统中存在ID为1的商品
    When 我通过API请求ID为1的商品详情
    Then API返回状态码200
    And API响应包含商品详情
    And 商品详情包含完整的商品信息

  Scenario: API - 获取不存在的商品详情
    Given 系统中不存在ID为999的商品
    When 我通过API请求ID为999的商品详情
    Then API返回状态码404
    And API响应包含商品不存在的错误信息

  Scenario: API - 成功搜索商品
    Given 系统中存在商品数据
    When 我通过API搜索商品，关键词为 "手机"
    Then API返回状态码200
    And API响应包含搜索结果
    And 搜索结果中的商品名称包含 "手机"

  Scenario: API - 搜索商品无结果
    Given 系统中存在商品数据
    When 我通过API搜索商品，关键词为 "不存在的商品"
    Then API返回状态码200
    And API响应包含空的搜索结果

  Scenario: API - 商品列表分页
    Given 系统中存在商品数据
    When 我通过API请求商品列表，页码为 1，每页数量为 5
    Then API返回状态码200
    And API响应包含分页信息
    And 返回的商品数量不超过 5

  Scenario: API - 无效的商品ID格式
    When 我通过API请求ID为 "invalid" 的商品详情
    Then API返回状态码400
    And API响应包含无效ID格式的错误信息

  # 性能测试场景
  Scenario: 商品列表加载性能
    Given 系统中存在大量商品数据
    When 用户请求商品列表
    Then 系统在3秒内返回商品列表
    And 商品列表页面在3秒内完成加载

  Scenario: 商品搜索性能
    Given 系统中存在大量商品数据
    When 用户搜索商品，关键词为 "手机"
    Then 系统在2秒内返回搜索结果
    And 搜索结果页面在2秒内完成加载

  # 边界测试场景
  Scenario: 商品列表 - 最大分页大小
    Given 系统中存在商品数据
    When 用户请求商品列表，页码为 1，每页数量为 100
    Then 系统返回商品列表
    And 返回的商品数量不超过 100

  Scenario: 商品搜索 - 空关键词
    Given 系统中存在商品数据
    When 用户搜索商品，关键词为空
    Then 系统返回所有商品列表
    And 搜索结果页面显示所有商品

  Scenario: 商品搜索 - 特殊字符关键词
    Given 系统中存在商品数据
    When 用户搜索商品，关键词为 "!@#$%^&*()"
    Then 系统返回空的商品列表
    And 搜索结果页面显示 "未找到匹配的商品"

  # 缓存测试场景
  Scenario: 商品列表缓存
    Given 系统中存在商品数据
    And 商品列表已被缓存
    When 用户请求商品列表
    Then 系统快速返回缓存的商品列表
    And 响应时间小于1秒

  Scenario: 商品详情缓存
    Given 系统中存在ID为1的商品
    And 该商品详情已被缓存
    When 用户请求ID为1的商品详情
    Then 系统快速返回缓存的商品详情
    And 响应时间小于1秒
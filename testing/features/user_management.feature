# language: zh-CN
Feature: 用户管理
  作为一个已登录的用户
  我希望能够管理我的个人信息
  以便保持账户信息的准确性和安全性

  Background:
    Given 系统已经启动并运行正常
    And 测试数据库已经初始化

  Scenario Outline: 成功更新用户信息
    Given 用户已登录
    When 用户提交有效的个人信息更新请求，昵称为 "<nickname>"，头像为 "<avatar>"
    Then 系统更新用户信息并返回成功响应
    And 返回更新后的用户信息
    And 用户信息页面显示更新后的昵称 "<nickname>"

    Examples:
      | nickname | avatar |
      | 小明     | https://example.com/avatar1.jpg |
      | 测试用户 | https://example.com/avatar2.jpg |
      | 新昵称   | https://example.com/avatar3.jpg |

  Scenario: 更新用户信息 - 只更新昵称
    Given 用户已登录
    When 用户提交有效的个人信息更新请求，昵称为 "更新的昵称"
    Then 系统更新用户信息并返回成功响应
    And 返回更新后的用户信息
    And 用户信息页面显示更新后的昵称 "更新的昵称"

  Scenario: 更新用户信息 - 只更新头像
    Given 用户已登录
    When 用户提交有效的个人信息更新请求，头像为 "https://example.com/new-avatar.jpg"
    Then 系统更新用户信息并返回成功响应
    And 返回更新后的用户信息
    And 用户信息页面显示更新后的头像

  Scenario Outline: 提交无效的用户信息 - 昵称验证失败
    Given 用户已登录
    When 用户提交包含无效昵称 "<invalid_nickname>" 的更新请求
    Then 系统返回400错误并提示具体的验证失败信息
    And 错误信息包含 "<error_message>"

    Examples:
      | invalid_nickname | error_message |
      |                  | 昵称长度必须在1-50个字符之间 |
      | 这是一个非常非常非常非常非常非常非常非常非常非常非常非常非常非常非常非常长的昵称 | 昵称长度必须在1-50个字符之间 |

  Scenario Outline: 提交无效的用户信息 - 头像URL验证失败
    Given 用户已登录
    When 用户提交包含无效头像URL "<invalid_avatar>" 的更新请求
    Then 系统返回400错误并提示具体的验证失败信息
    And 错误信息包含 "头像必须是有效的URL地址"

    Examples:
      | invalid_avatar |
      | invalid-url    |
      | not-a-url      |
      | ftp://invalid  |

  Scenario: 提交无效的用户信息 - 空的更新请求
    Given 用户已登录
    When 用户提交空的个人信息更新请求
    Then 系统返回400错误并提示具体的验证失败信息

  Scenario: 成功注销
    Given 用户已登录
    When 用户发起注销请求
    Then 系统清除用户的登录状态
    And 返回注销成功响应
    And 用户被重定向到登录页面
    And 用户无法访问需要登录的页面

  Scenario: 注销后再次访问需要登录的页面
    Given 用户已登录
    And 用户已成功注销
    When 用户尝试访问用户信息页面
    Then 用户被重定向到登录页面
    And 页面显示 "请先登录"

  Scenario: 未登录用户尝试更新信息
    Given 用户未登录
    When 用户尝试提交个人信息更新请求
    Then 系统返回401错误
    And 错误信息包含 "未授权访问"

  Scenario: 未登录用户尝试注销
    Given 用户未登录
    When 用户尝试发起注销请求
    Then 系统返回401错误
    And 错误信息包含 "未授权访问"

  # API测试场景
  Scenario: API - 成功获取用户信息
    Given 用户通过API已登录
    When 我通过API请求获取用户信息
    Then API返回状态码200
    And API响应包含用户信息
    And 用户信息包含手机号、昵称、头像等字段

  Scenario: API - 成功更新用户信息
    Given 用户通过API已登录
    When 我通过API更新用户信息，昵称为 "API测试昵称"，头像为 "https://example.com/api-avatar.jpg"
    Then API返回状态码200
    And API响应包含更新成功的消息
    And API响应包含更新后的用户信息

  Scenario: API - 更新用户信息验证失败
    Given 用户通过API已登录
    When 我通过API提交包含无效昵称的更新请求
    Then API返回状态码400
    And API响应包含验证失败的错误信息

  Scenario: API - 成功注销
    Given 用户通过API已登录
    When 我通过API发起注销请求
    Then API返回状态码200
    And API响应包含注销成功的消息

  Scenario: API - 未授权访问用户信息
    Given 用户未通过API登录
    When 我通过API请求获取用户信息
    Then API返回状态码401
    And API响应包含未授权的错误信息

  Scenario: API - 使用无效token访问用户信息
    Given 我使用无效的token
    When 我通过API请求获取用户信息
    Then API返回状态码401
    And API响应包含token无效的错误信息
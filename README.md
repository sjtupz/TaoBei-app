# 淘贝 (TaoBei) - 电商应用系统

一个基于 Node.js + React 的现代化电商应用系统，目前已支持新用户注册，手机号登录与账号登录等功能。

## 📁 项目结构

```
TaoBei-app/
├── src/
│   ├── frontend/        # React 前端应用
│   │   ├── components/  # React 组件
│   │   ├── App.jsx      # 主应用组件
│   │   ├── App.css      # 应用样式
│   │   ├── main.jsx     # 应用入口
│   │   ├── index.html   # HTML 模板
│   │   ├── vite.config.js # Vite 配置文件
│   │   ├── package.json # 前端依赖配置
│   │   └── package-lock.json # 前端依赖版本锁定
│   ├── backend/         # Node.js 后端服务
│   │   ├── routes/      # API 路由
│   │   ├── utils/       # 工具函数
│   │   ├── app.js       # Express 应用配置和服务器启动
│   │   ├── .env         # 环境变量配置
│   │   ├── package.json # 后端依赖配置
│   │   └── package-lock.json # 后端依赖版本锁定
│   └── database/        # 数据库相关
│       ├── database.js  # 数据库连接配置
│       ├── index.js     # 数据库初始化
│       ├── userDAO.js   # 用户数据访问层
│       ├── verificationCodeDAO.js # 验证码数据访问层
│       ├── init.sql     # 数据库初始化脚本
│       └── taobei.db    # SQLite 数据库文件
├── testing/             # 测试文件和报告
├── .artifacts/          # 接口规格文件
├── vite.config.js      # 根级 Vite 配置
└── 课程实践流程.pdf     # 项目文档
```

## 🚀 快速开始

### 环境要求
- Node.js 16+ 
- npm 或 yarn

### 开发环境运行

1. **启动后端服务**
   ```bash
   # 进入后端目录
   cd src/backend
   
   # 安装依赖
   npm install
   
   # 启动后端服务
   npm start
   ```
   - 后端服务将在 http://localhost:3001 运行

2. **启动前端服务**（新开一个终端窗口）
   ```bash
   # 进入前端目录
   cd src/frontend
   
   # 安装依赖
   npm install
   
   # 启动前端开发服务器
   npm run dev
   ```
   - 前端应用将在 http://localhost:5173 运行

3. **访问应用**
   - 打开浏览器访问 http://localhost:5173
   - 后端API地址：http://localhost:3001/api/*

### 生产环境部署

1. **构建前端**
   ```bash
   cd src/frontend
   npm run build
   ```

2. **启动后端服务**
   ```bash
   cd src/backend
   npm start
   ```

3. **预览构建结果**
   ```bash
   cd src/frontend
   npm run preview
   ```
   - 此时，前端应用可在 http://localhost:4173 进行预览


## 🧪 测试

### 测试环境准备
```bash
# 进入测试目录
cd testing

# 安装 Python 测试依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器（用于 UI 测试）
playwright install
```

### 运行测试

#### 1. 基础功能测试
```bash
# 运行基础登录功能测试
pytest test_simple_login.py -v

# 运行 API 接口测试
pytest test_login_api.py -v

# 运行所有基础测试并生成报告
pytest test_simple_login.py test_login_api.py --html=reports/test_report.html
```

#### 2. BDD 行为驱动测试
```bash
# 注意：BDD 测试需要前端服务运行在 http://localhost:5173
# 请先启动前端服务，然后运行：

# 运行登录 BDD 测试
pytest test_login_bdd_fixed.py -v

# 运行注册 BDD 测试  
pytest test_register_bdd_fixed.py -v

# 使用 behave 直接运行 BDD 功能测试
behave features/login.feature
```

### 测试报告
测试完成后，可在 `testing/reports/` 目录查看：
- HTML 格式报告：`test_report.html`
- JSON 格式报告：`report.json`

### 注意事项
- API 测试：可独立运行，不需要前端服务
- BDD UI 测试：需要前端服务运行在 `http://localhost:5173`
- 后端服务：所有测试都需要后端服务运行在 `http://localhost:3001`


## 🔧 配置说明

#### 后端配置 (`src/backend/`)
- 端口: 3001 (可通过环境变量 `PORT` 修改)
- API 路径: `/api/*`
- 数据库: SQLite (`src/database/taobei.db`，自动初始化)

#### 前端配置 (`src/frontend/`)
- 开发端口: 5173 (Vite 开发服务器默认端口)
- 预览端口: 4173 (Vite 预览服务器默认端口)
- API 代理: 自动代理 `/api` 请求到 `http://localhost:3001`
- 构建输出: `src/frontend/dist/` 目录



## 📱 功能特性

### 用户认证系统
- ✅ 用户注册
- ✅ 用户信息管理
- ✅ 手机号验证码登录
- ✅ 登录状态保持

### 技术特性
- ✅ 响应式设计
- ✅ 现代化 UI
- ✅ 错误处理和加载状态
- ✅ RESTful API 设计
- ✅ 数据库自动初始化
- ✅ 安全中间件集成


## 📞 技术支持

### 可能错误
如有问题，请检查：
1. Node.js 版本是否为 16+
2. 端口 3001 和 5173 是否被占用
3. 网络连接是否正常
4. 数据库文件是否有读写权限

### 常见问题

**Q: 验证码在哪里查看？**
A: 验证码会打印在后端控制台中，请查看终端输出。

**Q: 数据库文件在哪里？**
A: SQLite 数据库文件位于 `src/database/taobei.db`，首次运行会自动创建。

**Q: 如何重置数据库？**
A: 删除 `src/database/taobei.db` 文件，重启后端服务即可自动重新初始化。

---

**注意**: 生产环境部署时，请确保后端 API 服务正常运行，前端才能正常使用所有功能。建议使用 PM2 或 Docker 等工具管理生产环境服务。
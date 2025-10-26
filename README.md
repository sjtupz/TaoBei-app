# 淘贝 (TaoBei) - 电商应用系统

一个基于 Node.js + React 的现代化电商应用系统，目前已支持新用户注册，手机号登录与账号登录等功能。

## 📁 项目结构

```
TaoBei-app/
├── src/
│   ├── frontend/        # React 前端应用
│   │   ├── components/  # React 组件
│   │   ├── App.jsx      # 主应用组件
│   │   ├── main.jsx     # 应用入口
│   │   ├── index.html   # HTML 模板
│   │   ├── vite.config.js # Vite 配置文件
│   │   └── package.json # 前端依赖配置
│   ├── backend/         # Node.js 后端服务
│   │   ├── routes/      # API 路由
│   │   ├── utils/       # 工具函数
│   │   ├── app.js       # Express 应用配置
│   │   ├── server.js    # 服务器启动文件
│   │   └── package.json # 后端依赖配置
│   └── database/        # 数据库相关
│       ├── *.js         # 数据访问层 (DAO)
│       ├── init.sql     # 数据库初始化脚本
│       └── taobei.db    # SQLite 数据库文件
├── testing/             # 测试文件和报告
├── .artifacts/          # 接口规格文件
├── vite.config.js      # 根级 Vite 配置
├── package.json        # 项目配置和脚本
└── package-lock.json   # 依赖版本锁定文件
```

## 🚀 快速开始

### 方式一：开发环境运行

1. **安装依赖**
   ```bash
   npm install
   ```

2. **同时启动前后端服务**
   ```bash
   npm run dev
   ```
   - 前端应用将在 http://localhost:5173 运行
   - 后端服务将在 http://localhost:3001 运行

3. **分别启动服务**
   ```bash
   # 启动后端服务
   npm run dev:backend
   
   # 启动前端开发服务器
   npm run dev:frontend
   ```

### 方式二：生产环境部署

1. **构建前端**
   ```bash
   npm run build
   ```
   - 构建后的文件将生成在`/src/frontend/dist/`目录

2. **启动后端服务**
   ```bash
   npm run start:backend
   ```

3. **预览构建结果**
   ```bash
   cd src/frontend
   npm run preview
   ```
   - 此时，可以在`http://localhost:4173`预览构建结果



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



## 🧪 测试

### Node.js 测试
```bash
# 运行后端测试
cd src/backend && npm test
```

### Python 测试套件
```bash
# 运行 Python 测试套件 (需要安装 Python 和依赖)
cd testing && pip install -r requirements.txt
cd testing && python -m pytest

# 运行 BDD 测试
cd testing && python -m behave

# 运行特定测试
cd testing && python run_tests.py
```


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
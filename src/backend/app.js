const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 静态文件服务
app.use(express.static(path.join(__dirname, 'public')));

// 路由
const authRoutes = require('./routes/auth');
app.use('/api/auth', authRoutes);

// 健康检查端点
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: '淘贝商城后端服务运行正常' });
});

// 404 处理
app.use('*', (req, res) => {
  res.status(404).json({ error: '接口不存在' });
});

// 错误处理中间件
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: '服务器内部错误' });
});

app.listen(PORT, () => {
  console.log(`淘贝商城后端服务启动成功，端口: ${PORT}`);
  console.log(`健康检查: http://localhost:${PORT}/api/health`);
});

module.exports = app;
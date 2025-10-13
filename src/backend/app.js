const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const path = require('path');

// 导入路由
const authRoutes = require('./routes/auth');
const userRoutes = require('./routes/user');
const productRoutes = require('./routes/products');
const cartRoutes = require('./routes/cart');
const orderRoutes = require('./routes/orders');

const app = express();

// 安全中间件
app.use(helmet({
    contentSecurityPolicy: false, // 开发环境下禁用CSP
}));

// CORS配置
app.use(cors({
    origin: ['http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:5173', 'http://127.0.0.1:5173'],
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization']
}));

// 请求日志
app.use(morgan('combined'));

// 解析JSON请求体
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// 静态文件服务
app.use(express.static(path.join(__dirname, '../frontend/dist')));

// API路由
app.use('/api/auth', authRoutes);
app.use('/api/user', userRoutes);
app.use('/api/products', productRoutes);
app.use('/api/cart', cartRoutes);
app.use('/api/orders', orderRoutes);

// 健康检查端点
app.get('/api/health', (req, res) => {
    res.status(200).json({
        status: 'ok',
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

// 前端路由处理（SPA支持）
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/dist/index.html'));
});

// 全局错误处理中间件
app.use((err, req, res, next) => {
    console.error('全局错误处理:', err);
    
    // 处理JWT错误
    if (err.name === 'JsonWebTokenError') {
        return res.status(401).json({ error: '无效的token' });
    }
    
    if (err.name === 'TokenExpiredError') {
        return res.status(401).json({ error: 'token已过期' });
    }
    
    // 处理验证错误
    if (err.name === 'ValidationError') {
        return res.status(400).json({ error: err.message });
    }
    
    // 默认错误响应
    res.status(500).json({ 
        error: '服务器内部错误',
        message: process.env.NODE_ENV === 'development' ? err.message : undefined
    });
});

// 404处理
app.use((req, res) => {
    res.status(404).json({ error: '接口不存在' });
});

module.exports = app;
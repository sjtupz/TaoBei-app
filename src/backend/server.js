require('dotenv').config();
const app = require('./app');
const { initDatabase } = require('../database');

const PORT = process.env.PORT || 3001;

async function startServer() {
    try {
        // 初始化数据库
        console.log('正在初始化数据库...');
        await initDatabase();
        console.log('数据库初始化完成');

        // 启动服务器
        const server = app.listen(PORT, () => {
            console.log(`服务器已启动，端口: ${PORT}`);
            console.log(`API地址: http://localhost:${PORT}/api`);
            console.log(`健康检查: http://localhost:${PORT}/api/health`);
        });

        // 优雅关闭
        process.on('SIGTERM', () => {
            console.log('收到SIGTERM信号，正在关闭服务器...');
            server.close(() => {
                console.log('服务器已关闭');
                process.exit(0);
            });
        });

        process.on('SIGINT', () => {
            console.log('收到SIGINT信号，正在关闭服务器...');
            server.close(() => {
                console.log('服务器已关闭');
                process.exit(0);
            });
        });

    } catch (error) {
        console.error('服务器启动失败:', error);
        process.exit(1);
    }
}

// 启动服务器
startServer();
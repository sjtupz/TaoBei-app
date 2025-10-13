import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import './App.css';

const App = () => {
    const [currentView, setCurrentView] = useState('login'); // 'login' or 'register'
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // 检查用户登录状态
    useEffect(() => {
        const token = localStorage.getItem('token');
        const userData = localStorage.getItem('user');
        
        if (token && userData) {
            try {
                setUser(JSON.parse(userData));
            } catch (error) {
                console.error('解析用户数据失败:', error);
                localStorage.removeItem('token');
                localStorage.removeItem('user');
            }
        }
        setLoading(false);
    }, []);

    // 处理登录成功
    const handleLoginSuccess = (userData) => {
        setUser(userData);
    };

    // 处理注册成功
    const handleRegisterSuccess = (userData) => {
        setUser(userData);
    };

    // 处理退出登录
    const handleLogout = async () => {
        try {
            const token = localStorage.getItem('token');
            if (token) {
                await fetch('/api/auth/logout', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });
            }
        } catch (error) {
            console.error('退出登录失败:', error);
        } finally {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            setUser(null);
        }
    };

    // 切换到注册页面
    const switchToRegister = () => {
        setCurrentView('register');
    };

    // 切换到登录页面
    const switchToLogin = () => {
        setCurrentView('login');
    };

    if (loading) {
        return (
            <div className="app-loading">
                <div className="loading-spinner"></div>
                <p>加载中...</p>
            </div>
        );
    }

    // 已登录状态
    if (user) {
        return (
            <div className="app-container">
                <header className="app-header">
                    <div className="header-content">
                        <div className="logo">
                            <h1>淘宝</h1>
                            <span className="logo-subtitle">Taobao</span>
                        </div>
                        <div className="user-info">
                            <span className="welcome-text">欢迎，{user.nickname || user.phoneNumber}</span>
                            <button className="logout-btn" onClick={handleLogout}>
                                退出登录
                            </button>
                        </div>
                    </div>
                </header>

                <main className="app-main">
                    <div className="main-content">
                        <div className="welcome-section">
                            <h2>欢迎来到淘宝</h2>
                            <p>您已成功登录，可以开始购物了！</p>
                            
                            <div className="user-profile">
                                <h3>个人信息</h3>
                                <div className="profile-item">
                                    <label>手机号：</label>
                                    <span>{user.phoneNumber}</span>
                                </div>
                                <div className="profile-item">
                                    <label>昵称：</label>
                                    <span>{user.nickname || '未设置'}</span>
                                </div>
                                <div className="profile-item">
                                    <label>注册时间：</label>
                                    <span>{user.createdAt ? new Date(user.createdAt).toLocaleDateString() : '未知'}</span>
                                </div>
                            </div>

                            <div className="quick-actions">
                                <h3>快捷操作</h3>
                                <div className="action-buttons">
                                    <button className="action-btn">浏览商品</button>
                                    <button className="action-btn">我的订单</button>
                                    <button className="action-btn">购物车</button>
                                    <button className="action-btn">个人设置</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </main>
            </div>
        );
    }

    // 未登录状态
    return (
        <div className="app-container">
            <header className="app-header">
                <div className="header-content">
                    <div className="logo">
                        <h1>淘宝</h1>
                        <span className="logo-subtitle">Taobao</span>
                    </div>
                    <div className="header-links">
                        <a href="#" className="header-link">网站导航</a>
                        <a href="#" className="header-link">帮助中心</a>
                    </div>
                </div>
            </header>

            <main className="app-main">
                <div className="auth-container">
                    <div className="auth-left">
                        <div className="qr-section">
                            <h3>手机扫码登录</h3>
                            <div className="qr-code">
                                <div className="qr-placeholder">
                                    <svg width="200" height="200" viewBox="0 0 200 200">
                                        <rect width="200" height="200" fill="#f5f5f5" stroke="#ddd"/>
                                        <text x="100" y="100" textAnchor="middle" dy=".3em" fill="#999">
                                            二维码
                                        </text>
                                    </svg>
                                </div>
                            </div>
                            <p className="qr-tip">打开淘宝APP，扫一扫登录</p>
                            <p className="qr-question">
                                <a href="#">无法扫码？</a>
                            </p>
                        </div>
                    </div>

                    <div className="auth-right">
                        {currentView === 'login' ? (
                            <Login 
                                onLoginSuccess={handleLoginSuccess}
                                onSwitchToRegister={switchToRegister}
                            />
                        ) : (
                            <Register 
                                onRegisterSuccess={handleRegisterSuccess}
                                onSwitchToLogin={switchToLogin}
                            />
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
};

export default App;
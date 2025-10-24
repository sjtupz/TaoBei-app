import React, { useState, useEffect } from 'react';
import './App.css';
import UnifiedLogin from './components/UnifiedLogin';
import Register from './components/Register';

function App() {
  const [currentView, setCurrentView] = useState('login');
  const [error, setError] = useState('');
  const [isAnimating, setIsAnimating] = useState(false);
  const [qrStatus, setQrStatus] = useState('loading'); // loading, success, error

  // 清除错误提示
  const clearError = () => {
    setError('');
  };

  // 显示错误提示
  const showError = (message) => {
    setError(message);
    setTimeout(() => {
      setError('');
    }, 3000);
  };

  // 切换到注册页面
  const switchToRegister = () => {
    try {
      if (isAnimating) return;
      
      setIsAnimating(true);
      clearError();
      
      console.log('切换到注册页面...');
      
      setTimeout(() => {
        setCurrentView('register');
        setIsAnimating(false);
        console.log('成功切换到注册页面');
      }, 150);
      
    } catch (error) {
      console.error('切换到注册页面时发生错误:', error);
      showError('页面切换失败，请重试');
      setIsAnimating(false);
    }
  };

  // 切换到登录页面
  const switchToLogin = () => {
    try {
      if (isAnimating) return;
      
      setIsAnimating(true);
      clearError();
      
      console.log('切换到登录页面...');
      
      setTimeout(() => {
        setCurrentView('login');
        setIsAnimating(false);
        console.log('成功切换到登录页面');
      }, 150);
      
    } catch (error) {
      console.error('切换到登录页面时发生错误:', error);
      showError('页面切换失败，请重试');
      setIsAnimating(false);
    }
  };

  // 处理登录成功
  const handleLoginSuccess = (userInfo) => {
    try {
      console.log('登录成功，用户信息:', userInfo);
      
      // 显示成功消息
      alert('登录成功！');
      
      // 跳转到首页URL
      window.history.pushState({}, '', '/home');
      
      // 设置视图状态
      setCurrentView('dashboard');
      
    } catch (error) {
      console.error('处理登录成功时发生错误:', error);
      showError('登录成功但页面跳转失败');
    }
  };

  // 自动清除错误提示
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        setError('');
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  // 模拟二维码加载
  useEffect(() => {
    const timer = setTimeout(() => {
      setQrStatus('success');
    }, 1500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="app">
      {/* 顶部导航栏 */}
      <header className="app-header">
        <div className="app-logo">
          <h1>淘宝</h1>
          <span className="logo-text">Taobao</span>
        </div>
        <nav className="app-nav">
          <a href="#" className="nav-link">网站无障碍</a>
          <a href="#" className="nav-link highlight">登录页面</a>
          <span className="nav-link">欢迎建议</span>
        </nav>
      </header>

      {/* 主内容区域 */}
      <main className="app-main">
        <div className="auth-container">
          {/* 左侧 - 手机扫码登录 */}
          <div className="qr-section">
            <div className="qr-content">
              <div className="qr-tabs">
                <div className="qr-tab active">手机扫码登录</div>
              </div>
              <div className="qr-code-container">
                <div className="qr-code">
                  {qrStatus === 'loading' && (
                    <div className="qr-loading">
                      <div className="loading-spinner"></div>
                      <p>正在生成二维码...</p>
                    </div>
                  )}
                  {qrStatus === 'success' && (
                    <svg width="180" height="180" viewBox="0 0 180 180">
                      {/* 优化的二维码图案 */}
                      <rect width="180" height="180" fill="#fff"/>
                      {/* 三个定位角 */}
                      <rect x="8" y="8" width="28" height="28" fill="#000"/>
                      <rect x="12" y="12" width="20" height="20" fill="#fff"/>
                      <rect x="16" y="16" width="12" height="12" fill="#000"/>
                      
                      <rect x="144" y="8" width="28" height="28" fill="#000"/>
                      <rect x="148" y="12" width="20" height="20" fill="#fff"/>
                      <rect x="152" y="16" width="12" height="12" fill="#000"/>
                      
                      <rect x="8" y="144" width="28" height="28" fill="#000"/>
                      <rect x="12" y="148" width="20" height="20" fill="#fff"/>
                      <rect x="16" y="152" width="12" height="12" fill="#000"/>
                      
                      {/* 中心淘宝logo */}
                      <rect x="76" y="76" width="28" height="28" fill="#ff6600" rx="4"/>
                      <text x="90" y="95" textAnchor="middle" fill="#fff" fontSize="12" fontWeight="bold">淘</text>
                      
                      {/* 数据模块 */}
                      {Array.from({length: 200}, (_, i) => {
                        const x = 8 + (i % 20) * 8;
                        const y = 8 + Math.floor(i / 20) * 8;
                        const isInCorner = (x < 40 && y < 40) || (x > 140 && y < 40) || (x < 40 && y > 140);
                        const isInCenter = x > 72 && x < 108 && y > 72 && y < 108;
                        if (isInCorner || isInCenter) return null;
                        return (
                          <rect key={i} 
                            x={x} 
                            y={y} 
                            width="6" 
                            height="6" 
                            fill={Math.random() > 0.5 ? "#000" : "#fff"}
                          />
                        );
                      })}
                    </svg>
                  )}
                  {qrStatus === 'error' && (
                    <div className="qr-error">
                      <div className="error-icon">⚠</div>
                      <p>二维码生成失败</p>
                      <button className="retry-btn" onClick={() => setQrStatus('loading')}>
                        重新生成
                      </button>
                    </div>
                  )}
                </div>
                <p className="qr-tip">打开淘宝APP，点击右上角扫一扫</p>
              </div>
              <div className="qr-help">
                <a href="#" className="help-link">怎么扫码登录?</a>
              </div>
            </div>
          </div>

          {/* 右侧 - 登录/注册表单 */}
          <div className="form-section">
            <div className={`page-container ${isAnimating ? 'animating' : ''}`}>
              {currentView === 'login' ? (
                <UnifiedLogin 
                  onSwitchToRegister={switchToRegister}
                  onLoginSuccess={handleLoginSuccess}
                  error={error}
                  clearError={clearError}
                />
              ) : currentView === 'register' ? (
                <Register 
                  onSwitchToLogin={switchToLogin}
                  error={error}
                  clearError={clearError}
                />
              ) : (
                <div className="dashboard">
                  <h2>欢迎来到淘宝！</h2>
                  <p>登录成功，您已进入系统。</p>
                  <button onClick={switchToLogin}>返回登录</button>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      {/* 错误提示 */}
      {error && (
        <div className={`error-toast ${error ? '' : 'fade-out'}`}>
          {error}
        </div>
      )}
    </div>
  );
}

export default App;
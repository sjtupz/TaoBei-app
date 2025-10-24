import React, { useState, useEffect } from 'react';
import './UnifiedLogin.css';

const UnifiedLogin = ({ onLoginSuccess, onSwitchToRegister }) => {
    const [loginMode, setLoginMode] = useState('password'); // 'password' 或 'sms'
    const [formData, setFormData] = useState({
        account: '', // 账号/手机号
        password: '', // 密码
        phoneNumber: '', // 手机号（短信登录）
        verificationCode: '' // 验证码
    });
    const [errors, setErrors] = useState({});
    const [loading, setLoading] = useState(false);
    const [sendingCode, setSendingCode] = useState(false);
    const [countdown, setCountdown] = useState(0);

    // 倒计时效果
    useEffect(() => {
        let timer;
        if (countdown > 0) {
            timer = setTimeout(() => setCountdown(countdown - 1), 1000);
        }
        return () => clearTimeout(timer);
    }, [countdown]);

    // 验证手机号
    const validatePhoneNumber = (phone) => {
        const phoneRegex = /^1[3-9]\d{9}$/;
        return phoneRegex.test(phone);
    };

    // 验证账号（可以是手机号或用户名）
    const validateAccount = (account) => {
        // 如果是手机号格式，验证手机号
        if (/^1\d{10}$/.test(account)) {
            return validatePhoneNumber(account);
        }
        // 否则验证用户名格式（4-20位字母数字下划线）
        const usernameRegex = /^[a-zA-Z0-9_]{4,20}$/;
        return usernameRegex.test(account);
    };

    // 处理输入变化
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        
        // 清除对应字段的错误
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    // 切换登录模式
    const switchLoginMode = (mode) => {
        setLoginMode(mode);
        setErrors({});
        // 清空表单数据
        setFormData({
            account: '',
            password: '',
            phoneNumber: '',
            verificationCode: ''
        });
    };

    // 发送验证码
    const handleSendCode = async () => {
        const phoneToValidate = loginMode === 'sms' ? formData.phoneNumber : formData.account;
        
        if (!validatePhoneNumber(phoneToValidate)) {
            const errorField = loginMode === 'sms' ? 'phoneNumber' : 'account';
            setErrors({ [errorField]: '请输入正确的手机号码' });
            return;
        }

        setSendingCode(true);
        try {
            const response = await fetch('/api/auth/send-verification-code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    phoneNumber: phoneToValidate
                }),
            });

            const data = await response.json();

            if (response.ok) {
                setCountdown(60);
                alert('验证码已发送，请查收');
            } else {
                const errorField = loginMode === 'sms' ? 'phoneNumber' : 'account';
                setErrors({ [errorField]: data.error || '发送验证码失败' });
            }
        } catch (error) {
            console.error('发送验证码失败:', error);
            const errorField = loginMode === 'sms' ? 'phoneNumber' : 'account';
            setErrors({ [errorField]: '网络错误，请稍后重试' });
        } finally {
            setSendingCode(false);
        }
    };

    // 处理账号登录
    const handlePasswordLogin = async () => {
        const newErrors = {};
        
        if (!validateAccount(formData.account)) {
            newErrors.account = '请输入正确的账号或手机号';
        }
        if (!formData.password || formData.password.length < 6) {
            newErrors.password = '密码至少6位';
        }

        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            return;
        }

        try {
            const response = await fetch('/api/auth/password-login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    account: formData.account,
                    password: formData.password
                }),
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
                alert('登录成功！');
                onLoginSuccess && onLoginSuccess(data.user);
            } else {
                setErrors({ general: data.error || '登录失败' });
            }
        } catch (error) {
            console.error('登录失败:', error);
            setErrors({ general: '网络错误，请稍后重试' });
        }
    };

    // 处理短信登录
    const handleSmsLogin = async () => {
        const newErrors = {};
        
        if (!validatePhoneNumber(formData.phoneNumber)) {
            newErrors.phoneNumber = '请输入正确的手机号码';
        }
        if (!formData.verificationCode || formData.verificationCode.length !== 6) {
            newErrors.verificationCode = '请输入6位验证码';
        }

        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            return;
        }

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    phoneNumber: formData.phoneNumber,
                    verificationCode: formData.verificationCode
                }),
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
                alert('登录成功！');
                onLoginSuccess && onLoginSuccess(data.user);
            } else {
                if (data.error === '该手机号未注册，请先完成注册') {
                    setErrors({ general: data.error });
                } else {
                    setErrors({ verificationCode: data.error || '登录失败' });
                }
            }
        } catch (error) {
            console.error('登录失败:', error);
            setErrors({ general: '网络错误，请稍后重试' });
        }
    };

    // 处理登录提交
    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        
        try {
            if (loginMode === 'password') {
                await handlePasswordLogin();
            } else {
                await handleSmsLogin();
            }
        } finally {
            setLoading(false);
        }
    };

    // 处理跳转到注册页面
    const handleSwitchToRegister = (e) => {
        e.preventDefault(); // 防止默认的链接跳转行为
        
        try {
            if (typeof onSwitchToRegister === 'function') {
                onSwitchToRegister();
            } else {
                console.error('注册页面跳转函数未定义');
                setErrors({ general: '页面跳转失败，请刷新页面后重试' });
            }
        } catch (error) {
            console.error('跳转到注册页面失败:', error);
            setErrors({ general: '页面跳转失败，请稍后重试' });
        }
    };

    return (
        <div className="unified-login-container">
            <div className="login-header">
                <h2>登录</h2>
                <div className="login-tabs">
                    <span 
                        className={`tab ${loginMode === 'password' ? 'active' : ''}`}
                        onClick={() => switchLoginMode('password')}
                    >
                        账号登录
                    </span>
                    <span 
                        className={`tab ${loginMode === 'sms' ? 'active' : ''}`}
                        onClick={() => switchLoginMode('sms')}
                    >
                        短信登录
                    </span>
                </div>
            </div>

            <form onSubmit={handleLogin} className="login-form">
                {errors.general && (
                    <div className="error-message general-error">
                        {errors.general}
                    </div>
                )}

                {loginMode === 'password' ? (
                    // 账号登录模式
                    <>
                        <div className="form-group">
                            <div className="input-container">
                                <input
                                    type="text"
                                    name="account"
                                    placeholder="请输入账号/手机号"
                                    value={formData.account}
                                    onChange={handleInputChange}
                                    className={errors.account ? 'error' : ''}
                                />
                            </div>
                            {errors.account && (
                                <div className="error-message">{errors.account}</div>
                            )}
                        </div>

                        <div className="form-group">
                            <div className="input-container">
                                <input
                                    type="password"
                                    name="password"
                                    placeholder="请输入密码"
                                    value={formData.password}
                                    onChange={handleInputChange}
                                    className={errors.password ? 'error' : ''}
                                />
                            </div>
                            {errors.password && (
                                <div className="error-message">{errors.password}</div>
                            )}
                        </div>
                    </>
                ) : (
                    // 短信登录模式
                    <>
                        <div className="form-group">
                            <div className="phone-input-container">
                                <select className="country-code">
                                    <option value="+86">+86</option>
                                </select>
                                <input
                                    type="tel"
                                    name="phoneNumber"
                                    placeholder="请输入手机号"
                                    value={formData.phoneNumber}
                                    onChange={handleInputChange}
                                    className={errors.phoneNumber ? 'error' : ''}
                                    maxLength="11"
                                />
                            </div>
                            {errors.phoneNumber && (
                                <div className="error-message">{errors.phoneNumber}</div>
                            )}
                        </div>

                        <div className="form-group">
                            <div className="verification-input-container">
                                <input
                                    type="text"
                                    name="verificationCode"
                                    placeholder="请输入验证码"
                                    value={formData.verificationCode}
                                    onChange={handleInputChange}
                                    className={errors.verificationCode ? 'error' : ''}
                                    maxLength="6"
                                />
                                <button
                                    type="button"
                                    className="send-code-btn"
                                    onClick={handleSendCode}
                                    disabled={sendingCode || countdown > 0 || !formData.phoneNumber}
                                >
                                    {sendingCode ? '发送中...' : countdown > 0 ? `${countdown}s` : '获取验证码'}
                                </button>
                            </div>
                            {errors.verificationCode && (
                                <div className="error-message">{errors.verificationCode}</div>
                            )}
                        </div>
                    </>
                )}

                <button
                    type="submit"
                    className="login-btn"
                    disabled={loading}
                >
                    {loading ? '登录中...' : '登录'}
                </button>

                <div className="login-footer">
                    <div className="remember-forgot">
                        <label className="remember-me">
                            <input type="checkbox" />
                            <span>记住登录</span>
                        </label>
                        <a href="#" className="forgot-password">忘记密码</a>
                    </div>
                    
                    <div className="register-link">
                        <span>还没有账号？</span>
                        <a 
                            href="#" 
                            onClick={handleSwitchToRegister} 
                            className="free-register"
                            role="button"
                            aria-label="跳转到注册页面"
                        >
                            免费注册
                        </a>
                    </div>
                    
                    <div className="agreement">
                        <span>登录即表示您同意淘宝</span>
                        <a href="#">《服务协议》</a>
                        <span>和</span>
                        <a href="#">《隐私政策》</a>
                    </div>
                </div>
            </form>
        </div>
    );
};

export default UnifiedLogin;
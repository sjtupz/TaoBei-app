import React, { useState, useEffect } from 'react';
import './Register.css';

const Register = ({ onRegisterSuccess, onSwitchToLogin }) => {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        confirmPassword: '',
        phoneNumber: '',
        verificationCode: '',
        agreeToTerms: false
    });
    const [errors, setErrors] = useState({});
    const [loading, setLoading] = useState(false);
    const [sendingCode, setSendingCode] = useState(false);
    const [countdown, setCountdown] = useState(0);
    const [passwordStrength, setPasswordStrength] = useState({
        score: 0,
        feedback: '请输入密码'
    });

    // 倒计时效果
    useEffect(() => {
        let timer;
        if (countdown > 0) {
            timer = setTimeout(() => setCountdown(countdown - 1), 1000);
        }
        return () => clearTimeout(timer);
    }, [countdown]);

    // 密码强度检测
    const checkPasswordStrength = (password) => {
        if (!password) {
            return { score: 0, feedback: '请输入密码' };
        }
        
        let score = 0;
        let feedback = '';
        
        // 长度检查
        if (password.length >= 8) score += 1;
        else return { score: 0, feedback: '密码至少需要8位字符' };
        
        // 包含数字
        if (/\d/.test(password)) score += 1;
        
        // 包含小写字母
        if (/[a-z]/.test(password)) score += 1;
        
        // 包含大写字母
        if (/[A-Z]/.test(password)) score += 1;
        
        // 包含特殊字符
        if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score += 1;
        
        switch (score) {
            case 0:
            case 1:
                feedback = '密码强度：弱';
                break;
            case 2:
            case 3:
                feedback = '密码强度：中等';
                break;
            case 4:
            case 5:
                feedback = '密码强度：强';
                break;
            default:
                feedback = '密码强度：弱';
        }
        
        return { score, feedback };
    };

    // 验证手机号
    const validatePhoneNumber = (phone) => {
        const phoneRegex = /^1[3-9]\d{9}$/;
        return phoneRegex.test(phone);
    };

    // 验证用户名
    const validateUsername = (username) => {
        const usernameRegex = /^[a-zA-Z0-9_\u4e00-\u9fa5]{2,20}$/;
        return usernameRegex.test(username);
    };

    // 处理输入变化
    const handleInputChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
        
        // 密码强度检测
        if (name === 'password') {
            setPasswordStrength(checkPasswordStrength(value));
        }
        
        // 清除对应字段的错误
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    // 发送验证码
    const sendVerificationCode = async () => {
        if (!validatePhoneNumber(formData.phoneNumber)) {
            setErrors(prev => ({
                ...prev,
                phoneNumber: '请输入正确的手机号码'
            }));
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
                    phoneNumber: formData.phoneNumber,
                    type: 'register'
                }),
            });

            if (response.ok) {
                setCountdown(60);
                setErrors(prev => ({
                    ...prev,
                    phoneNumber: ''
                }));
            } else {
                const errorData = await response.json();
                setErrors(prev => ({
                    ...prev,
                    phoneNumber: errorData.message || '发送验证码失败'
                }));
            }
        } catch (error) {
            console.error('发送验证码错误:', error);
            setErrors(prev => ({
                ...prev,
                phoneNumber: '网络错误，请稍后重试'
            }));
        } finally {
            setSendingCode(false);
        }
    };

    // 处理返回登录页面
    const handleSwitchToLogin = (e) => {
        e.preventDefault(); // 防止默认的链接跳转行为
        
        try {
            if (typeof onSwitchToLogin === 'function') {
                onSwitchToLogin();
            } else {
                console.error('登录页面跳转函数未定义');
                setErrors({ general: '页面跳转失败，请刷新页面后重试' });
            }
        } catch (error) {
            console.error('跳转到登录页面失败:', error);
            setErrors({ general: '页面跳转失败，请稍后重试' });
        }
    };

    // 处理注册
    const handleRegister = async (e) => {
        e.preventDefault();
        
        // 表单验证
        const newErrors = {};
        
        // 用户名验证
        if (!formData.username) {
            newErrors.username = '请输入用户名';
        } else if (!validateUsername(formData.username)) {
            newErrors.username = '用户名只能包含字母、数字、下划线和中文，长度2-20位';
        }
        
        // 密码验证
        if (!formData.password) {
            newErrors.password = '请输入密码';
        } else if (formData.password.length < 8) {
            newErrors.password = '密码至少需要8位字符';
        }
        
        // 确认密码验证
        if (!formData.confirmPassword) {
            newErrors.confirmPassword = '请确认密码';
        } else if (formData.password !== formData.confirmPassword) {
            newErrors.confirmPassword = '两次输入的密码不一致';
        }
        
        // 手机号验证
        if (!validatePhoneNumber(formData.phoneNumber)) {
            newErrors.phoneNumber = '请输入正确的手机号码';
        }
        
        // 验证码验证
        if (!formData.verificationCode) {
            newErrors.verificationCode = '请输入验证码';
        }
        
        // 协议验证
        if (!formData.agreeToTerms) {
            newErrors.agreeToTerms = '请同意用户协议和隐私政策';
        }
        
        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            return;
        }

        setLoading(true);
        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: formData.username,
                    password: formData.password,
                    phoneNumber: formData.phoneNumber,
                    verificationCode: formData.verificationCode
                }),
            });

            if (response.ok) {
                const userData = await response.json();
                onRegisterSuccess(userData);
            } else {
                const errorData = await response.json();
                setErrors(prev => ({
                    ...prev,
                    general: errorData.message || '注册失败，请重试'
                }));
            }
        } catch (error) {
            console.error('注册错误:', error);
            setErrors(prev => ({
                ...prev,
                general: '网络错误，请稍后重试'
            }));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="register-container">
            <div className="register-header">
                <h2>用户注册</h2>
                <p>创建您的账户，开始使用我们的服务</p>
            </div>

            <form onSubmit={handleRegister} className="register-form">
                {/* 通用错误提示 */}
                {errors.general && (
                    <div className="error-message general-error">
                        {errors.general}
                    </div>
                )}

                {/* 用户名输入 */}
                <div className="form-group">
                    <label htmlFor="username">用户名</label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        value={formData.username}
                        onChange={handleInputChange}
                        placeholder="请输入用户名"
                        className={errors.username ? 'error' : ''}
                        maxLength="20"
                    />
                    {errors.username && (
                        <div className="error-message">{errors.username}</div>
                    )}
                </div>

                {/* 密码输入 */}
                <div className="form-group">
                    <label htmlFor="password">密码</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        value={formData.password}
                        onChange={handleInputChange}
                        placeholder="请输入密码"
                        className={errors.password ? 'error' : ''}
                    />
                    {/* 密码强度提示 */}
                    <div className={`password-strength strength-${passwordStrength.score}`}>
                        <div className="strength-bar">
                            <div className="strength-fill"></div>
                        </div>
                        <span className="strength-text">{passwordStrength.feedback}</span>
                    </div>
                    {errors.password && (
                        <div className="error-message">{errors.password}</div>
                    )}
                </div>

                {/* 确认密码输入 */}
                <div className="form-group">
                    <label htmlFor="confirmPassword">确认密码</label>
                    <input
                        type="password"
                        id="confirmPassword"
                        name="confirmPassword"
                        value={formData.confirmPassword}
                        onChange={handleInputChange}
                        placeholder="请再次输入密码"
                        className={errors.confirmPassword ? 'error' : ''}
                    />
                    {errors.confirmPassword && (
                        <div className="error-message">{errors.confirmPassword}</div>
                    )}
                </div>

                {/* 手机号输入 */}
                <div className="form-group">
                    <label htmlFor="phoneNumber">手机号码</label>
                    <div className="phone-input-group">
                        <select className="country-code">
                            <option value="+86">+86</option>
                        </select>
                        <input
                            type="tel"
                            id="phoneNumber"
                            name="phoneNumber"
                            value={formData.phoneNumber}
                            onChange={handleInputChange}
                            placeholder="请输入手机号码"
                            className={errors.phoneNumber ? 'error' : ''}
                            maxLength="11"
                        />
                    </div>
                    {errors.phoneNumber && (
                        <div className="error-message">{errors.phoneNumber}</div>
                    )}
                </div>

                {/* 验证码输入 */}
                <div className="form-group">
                    <label htmlFor="verificationCode">验证码</label>
                    <div className="verification-input-group">
                        <input
                            type="text"
                            id="verificationCode"
                            name="verificationCode"
                            value={formData.verificationCode}
                            onChange={handleInputChange}
                            placeholder="请输入验证码"
                            className={errors.verificationCode ? 'error' : ''}
                            maxLength="6"
                        />
                        <button
                            type="button"
                            className="send-code-btn"
                            onClick={sendVerificationCode}
                            disabled={sendingCode || countdown > 0 || !formData.phoneNumber}
                        >
                            {sendingCode ? '发送中...' : countdown > 0 ? `${countdown}s` : '发送验证码'}
                        </button>
                    </div>
                    {errors.verificationCode && (
                        <div className="error-message">{errors.verificationCode}</div>
                    )}
                </div>

                {/* 用户协议 */}
                <div className="form-group agreement-group">
                    <label className="checkbox-label">
                        <input
                            type="checkbox"
                            name="agreeToTerms"
                            checked={formData.agreeToTerms}
                            onChange={handleInputChange}
                            className={errors.agreeToTerms ? 'error' : ''}
                        />
                        <span className="checkmark"></span>
                        我已阅读并同意
                        <a href="/terms" target="_blank" rel="noopener noreferrer">《用户协议》</a>
                        和
                        <a href="/privacy" target="_blank" rel="noopener noreferrer">《隐私政策》</a>
                    </label>
                    {errors.agreeToTerms && (
                        <div className="error-message">{errors.agreeToTerms}</div>
                    )}
                </div>

                {/* 注册按钮 */}
                <button
                    type="submit"
                    className="register-btn"
                    disabled={loading}
                >
                    {loading ? '注册中...' : '立即注册'}
                </button>

                {/* 返回登录 */}
                <div className="login-link">
                    <span>已有账户？</span>
                    <a 
                        href="#" 
                        onClick={handleSwitchToLogin}
                        className="back-to-login"
                        role="button"
                        aria-label="返回登录页面"
                    >
                        立即登录
                    </a>
                </div>
            </form>
        </div>
    );
};

export default Register;
import React, { useState, useEffect } from 'react';
import './Register.css';

const Register = ({ onRegisterSuccess, onSwitchToLogin }) => {
    const [formData, setFormData] = useState({
        phoneNumber: '',
        verificationCode: '',
        agreeToTerms: false
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

    // 处理输入变化
    const handleInputChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
        
        // 清除对应字段的错误
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    // 发送验证码
    const handleSendCode = async () => {
        if (!validatePhoneNumber(formData.phoneNumber)) {
            setErrors({ phoneNumber: '请输入正确的手机号码' });
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
                    phoneNumber: formData.phoneNumber
                }),
            });

            const data = await response.json();

            if (response.ok) {
                setCountdown(60);
                alert('验证码已发送，请查收');
            } else {
                setErrors({ phoneNumber: data.error || '发送验证码失败' });
            }
        } catch (error) {
            console.error('发送验证码失败:', error);
            setErrors({ phoneNumber: '网络错误，请稍后重试' });
        } finally {
            setSendingCode(false);
        }
    };

    // 处理注册
    const handleRegister = async (e) => {
        e.preventDefault();
        
        // 表单验证
        const newErrors = {};
        if (!validatePhoneNumber(formData.phoneNumber)) {
            newErrors.phoneNumber = '请输入正确的手机号码';
        }
        if (!formData.verificationCode || formData.verificationCode.length !== 6) {
            newErrors.verificationCode = '请输入6位验证码';
        }
        if (!formData.agreeToTerms) {
            newErrors.agreeToTerms = '请同意用户协议';
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
                    ...formData,
                    agreeToTerms: formData.agreeToTerms.toString()
                }),
            });

            const data = await response.json();

            if (response.ok) {
                // 保存token到localStorage
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
                
                alert(data.message);
                onRegisterSuccess && onRegisterSuccess(data.user);
            } else {
                setErrors({ verificationCode: data.error || '注册失败' });
            }
        } catch (error) {
            console.error('注册失败:', error);
            setErrors({ general: '网络错误，请稍后重试' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="register-container">
            <div className="register-header">
                <h2>短信登录</h2>
                <div className="register-tabs">
                    <span className="tab" onClick={onSwitchToLogin}>密码登录</span>
                    <span className="tab active">短信登录</span>
                </div>
            </div>

            <form onSubmit={handleRegister} className="register-form">
                {errors.general && (
                    <div className="error-message general-error">
                        {errors.general}
                    </div>
                )}

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

                <div className="form-group">
                    <label className="agreement-checkbox">
                        <input
                            type="checkbox"
                            name="agreeToTerms"
                            checked={formData.agreeToTerms}
                            onChange={handleInputChange}
                        />
                        <span className="checkmark"></span>
                        <span className="agreement-text">
                            我已阅读并同意
                            <a href="#" className="agreement-link">《淘宝服务协议》</a>
                            和
                            <a href="#" className="agreement-link">《隐私权政策》</a>
                        </span>
                    </label>
                    {errors.agreeToTerms && (
                        <div className="error-message">{errors.agreeToTerms}</div>
                    )}
                </div>

                <button
                    type="submit"
                    className="register-btn"
                    disabled={loading}
                >
                    {loading ? '登录中...' : '登录'}
                </button>

                <div className="register-footer">
                    <div className="other-login">
                        <div className="divider">
                            <span>其他登录方式</span>
                        </div>
                        <div className="social-login">
                            <button type="button" className="social-btn wechat">
                                <span>微信</span>
                            </button>
                            <button type="button" className="social-btn qq">
                                <span>QQ</span>
                            </button>
                            <button type="button" className="social-btn weibo">
                                <span>微博</span>
                            </button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    );
};

export default Register;
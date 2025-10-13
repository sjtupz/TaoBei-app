const express = require('express');
const rateLimit = require('express-rate-limit');
const { body, validationResult } = require('express-validator');
const { userDAO, verificationCodeDAO } = require('../../database');
const { 
    generateVerificationCode, 
    validatePhoneNumber, 
    generateToken,
    authenticateToken 
} = require('../utils/auth');

const router = express.Router();

// 发送验证码的频率限制
const sendCodeLimiter = rateLimit({
    windowMs: 60 * 1000, // 1分钟
    max: 1, // 每个IP每分钟最多1次
    message: { error: '请求过于频繁，请稍后再试' },
    standardHeaders: true,
    legacyHeaders: false,
});

// API-POST-SendVerificationCode: 发送验证码到指定手机号
router.post('/send-verification-code', 
    sendCodeLimiter,
    [
        body('phoneNumber')
            .notEmpty()
            .withMessage('手机号不能为空')
            .custom((value) => {
                if (!validatePhoneNumber(value)) {
                    throw new Error('请输入正确的手机号码');
                }
                return true;
            })
    ],
    async (req, res) => {
        try {
            // 验证请求参数
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({ 
                    error: errors.array()[0].msg 
                });
            }

            const { phoneNumber } = req.body;

            // 检查发送频率限制
            const isRateLimited = await verificationCodeDAO.checkRateLimit(phoneNumber, 60);
            if (isRateLimited) {
                return res.status(429).json({ 
                    error: '请求过于频繁，请稍后再试' 
                });
            }

            // 生成验证码
            const code = generateVerificationCode();
            
            // 保存验证码到数据库
            await verificationCodeDAO.createVerificationCode(phoneNumber, code, 60);
            
            // 在控制台打印验证码（开发调试用）
            console.log(`验证码发送成功 - 手机号: ${phoneNumber}, 验证码: ${code}`);

            res.status(200).json({
                message: '验证码已发送',
                expiresIn: 60
            });

        } catch (error) {
            console.error('发送验证码失败:', error);
            res.status(500).json({ error: '服务器内部错误' });
        }
    }
);

// API-POST-Login: 用户登录
router.post('/login',
    [
        body('phoneNumber')
            .notEmpty()
            .withMessage('手机号不能为空')
            .custom((value) => {
                if (!validatePhoneNumber(value)) {
                    throw new Error('请输入正确的手机号码');
                }
                return true;
            }),
        body('verificationCode')
            .notEmpty()
            .withMessage('验证码不能为空')
            .isLength({ min: 6, max: 6 })
            .withMessage('验证码必须是6位数字')
    ],
    async (req, res) => {
        try {
            // 验证请求参数
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({ 
                    error: errors.array()[0].msg 
                });
            }

            const { phoneNumber, verificationCode } = req.body;

            // 验证验证码
            const codeVerification = await verificationCodeDAO.verifyCode(phoneNumber, verificationCode);
            if (!codeVerification.valid) {
                return res.status(400).json({ 
                    error: codeVerification.reason 
                });
            }

            // 检查用户是否已注册
            const user = await userDAO.findUserByPhone(phoneNumber);
            if (!user) {
                return res.status(400).json({ 
                    error: '该手机号未注册，请先完成注册' 
                });
            }

            // 生成JWT token
            const token = generateToken({
                userId: user.id,
                phoneNumber: user.phone_number
            });

            res.status(200).json({
                message: '登录成功',
                token,
                user: {
                    id: user.id,
                    phoneNumber: user.phone_number,
                    nickname: user.nickname,
                    avatar: user.avatar
                }
            });

        } catch (error) {
            console.error('登录失败:', error);
            res.status(500).json({ error: '服务器内部错误' });
        }
    }
);

// API-POST-Register: 用户注册
router.post('/register',
    [
        body('phoneNumber')
            .notEmpty()
            .withMessage('手机号不能为空')
            .custom((value) => {
                if (!validatePhoneNumber(value)) {
                    throw new Error('请输入正确的手机号码');
                }
                return true;
            }),
        body('verificationCode')
            .notEmpty()
            .withMessage('验证码不能为空')
            .isLength({ min: 6, max: 6 })
            .withMessage('验证码必须是6位数字'),
        body('agreeToTerms')
            .equals('true')
            .withMessage('必须同意用户协议')
    ],
    async (req, res) => {
        try {
            // 验证请求参数
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({ 
                    error: errors.array()[0].msg 
                });
            }

            const { phoneNumber, verificationCode, agreeToTerms } = req.body;

            // 验证验证码
            const codeVerification = await verificationCodeDAO.verifyCode(phoneNumber, verificationCode);
            if (!codeVerification.valid) {
                return res.status(400).json({ 
                    error: codeVerification.reason 
                });
            }

            // 检查用户是否已注册
            const existingUser = await userDAO.findUserByPhone(phoneNumber);
            if (existingUser) {
                // 如果已注册，直接登录
                const token = generateToken({
                    userId: existingUser.id,
                    phoneNumber: existingUser.phone_number
                });

                return res.status(200).json({
                    message: '该手机号已注册，将直接为您登录',
                    token,
                    user: {
                        id: existingUser.id,
                        phoneNumber: existingUser.phone_number,
                        nickname: existingUser.nickname,
                        avatar: existingUser.avatar
                    }
                });
            }

            // 创建新用户
            const newUser = await userDAO.createUser(phoneNumber);
            
            // 生成JWT token
            const token = generateToken({
                userId: newUser.id,
                phoneNumber: newUser.phone_number
            });

            res.status(201).json({
                message: '注册成功',
                token,
                user: {
                    id: newUser.id,
                    phoneNumber: newUser.phone_number,
                    nickname: newUser.nickname,
                    avatar: newUser.avatar
                }
            });

        } catch (error) {
            console.error('注册失败:', error);
            res.status(500).json({ error: '服务器内部错误' });
        }
    }
);

// API-POST-Logout: 用户退出登录
router.post('/logout', authenticateToken, async (req, res) => {
    try {
        // 在实际应用中，可以将token加入黑名单
        // 这里简单返回成功响应
        res.status(200).json({
            message: '退出登录成功'
        });
    } catch (error) {
        console.error('退出登录失败:', error);
        res.status(500).json({ error: '服务器内部错误' });
    }
});

module.exports = router;
const express = require('express');
const { body, validationResult } = require('express-validator');
const { userDAO } = require('../../database');
const { authenticateToken } = require('../utils/auth');

const router = express.Router();

// API-GET-UserProfile: 获取用户个人信息
router.get('/profile', authenticateToken, async (req, res) => {
    try {
        const { userId } = req.user;
        
        const user = await userDAO.getUserById(userId);
        if (!user) {
            return res.status(404).json({ error: '用户不存在' });
        }

        res.status(200).json({
            message: '获取用户信息成功',
            data: {
                id: user.id,
                phoneNumber: user.phone_number,
                nickname: user.nickname,
                avatar: user.avatar,
                createdAt: user.created_at,
                updatedAt: user.updated_at
            }
        });

    } catch (error) {
        console.error('获取用户信息失败:', error);
        res.status(500).json({ error: '服务器内部错误' });
    }
});

// API-PUT-UpdateUserProfile: 更新用户个人信息
router.put('/profile', 
    authenticateToken,
    [
        body('nickname')
            .optional()
            .isLength({ min: 1, max: 50 })
            .withMessage('昵称长度必须在1-50个字符之间'),
        body('avatar')
            .optional()
            .isURL()
            .withMessage('头像必须是有效的URL地址')
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

            const { phoneNumber } = req.user;
            const { nickname, avatar } = req.body;

            // 构建更新数据
            const updates = {};
            if (nickname !== undefined) updates.nickname = nickname;
            if (avatar !== undefined) updates.avatar = avatar;

            if (Object.keys(updates).length === 0) {
                return res.status(400).json({ error: '没有提供要更新的字段' });
            }

            // 更新用户信息
            const updatedUser = await userDAO.updateUserProfile(phoneNumber, updates);

            res.status(200).json({
                message: '用户信息更新成功',
                data: {
                    id: updatedUser.id,
                    phoneNumber: updatedUser.phone_number,
                    nickname: updatedUser.nickname,
                    avatar: updatedUser.avatar,
                    updatedAt: updatedUser.updated_at
                }
            });

        } catch (error) {
            console.error('更新用户信息失败:', error);
            
            if (error.message === '用户不存在') {
                return res.status(404).json({ error: '用户不存在' });
            }
            
            res.status(500).json({ error: '服务器内部错误' });
        }
    }
);

module.exports = router;
const express = require('express');
const { body, param, validationResult } = require('express-validator');
const { cartDAO, productDAO } = require('../../database');
const { authenticateToken } = require('../utils/auth');

const router = express.Router();

// API-GET-Cart: 获取用户购物车
router.get('/', authenticateToken, async (req, res) => {
    try {
        const { userId } = req.user;
        const cart = await cartDAO.getCartByUserId(userId);

        res.status(200).json({
            code: 200,
            data: cart
        });

    } catch (error) {
        console.error('获取购物车失败:', error);
        res.status(500).json({ error: '服务器内部错误' });
    }
});

// API-POST-AddToCart: 添加商品到购物车
router.post('/add',
    authenticateToken,
    [
        body('product_id')
            .isInt({ min: 1 })
            .withMessage('商品ID必须是大于0的整数'),
        body('quantity')
            .isInt({ min: 1 })
            .withMessage('数量必须是大于0的整数')
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

            const { userId } = req.user;
            const { product_id, quantity } = req.body;

            // 检查商品是否存在
            const product = await productDAO.getProductById(product_id);
            if (!product) {
                return res.status(404).json({ 
                    error: '商品不存在' 
                });
            }

            // 检查库存
            const stockCheck = await productDAO.checkProductStock(product_id, quantity);
            if (!stockCheck.valid) {
                return res.status(400).json({ 
                    error: stockCheck.reason 
                });
            }

            // 添加到购物车
            await cartDAO.addToCart(userId, product_id, quantity);

            // 获取更新后的购物车
            const cart = await cartDAO.getCartByUserId(userId);

            res.status(200).json({
                code: 200,
                message: '添加成功',
                data: cart
            });

        } catch (error) {
            console.error('添加到购物车失败:', error);
            res.status(500).json({ error: '服务器内部错误' });
        }
    }
);

// API-PUT-UpdateCartItem: 更新购物车商品数量
router.put('/item/:id',
    authenticateToken,
    [
        param('id')
            .isInt({ min: 1 })
            .withMessage('购物车项ID必须是大于0的整数'),
        body('quantity')
            .isInt({ min: 0 })
            .withMessage('数量必须是大于等于0的整数')
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

            const { userId } = req.user;
            const { id } = req.params;
            const { quantity } = req.body;

            // 检查购物车项是否存在
            const cartItem = await cartDAO.getCartItem(parseInt(id), userId);
            if (!cartItem) {
                return res.status(404).json({ 
                    error: '购物车项不存在' 
                });
            }

            // 如果数量大于0，检查库存
            if (quantity > 0) {
                const stockCheck = await productDAO.checkProductStock(cartItem.product_id, quantity);
                if (!stockCheck.valid) {
                    return res.status(400).json({ 
                        error: stockCheck.reason 
                    });
                }
            }

            // 更新购物车项
            const updated = await cartDAO.updateCartItem(parseInt(id), userId, quantity);
            if (!updated) {
                return res.status(404).json({ 
                    error: '购物车项不存在' 
                });
            }

            // 获取更新后的购物车
            const cart = await cartDAO.getCartByUserId(userId);

            res.status(200).json({
                code: 200,
                message: '更新成功',
                data: cart
            });

        } catch (error) {
            console.error('更新购物车失败:', error);
            res.status(500).json({ error: '服务器内部错误' });
        }
    }
);

// API-DELETE-CartItem: 删除购物车商品
router.delete('/item/:id',
    authenticateToken,
    [
        param('id')
            .isInt({ min: 1 })
            .withMessage('购物车项ID必须是大于0的整数')
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

            const { userId } = req.user;
            const { id } = req.params;

            // 删除购物车项
            const deleted = await cartDAO.removeFromCart(parseInt(id), userId);
            if (!deleted) {
                return res.status(404).json({ 
                    error: '购物车项不存在' 
                });
            }

            res.status(200).json({
                code: 200,
                message: '删除成功'
            });

        } catch (error) {
            console.error('删除购物车商品失败:', error);
            res.status(500).json({ error: '服务器内部错误' });
        }
    }
);

module.exports = router;
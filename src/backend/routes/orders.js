const express = require('express');
const { body, param, query, validationResult } = require('express-validator');
const { orderDAO, cartDAO, productDAO } = require('../../database');
const { authenticateToken } = require('../utils/auth');

const router = express.Router();

// API-POST-CreateOrder: 创建订单
router.post('/',
    authenticateToken,
    [
        body('items')
            .isArray({ min: 1 })
            .withMessage('订单商品列表不能为空'),
        body('items.*.product_id')
            .isInt({ min: 1 })
            .withMessage('商品ID必须是大于0的整数'),
        body('items.*.quantity')
            .isInt({ min: 1 })
            .withMessage('商品数量必须是大于0的整数'),
        body('shippingAddress')
            .notEmpty()
            .withMessage('收货地址不能为空')
            .isLength({ max: 500 })
            .withMessage('收货地址长度不能超过500个字符')
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
            const { items, shippingAddress } = req.body;

            // 验证商品存在性和库存
            let totalAmount = 0;
            const validatedItems = [];

            for (const item of items) {
                const product = await productDAO.getProductById(item.product_id);
                if (!product) {
                    return res.status(400).json({ 
                        error: `商品ID ${item.product_id} 不存在` 
                    });
                }

                const stockCheck = await productDAO.checkProductStock(item.product_id, item.quantity);
                if (!stockCheck.valid) {
                    return res.status(400).json({ 
                        error: `商品 ${product.name} ${stockCheck.reason}` 
                    });
                }

                const itemTotal = product.price * item.quantity;
                totalAmount += itemTotal;

                validatedItems.push({
                    product_id: item.product_id,
                    quantity: item.quantity,
                    price: product.price
                });
            }

            // 创建订单
            const order = await orderDAO.createOrder(userId, validatedItems, shippingAddress, totalAmount);

            // 更新商品库存
            for (const item of validatedItems) {
                await productDAO.updateProductStock(item.product_id, item.quantity);
            }

            // 清空购物车（如果订单来自购物车）
            await cartDAO.clearCart(userId);

            res.status(201).json({
                code: 201,
                message: '订单创建成功',
                data: order
            });

        } catch (error) {
            console.error('创建订单失败:', error);
            res.status(500).json({ error: '服务器内部错误' });
        }
    }
);

// API-GET-OrderList: 获取用户订单列表
router.get('/',
    authenticateToken,
    [
        query('page')
            .optional()
            .isInt({ min: 1 })
            .withMessage('页码必须是大于0的整数'),
        query('pageSize')
            .optional()
            .isInt({ min: 1, max: 100 })
            .withMessage('每页数量必须是1-100之间的整数'),
        query('status')
            .optional()
            .isIn(['pending', 'paid', 'shipped', 'delivered', 'cancelled'])
            .withMessage('订单状态必须是pending、paid、shipped、delivered或cancelled')
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
            const {
                page = 1,
                pageSize = 10,
                status = ''
            } = req.query;

            const result = await orderDAO.getOrdersByUserId(userId, {
                page: parseInt(page),
                pageSize: parseInt(pageSize),
                status
            });

            res.status(200).json({
                code: 200,
                data: result
            });

        } catch (error) {
            console.error('获取订单列表失败:', error);
            res.status(500).json({ error: '服务器内部错误' });
        }
    }
);

// API-GET-OrderDetail: 获取订单详情
router.get('/:id',
    authenticateToken,
    [
        param('id')
            .isInt({ min: 1 })
            .withMessage('订单ID必须是大于0的整数')
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

            const order = await orderDAO.getOrderById(parseInt(id), userId);
            if (!order) {
                return res.status(404).json({ 
                    error: '订单不存在' 
                });
            }

            res.status(200).json({
                code: 200,
                data: order
            });

        } catch (error) {
            console.error('获取订单详情失败:', error);
            res.status(500).json({ error: '服务器内部错误' });
        }
    }
);

// API-PUT-CancelOrder: 取消订单
router.put('/:id/cancel',
    authenticateToken,
    [
        param('id')
            .isInt({ min: 1 })
            .withMessage('订单ID必须是大于0的整数')
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

            try {
                const success = await orderDAO.cancelOrder(parseInt(id), userId);
                if (!success) {
                    return res.status(404).json({ 
                        error: '订单不存在' 
                    });
                }

                res.status(200).json({
                    code: 200,
                    message: '订单取消成功'
                });

            } catch (orderError) {
                if (orderError.message === '订单不存在') {
                    return res.status(404).json({ 
                        error: '订单不存在' 
                    });
                } else if (orderError.message === '订单状态不允许取消') {
                    return res.status(400).json({ 
                        error: '订单状态不允许取消' 
                    });
                } else {
                    throw orderError;
                }
            }

        } catch (error) {
            console.error('取消订单失败:', error);
            res.status(500).json({ error: '服务器内部错误' });
        }
    }
);

module.exports = router;
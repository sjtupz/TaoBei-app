const express = require('express');
const { query, param, validationResult } = require('express-validator');
const { productDAO } = require('../../database');

const router = express.Router();

// API-GET-ProductList: 获取商品列表
router.get('/',
    [
        query('page')
            .optional()
            .isInt({ min: 1 })
            .withMessage('页码必须是大于0的整数'),
        query('pageSize')
            .optional()
            .isInt({ min: 1, max: 100 })
            .withMessage('每页数量必须是1-100之间的整数'),
        query('keyword')
            .optional()
            .isLength({ max: 100 })
            .withMessage('搜索关键词长度不能超过100个字符'),
        query('category')
            .optional()
            .isLength({ max: 50 })
            .withMessage('分类名称长度不能超过50个字符'),
        query('sortBy')
            .optional()
            .isIn(['name', 'price', 'created_at', 'stock'])
            .withMessage('排序字段必须是name、price、created_at或stock'),
        query('sortOrder')
            .optional()
            .isIn(['ASC', 'DESC', 'asc', 'desc'])
            .withMessage('排序方向必须是ASC或DESC')
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

            const {
                page = 1,
                pageSize = 10,
                keyword = '',
                category = '',
                sortBy = 'created_at',
                sortOrder = 'DESC'
            } = req.query;

            const result = await productDAO.getProductList({
                page: parseInt(page),
                pageSize: parseInt(pageSize),
                keyword,
                category,
                sortBy,
                sortOrder: sortOrder.toUpperCase()
            });

            res.status(200).json({
                code: 200,
                data: result
            });

        } catch (error) {
            console.error('获取商品列表失败:', error);
            res.status(500).json({ error: '服务器内部错误' });
        }
    }
);

// API-GET-ProductDetail: 获取商品详情
router.get('/:id',
    [
        param('id')
            .isInt({ min: 1 })
            .withMessage('商品ID必须是大于0的整数')
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

            const { id } = req.params;
            const product = await productDAO.getProductById(parseInt(id));

            if (!product) {
                return res.status(404).json({ 
                    error: '商品不存在' 
                });
            }

            res.status(200).json({
                code: 200,
                data: product
            });

        } catch (error) {
            console.error('获取商品详情失败:', error);
            res.status(500).json({ error: '服务器内部错误' });
        }
    }
);

module.exports = router;
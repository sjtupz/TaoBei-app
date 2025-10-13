const database = require('./database');

class ProductDAO {
    // 获取商品列表（支持分页、搜索、分类筛选、排序）
    async getProductList(options = {}) {
        const {
            page = 1,
            pageSize = 10,
            keyword = '',
            category = '',
            sortBy = 'created_at',
            sortOrder = 'DESC'
        } = options;

        const offset = (page - 1) * pageSize;
        let whereClause = 'WHERE 1=1';
        const params = [];

        // 关键词搜索
        if (keyword) {
            whereClause += ' AND (name LIKE ? OR description LIKE ?)';
            params.push(`%${keyword}%`, `%${keyword}%`);
        }

        // 分类筛选
        if (category) {
            whereClause += ' AND category = ?';
            params.push(category);
        }

        // 验证排序字段
        const allowedSortFields = ['name', 'price', 'created_at', 'stock'];
        const validSortBy = allowedSortFields.includes(sortBy) ? sortBy : 'created_at';
        const validSortOrder = ['ASC', 'DESC'].includes(sortOrder.toUpperCase()) ? sortOrder.toUpperCase() : 'DESC';

        // 查询商品列表
        const productsQuery = `
            SELECT id, name, description, price, stock, category, image_url, created_at, updated_at
            FROM products 
            ${whereClause}
            ORDER BY ${validSortBy} ${validSortOrder}
            LIMIT ? OFFSET ?
        `;
        params.push(pageSize, offset);

        // 查询总数
        const countQuery = `SELECT COUNT(*) as total FROM products ${whereClause}`;
        const countParams = params.slice(0, -2); // 移除LIMIT和OFFSET参数

        try {
            const [products, countResult] = await Promise.all([
                new Promise((resolve, reject) => {
                    database.db.all(productsQuery, params, (err, rows) => {
                        if (err) reject(err);
                        else resolve(rows);
                    });
                }),
                new Promise((resolve, reject) => {
                    database.db.get(countQuery, countParams, (err, row) => {
                        if (err) reject(err);
                        else resolve(row);
                    });
                })
            ]);

            return {
                products,
                total: countResult.total,
                page: parseInt(page),
                pageSize: parseInt(pageSize)
            };
        } catch (error) {
            console.error('获取商品列表失败:', error);
            throw error;
        }
    }

    // 根据ID获取商品详情
    async getProductById(productId) {
        const query = `
            SELECT id, name, description, price, stock, category, image_url, created_at, updated_at
            FROM products 
            WHERE id = ?
        `;

        return new Promise((resolve, reject) => {
            database.db.get(query, [productId], (err, row) => {
                if (err) {
                    console.error('获取商品详情失败:', err);
                    reject(err);
                } else {
                    resolve(row);
                }
            });
        });
    }

    // 更新商品库存
    async updateProductStock(productId, quantity) {
        const query = `
            UPDATE products 
            SET stock = stock - ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND stock >= ?
        `;

        return new Promise((resolve, reject) => {
            database.db.run(query, [quantity, productId, quantity], function(err) {
                if (err) {
                    console.error('更新商品库存失败:', err);
                    reject(err);
                } else {
                    resolve(this.changes > 0);
                }
            });
        });
    }

    // 检查商品库存
    async checkProductStock(productId, quantity) {
        const product = await this.getProductById(productId);
        if (!product) {
            return { valid: false, reason: '商品不存在' };
        }
        if (product.stock < quantity) {
            return { valid: false, reason: '库存不足' };
        }
        return { valid: true };
    }
}

module.exports = new ProductDAO();
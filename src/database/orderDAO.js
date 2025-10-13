const database = require('./database');

class OrderDAO {
    // 创建订单
    async createOrder(userId, items, shippingAddress, totalAmount) {
        return new Promise((resolve, reject) => {
            database.db.serialize(() => {
                database.db.run('BEGIN TRANSACTION');

                // 插入订单
                const orderQuery = `
                    INSERT INTO orders (user_id, total_amount, shipping_address, status)
                    VALUES (?, ?, ?, 'pending')
                `;

                database.db.run(orderQuery, [userId, totalAmount, shippingAddress], function(err) {
                    if (err) {
                        database.db.run('ROLLBACK');
                        console.error('创建订单失败:', err);
                        reject(err);
                        return;
                    }

                    const orderId = this.lastID;

                    // 插入订单项
                    const orderItemQuery = `
                        INSERT INTO order_items (order_id, product_id, quantity, price)
                        VALUES (?, ?, ?, ?)
                    `;

                    let completed = 0;
                    let hasError = false;

                    items.forEach(item => {
                        database.db.run(orderItemQuery, [orderId, item.product_id, item.quantity, item.price], function(err) {
                            if (err && !hasError) {
                                hasError = true;
                                database.db.run('ROLLBACK');
                                console.error('创建订单项失败:', err);
                                reject(err);
                                return;
                            }

                            completed++;
                            if (completed === items.length && !hasError) {
                                database.db.run('COMMIT', (err) => {
                                    if (err) {
                                        console.error('提交事务失败:', err);
                                        reject(err);
                                    } else {
                                        resolve({
                                            id: orderId,
                                            user_id: userId,
                                            total_amount: totalAmount,
                                            shipping_address: shippingAddress,
                                            status: 'pending',
                                            created_at: new Date().toISOString()
                                        });
                                    }
                                });
                            }
                        });
                    });
                });
            });
        });
    }

    // 获取用户订单列表
    async getOrdersByUserId(userId, options = {}) {
        const {
            page = 1,
            pageSize = 10,
            status = ''
        } = options;

        const offset = (page - 1) * pageSize;
        let whereClause = 'WHERE user_id = ?';
        const params = [userId];

        // 状态筛选
        if (status) {
            whereClause += ' AND status = ?';
            params.push(status);
        }

        // 查询订单列表
        const ordersQuery = `
            SELECT id, user_id, total_amount, status, shipping_address, created_at, updated_at
            FROM orders 
            ${whereClause}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        `;
        params.push(pageSize, offset);

        // 查询总数
        const countQuery = `SELECT COUNT(*) as total FROM orders ${whereClause}`;
        const countParams = params.slice(0, -2); // 移除LIMIT和OFFSET参数

        try {
            const [orders, countResult] = await Promise.all([
                new Promise((resolve, reject) => {
                    database.db.all(ordersQuery, params, (err, rows) => {
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
                orders,
                total: countResult.total,
                page: parseInt(page),
                pageSize: parseInt(pageSize)
            };
        } catch (error) {
            console.error('获取订单列表失败:', error);
            throw error;
        }
    }

    // 根据ID获取订单详情
    async getOrderById(orderId, userId = null) {
        let query = `
            SELECT o.id, o.user_id, o.total_amount, o.status, o.shipping_address, 
                   o.created_at, o.updated_at
            FROM orders o
            WHERE o.id = ?
        `;
        const params = [orderId];

        // 如果提供了userId，验证订单属于该用户
        if (userId) {
            query += ' AND o.user_id = ?';
            params.push(userId);
        }

        try {
            const order = await new Promise((resolve, reject) => {
                database.db.get(query, params, (err, row) => {
                    if (err) reject(err);
                    else resolve(row);
                });
            });

            if (!order) {
                return null;
            }

            // 获取订单项
            const itemsQuery = `
                SELECT oi.id, oi.product_id, oi.quantity, oi.price,
                       p.name as product_name, p.description as product_description,
                       p.image_url as product_image_url, p.category as product_category
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = ?
                ORDER BY oi.id
            `;

            const items = await new Promise((resolve, reject) => {
                database.db.all(itemsQuery, [orderId], (err, rows) => {
                    if (err) reject(err);
                    else resolve(rows.map(row => ({
                        id: row.id,
                        product: {
                            id: row.product_id,
                            name: row.product_name,
                            description: row.product_description,
                            image_url: row.product_image_url,
                            category: row.product_category
                        },
                        quantity: row.quantity,
                        price: row.price,
                        subtotal: row.quantity * row.price
                    })));
                });
            });

            return {
                ...order,
                items
            };
        } catch (error) {
            console.error('获取订单详情失败:', error);
            throw error;
        }
    }

    // 更新订单状态
    async updateOrderStatus(orderId, status, userId = null) {
        let query = `
            UPDATE orders 
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        `;
        const params = [status, orderId];

        // 如果提供了userId，验证订单属于该用户
        if (userId) {
            query += ' AND user_id = ?';
            params.push(userId);
        }

        return new Promise((resolve, reject) => {
            database.db.run(query, params, function(err) {
                if (err) {
                    console.error('更新订单状态失败:', err);
                    reject(err);
                } else {
                    resolve(this.changes > 0);
                }
            });
        });
    }

    // 取消订单
    async cancelOrder(orderId, userId) {
        // 检查订单状态是否允许取消
        const order = await this.getOrderById(orderId, userId);
        if (!order) {
            throw new Error('订单不存在');
        }

        if (order.status !== 'pending') {
            throw new Error('订单状态不允许取消');
        }

        return this.updateOrderStatus(orderId, 'cancelled', userId);
    }
}

module.exports = new OrderDAO();
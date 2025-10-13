const database = require('./database');

class CartDAO {
    // 获取用户购物车
    async getCartByUserId(userId) {
        const query = `
            SELECT 
                ci.id,
                ci.quantity,
                ci.created_at,
                ci.updated_at,
                p.id as product_id,
                p.name as product_name,
                p.description as product_description,
                p.price as product_price,
                p.stock as product_stock,
                p.category as product_category,
                p.image_url as product_image_url
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.id
            WHERE ci.user_id = ?
            ORDER BY ci.created_at DESC
        `;

        return new Promise((resolve, reject) => {
            database.db.all(query, [userId], (err, rows) => {
                if (err) {
                    console.error('获取购物车失败:', err);
                    reject(err);
                } else {
                    // 格式化数据
                    const items = rows.map(row => ({
                        id: row.id,
                        quantity: row.quantity,
                        product: {
                            id: row.product_id,
                            name: row.product_name,
                            description: row.product_description,
                            price: row.product_price,
                            stock: row.product_stock,
                            category: row.product_category,
                            image_url: row.product_image_url
                        },
                        subtotal: row.quantity * row.product_price,
                        created_at: row.created_at,
                        updated_at: row.updated_at
                    }));

                    // 计算总金额
                    const totalAmount = items.reduce((sum, item) => sum + item.subtotal, 0);

                    resolve({
                        items,
                        totalAmount
                    });
                }
            });
        });
    }

    // 添加商品到购物车
    async addToCart(userId, productId, quantity) {
        // 先检查是否已存在该商品
        const checkQuery = `
            SELECT * FROM cart_items 
            WHERE user_id = ? AND product_id = ?
        `;

        return new Promise((resolve, reject) => {
            database.db.get(checkQuery, [userId, productId], (err, existingItem) => {
                if (err) {
                    console.error('检查购物车商品失败:', err);
                    reject(err);
                    return;
                }

                if (existingItem) {
                    // 更新数量
                    const updateQuery = `
                        UPDATE cart_items 
                        SET quantity = quantity + ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    `;
                    database.db.run(updateQuery, [quantity, existingItem.id], function(err) {
                        if (err) {
                            console.error('更新购物车失败:', err);
                            reject(err);
                        } else {
                            resolve({
                                id: existingItem.id,
                                changes: this.changes
                            });
                        }
                    });
                } else {
                    // 插入新记录
                    const insertQuery = `
                        INSERT INTO cart_items (user_id, product_id, quantity)
                        VALUES (?, ?, ?)
                    `;
                    database.db.run(insertQuery, [userId, productId, quantity], function(err) {
                        if (err) {
                            console.error('添加到购物车失败:', err);
                            reject(err);
                        } else {
                            resolve({
                                id: this.lastID,
                                changes: this.changes
                            });
                        }
                    });
                }
            });
        });
    }

    // 更新购物车商品数量
    async updateCartItem(cartItemId, userId, quantity) {
        if (quantity <= 0) {
            // 如果数量为0或负数，删除该项
            const deleteQuery = `
                DELETE FROM cart_items 
                WHERE id = ? AND user_id = ?
            `;
            return new Promise((resolve, reject) => {
                database.db.run(deleteQuery, [cartItemId], function(err) {
                    if (err) {
                        console.error('删除购物车商品失败:', err);
                        reject(err);
                    } else {
                        resolve(this.changes > 0);
                    }
                });
            });
        }

        const updateQuery = `
            UPDATE cart_items 
            SET quantity = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        `;

        return new Promise((resolve, reject) => {
            database.db.run(updateQuery, [quantity, cartItemId, userId], function(err) {
                if (err) {
                    console.error('更新购物车失败:', err);
                    reject(err);
                } else {
                    resolve(this.changes > 0);
                }
            });
        });
    }

    // 从购物车删除商品
    async removeFromCart(cartItemId, userId) {
        const query = `
            DELETE FROM cart_items 
            WHERE id = ? AND user_id = ?
        `;

        return new Promise((resolve, reject) => {
            database.db.run(query, [cartItemId, userId], function(err) {
                if (err) {
                    console.error('删除购物车商品失败:', err);
                    reject(err);
                } else {
                    resolve(this.changes > 0);
                }
            });
        });
    }

    // 清空用户购物车
    async clearCart(userId) {
        const query = `DELETE FROM cart_items WHERE user_id = ?`;

        return new Promise((resolve, reject) => {
            database.db.run(query, [userId], function(err) {
                if (err) {
                    console.error('清空购物车失败:', err);
                    reject(err);
                } else {
                    resolve(this.changes);
                }
            });
        });
    }

    // 获取购物车商品项
    async getCartItem(cartItemId, userId) {
        const query = `
            SELECT ci.*, p.name, p.price, p.stock
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.id
            WHERE ci.id = ? AND ci.user_id = ?
        `;

        return new Promise((resolve, reject) => {
            database.db.get(query, [cartItemId, userId], (err, row) => {
                if (err) {
                    console.error('获取购物车商品失败:', err);
                    reject(err);
                } else {
                    resolve(row);
                }
            });
        });
    }
}

module.exports = new CartDAO();
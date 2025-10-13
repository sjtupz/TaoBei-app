const database = require('./database');

class UserDAO {
    // DB-FindUserByPhone: 根据手机号查找用户记录
    async findUserByPhone(phoneNumber) {
        try {
            const sql = 'SELECT * FROM users WHERE phone_number = ?';
            const user = await database.get(sql, [phoneNumber]);
            return user || null;
        } catch (error) {
            console.error('查找用户失败:', error);
            throw error;
        }
    }

    // DB-CreateUser: 在数据库中创建一个新的用户记录
    async createUser(phoneNumber, nickname = null, avatar = null) {
        try {
            const sql = `
                INSERT INTO users (phone_number, nickname, avatar, created_at, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            `;
            const result = await database.run(sql, [phoneNumber, nickname, avatar]);
            
            // 返回新创建的用户信息
            return await this.findUserByPhone(phoneNumber);
        } catch (error) {
            if (error.code === 'SQLITE_CONSTRAINT_UNIQUE') {
                throw new Error('该手机号已注册');
            }
            console.error('创建用户失败:', error);
            throw error;
        }
    }

    // DB-UpdateUserProfile: 更新用户个人信息
    async updateUserProfile(phoneNumber, updates) {
        try {
            const allowedFields = ['nickname', 'avatar'];
            const updateFields = [];
            const values = [];

            // 只更新允许的字段
            for (const [key, value] of Object.entries(updates)) {
                if (allowedFields.includes(key) && value !== undefined) {
                    updateFields.push(`${key} = ?`);
                    values.push(value);
                }
            }

            if (updateFields.length === 0) {
                throw new Error('没有有效的更新字段');
            }

            values.push(phoneNumber); // 添加WHERE条件的参数

            const sql = `
                UPDATE users 
                SET ${updateFields.join(', ')}, updated_at = CURRENT_TIMESTAMP
                WHERE phone_number = ?
            `;

            const result = await database.run(sql, values);
            
            if (result.changes === 0) {
                throw new Error('用户不存在');
            }

            // 返回更新后的用户信息
            return await this.findUserByPhone(phoneNumber);
        } catch (error) {
            console.error('更新用户信息失败:', error);
            throw error;
        }
    }

    // 获取用户信息（通过ID）
    async getUserById(userId) {
        try {
            const sql = 'SELECT * FROM users WHERE id = ?';
            const user = await database.get(sql, [userId]);
            return user || null;
        } catch (error) {
            console.error('获取用户信息失败:', error);
            throw error;
        }
    }

    // 删除用户（用于测试）
    async deleteUser(phoneNumber) {
        try {
            const sql = 'DELETE FROM users WHERE phone_number = ?';
            const result = await database.run(sql, [phoneNumber]);
            return result.changes > 0;
        } catch (error) {
            console.error('删除用户失败:', error);
            throw error;
        }
    }
}

module.exports = new UserDAO();